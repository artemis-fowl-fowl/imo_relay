"""Integration IMO Ismart Modbus Relay Control."""
import logging
import asyncio

import voluptuous as vol
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import async_load_platform

from .const import (
    DOMAIN,
    CONF_PORT,
    CONF_BAUDRATE,
    CONF_BYTESIZE,
    CONF_SLAVE_ID,
    CONF_NAME,
    CONF_RELAYS,
    CONF_RELAY_NAME,
    CONF_RELAY_ADDRESS,
    CONF_RELAY_READ_ADDRESS,
    CONF_RELAY_ICON,
    CONF_RELAY_DEVICE_CLASS,
    CONF_RELAY_DEVICE_ID,
    CONF_LIGHTS,
    CONF_LIGHT_COIL_ADDRESS,
    CONF_LIGHT_DEVICE_CLASS,
    CONF_LIGHT_DEVICE_ID,
    CONF_LIGHT_ICON,
    CONF_LIGHT_NAME,
    CONF_LIGHT_POSITION,
    CONF_LIGHT_READ_ADDRESS,
    CONF_SHUTTER_ICON,
    CONF_SHUTTER_DEVICE_ID,
    CONF_SHUTTER_DOWN_COIL,
    CONF_SHUTTER_DOWN_POSITION,
    CONF_SHUTTER_NAME,
    CONF_SHUTTER_OUTPUT_ADDRESS,
    CONF_SHUTTER_STATE_ADDRESS,
    CONF_SHUTTER_STATE_DOWN_POSITION,
    CONF_SHUTTER_STATE_UP_POSITION,
    CONF_SHUTTER_UP_COIL,
    CONF_SHUTTER_UP_POSITION,
    CONF_SHUTTERT_DEVICE_CLASS,
)
from .modbus_client import ModbusRTUClient

_LOGGER = logging.getLogger(__name__)

# individual relay schematic
# Voluptuous is a librairy intended for validating data coming into Pyhton as JSON, YAML...
# The schematic defines attributs that will be configured through the YAML
# Attributs may bye required or optional. The have a name and 
RELAY_SCHEMA = vol.Schema({
    vol.Required(CONF_RELAY_NAME): cv.string,                   # RELAY_NAME (sring) required
    vol.Required(CONF_RELAY_ADDRESS): cv.positive_int,          # Register address
    vol.Optional(CONF_RELAY_READ_ADDRESS): cv.positive_int,     # Adresse de lecture optionnelle
    vol.Optional(CONF_RELAY_ICON, default="mdi:electric-switch"): cv.icon,  # Icon symbole interrupteur classique
    vol.Optional(CONF_RELAY_DEVICE_CLASS): cv.string,
    vol.Optional(CONF_RELAY_DEVICE_ID): cv.positive_int,  # Identifiant esclave spécifique au relais
})
"""
SHUTTER_SCHEMA = vol.Schema({
    vol.Required(CONF_SHUTTER_NAME): cv.string,                                 # RELAY_NAME (sring) required
    vol.Required(CONF_SHUTTER_DEVICE_ID): cv.positive_int,                      # Identifiant esclave spécifique au relais
    vol.Required(CONF_SHUTTER_UP_COIL): cv.positive_int,                        # Coil address for shutter up drive
    vol.Required(CONF_SHUTTER_DOWN_COIL): cv.positive_int,                      # Coil address for shutter down drive
    vol.Required(CONF_SHUTTER_OUTPUT_ADDRESS): cv.positive_int,                 # Register adresse for shutter's moving state read
    vol.Required(CONF_SHUTTER_UP_POSITION): cv.positive_int,                    # Position of up bit in state's register
    vol.Required(CONF_SHUTTER_DOWN_POSITION): cv.positive_int,                  # Position of down bit in the state's register
    vol.Optional(CONF_SHUTTER_STATE_ADDRESS): cv.positive_int,                  # Register adresse for shutter's state read (If not defined is the M register address corresponding to the output)
    vol.Optional(CONF_SHUTTER_STATE_UP_POSITION): cv.positive_int,              # Position of up bit in the state's register (If not defined is same as SHUTTER_UP_POSITION)
    vol.Optional(CONF_SHUTTER_STATE_DOWN_POSITION): cv.positive_int,            # Position of down bit in the state's register (If not defined is same as SHUTTER_DOWN_POSITION)
    vol.Optional(CONF_SHUTTER_ICON, default="mdi:electric-switch"): cv.icon,
    vol.Optional(CONF_SHUTTERT_DEVICE_CLASS): cv.string,   
})
"""
LIGHT_SCHEMA = vol.Schema({
    vol.Required(CONF_LIGHT_NAME): cv.string,                               # RELAY_NAME (sring) required
    vol.Required(CONF_LIGHT_DEVICE_ID): cv.positive_int,                    # Identifiant esclave spécifique au relais
    vol.Required(CONF_LIGHT_COIL_ADDRESS): cv.positive_int,                 # Coil address for light toggling
    vol.Required(CONF_LIGHT_READ_ADDRESS): cv.positive_int,                 # Register adresse for light state read
    vol.Required(CONF_LIGHT_POSITION): cv.positive_int,                     # Position of the light bit in the state's register
    vol.Optional(CONF_LIGHT_ICON, default="mdi:electric-switch"): cv.icon,
    vol.Optional(CONF_LIGHT_DEVICE_CLASS): cv.string,   
})

# Schéma de configuration
CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_PORT): cv.string,
        vol.Required(CONF_BAUDRATE, default=38400): cv.positive_int,
        vol.Required(CONF_BYTESIZE, default=8): cv.positive_int,
        vol.Required(CONF_SLAVE_ID, default=1): cv.positive_int,
        vol.Optional(CONF_NAME, default="IMO Relay"): cv.string,
        vol.Required(CONF_RELAYS): vol.All(cv.ensure_list, [RELAY_SCHEMA]),
    })
}, extra=vol.ALLOW_EXTRA)

# Appel du setup en asynchrone (il semble qu'il serait également possible de le faire en syncrhone)
async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the IMO Relay integration from configuration.yaml."""
    if DOMAIN not in config:
        return True
    
    conf = config[DOMAIN]
    
    # Créer le client Modbus (with parity E like working config)
    client = ModbusRTUClient(
        port=conf[CONF_PORT],
        baudrate=conf[CONF_BAUDRATE],
        bytesize=conf[CONF_BYTESIZE],
        parity="N",
        stopbits=1,
        timeout=5,
        slave_id=conf[CONF_SLAVE_ID],
        name=conf[CONF_NAME],
        delay=0,
        message_wait_ms=30,
    )
    
    # Test de connexion
    try:
        await hass.async_add_executor_job(client.connect)
        _LOGGER.info(f"Connected to IMO device on {conf[CONF_PORT]}")
    except Exception as e:
        _LOGGER.error(f"Failed to connect to IMO device: {e}")
        return False
    
    hass.data[DOMAIN] = {
        "client": client,
        "config": conf,
        "relays": conf[CONF_RELAYS],
        "lights": conf[CONF_LIGHTS],
        "entities": [],  # Liste des entités pour mise à jour globale
    }
    
    # Lancer la boucle d'update automatique (toutes les 2 secondes, comme scripts.js)
    async def update_loop():
        """Boucle d'update automatique pour tous les relais (lecture groupée par automate)."""
        while True:
            try:
                await asyncio.sleep(2)                              # Update toutes les 2 secondes
                entities = hass.data[DOMAIN].get("entities", [])
                relays_config = hass.data[DOMAIN]["relays"]
                
                # Grouper les relais par device_id pour lecturer en masse
                relays_by_device = {}
                for relay_conf in relays_config:
                    device_id = relay_conf.get(CONF_RELAY_DEVICE_ID, conf[CONF_SLAVE_ID])
                    if device_id not in relays_by_device:
                        relays_by_device[device_id] = []
                    relays_by_device[device_id].append(relay_conf)
                
                # Lire les états par automate (holding register 0x0613 contient les 16 bits Q+Y)
                for device_id, relays in relays_by_device.items():
                    # Lire le holding register 0x0613 qui contient tous les états (comme scripts.js)
                    bits = await hass.async_add_executor_job(
                        client.read_coils_bulk, 0x0613, 16, device_id
                    )
                    
                    if bits:
                        # Mettre à jour tous les relais de cet automate
                        for entity in entities:
                            # Vérifier si le relais appartient à cet automate
                            if entity.device_id == device_id:
                                # Extraire le bit correspondant au read_address
                                read_addr = entity.read_address
                                # Conversion: 0x0000-0x0007 = index 0-7, 0x0010-0x0017 = index 8-15
                                if read_addr <= 0x0007:
                                    bit_index = read_addr
                                elif read_addr >= 0x0010 and read_addr <= 0x0017:
                                    bit_index = 8 + (read_addr - 0x0010)
                                else:
                                    _LOGGER.warning(f"Unknown read_address {read_addr:04X} for {entity._attr_name}")
                                    continue
                                
                                if bit_index < len(bits):
                                    entity._state = bool(bits[bit_index])
                                    entity.async_write_ha_state()
                                    _LOGGER.debug(f"Updated {entity._attr_name}: {entity._state}")
                    
            except Exception as e:
                _LOGGER.error(f"Error in update loop: {e}", exc_info=True)
    
    hass.async_create_task(update_loop())
    
    # Service pour écrire une bobine
    async def write_coil_service(call: ServiceCall) -> None:
        """Service pour écrire une bobine."""
        address = call.data.get("address")
        state = call.data.get("state")
        
        try:
            await hass.async_add_executor_job(
                client.write_coil, address, state
            )
            _LOGGER.info(f"Wrote coil {address:04X} = {state}")
        except Exception as e:
            _LOGGER.error(f"Failed to write coil: {e}")
    
    # Enregistrer le service
    hass.services.async_register(
        DOMAIN,
        "write_coil",
        write_coil_service,
        schema=vol.Schema({
            vol.Required("address"): cv.positive_int,
            vol.Required("state"): cv.boolean,
        })
    )
    
    # Charger la plateforme switch
    hass.async_create_task(
        async_load_platform(hass, Platform.SWITCH, DOMAIN, {}, config)
    )

    # Charger la plateforme light
    hass.async_create_task(
        async_load_platform(hass, Platform.LIGHT, DOMAIN, {}, config)
    )

    return True
