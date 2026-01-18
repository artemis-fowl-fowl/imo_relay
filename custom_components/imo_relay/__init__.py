"""Integration IMO Ismart Modbus Relay Control."""
import logging

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
)
from .modbus_client import ModbusRTUClient

_LOGGER = logging.getLogger(__name__)

# Schéma pour un relais individuel
RELAY_SCHEMA = vol.Schema({
    vol.Required(CONF_RELAY_NAME): cv.string,
    vol.Required(CONF_RELAY_ADDRESS): cv.positive_int,
    vol.Optional(CONF_RELAY_READ_ADDRESS): cv.positive_int,  # Adresse de lecture optionnelle
    vol.Optional(CONF_RELAY_ICON, default="mdi:electric-switch"): cv.icon,
    vol.Optional(CONF_RELAY_DEVICE_CLASS): cv.string,
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


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the IMO Relay integration from configuration.yaml."""
    if DOMAIN not in config:
        return True
    
    conf = config[DOMAIN]
    
    # Créer le client Modbus
    client = ModbusRTUClient(
        port=conf[CONF_PORT],
        baudrate=conf[CONF_BAUDRATE],
        bytesize=conf[CONF_BYTESIZE],
        slave_id=conf[CONF_SLAVE_ID],
        name=conf[CONF_NAME]
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
    }
    
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
    
    return True
