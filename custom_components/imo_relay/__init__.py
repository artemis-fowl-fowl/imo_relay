"""Integration IMO Ismart Modbus Relay Control."""
import logging
from typing import Final

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, CONF_PORT, CONF_BAUDRATE, CONF_BYTESIZE, CONF_SLAVE_ID, CONF_NAME
from .modbus_client import ModbusRTUClient

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [Platform.SWITCH]

# Schéma de configuration
CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_PORT): cv.string,
        vol.Required(CONF_BAUDRATE, default=38400): cv.positive_int,
        vol.Required(CONF_BYTESIZE, default=8): cv.positive_int,
        vol.Required(CONF_SLAVE_ID, default=1): cv.positive_int,
        vol.Optional(CONF_NAME, default="IMO Relay"): cv.string,
    }, extra=vol.ALLOW_EXTRA)
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the IMO Relay integration from configuration."""
    hass.data[DOMAIN] = {}
    
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
    
    hass.data[DOMAIN]["client"] = client
    hass.data[DOMAIN]["config"] = conf
    
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
    
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the IMO Relay integration from config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    client = ModbusRTUClient(
        port=entry.data[CONF_PORT],
        baudrate=entry.data[CONF_BAUDRATE],
        bytesize=entry.data[CONF_BYTESIZE],
        slave_id=entry.data[CONF_SLAVE_ID],
        name=entry.data[CONF_NAME]
    )
    
    try:
        await hass.async_add_executor_job(client.connect)
        _LOGGER.info(f"Connected to IMO device on {entry.data[CONF_PORT]}")
    except Exception as e:
        _LOGGER.error(f"Failed to connect: {e}")
        return False
    
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "config": entry.data,
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        client = hass.data[DOMAIN][entry.entry_id]["client"]
        await hass.async_add_executor_job(client.close)
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
