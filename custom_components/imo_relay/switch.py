"""Switch platform for IMO Relay integration."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_NAME
from .modbus_client import ModbusRTUClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switch platform from a config entry."""
    client: ModbusRTUClient = hass.data[DOMAIN][config_entry.entry_id]["client"]
    config = hass.data[DOMAIN][config_entry.entry_id]["config"]
    
    # Créer les entités de relais
    entities = [
        IMORelaySwitch(client, "relay_1", 0x0551, "Relay 1"),
        IMORelaySwitch(client, "relay_2", 0x0552, "Relay 2"),
        IMORelaySwitch(client, "relay_3", 0x0553, "Relay 3"),
        IMORelaySwitch(client, "relay_4", 0x0554, "Relay 4"),
    ]
    
    async_add_entities(entities)


class IMORelaySwitch(SwitchEntity):
    """Représente un relais IMO Ismart."""
    
    _attr_device_class = SwitchDeviceClass.SWITCH
    _attr_has_entity_name = True
    
    def __init__(
        self,
        client: ModbusRTUClient,
        relay_id: str,
        address: int,
        name: str,
    ):
        """Initialiser le switch."""
        self.client = client
        self.relay_id = relay_id
        self.address = address
        self._attr_name = name
        self._attr_unique_id = f"imo_relay_{relay_id}"
        self._state = None
    
    @property
    def is_on(self) -> bool | None:
        """Retourner l'état du relais."""
        return self._state
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Allumer le relais."""
        try:
            result = await self.hass.async_add_executor_job(
                self.client.write_coil, self.address, True
            )
            if result:
                self._state = True
                self.async_write_ha_state()
                _LOGGER.info(f"{self._attr_name} turned ON")
            else:
                _LOGGER.error(f"Failed to turn ON {self._attr_name}")
        except Exception as e:
            _LOGGER.error(f"Error turning ON {self._attr_name}: {e}")
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Éteindre le relais."""
        try:
            result = await self.hass.async_add_executor_job(
                self.client.write_coil, self.address, False
            )
            if result:
                self._state = False
                self.async_write_ha_state()
                _LOGGER.info(f"{self._attr_name} turned OFF")
            else:
                _LOGGER.error(f"Failed to turn OFF {self._attr_name}")
        except Exception as e:
            _LOGGER.error(f"Error turning OFF {self._attr_name}: {e}")
    
    async def async_update(self) -> None:
        """Mettre à jour l'état du relais."""
        try:
            state = await self.hass.async_add_executor_job(
                self.client.read_coil, self.address
            )
            if state is not None:
                self._state = state
            else:
                _LOGGER.warning(f"Failed to read state of {self._attr_name}")
        except Exception as e:
            _LOGGER.error(f"Error updating {self._attr_name}: {e}")
