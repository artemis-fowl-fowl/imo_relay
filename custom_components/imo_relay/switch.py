"""Switch platform for IMO Relay integration."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    DOMAIN,
    CONF_RELAY_NAME,
    CONF_RELAY_ADDRESS,
    CONF_RELAY_ICON,
    CONF_RELAY_DEVICE_CLASS,
)
from .modbus_client import ModbusRTUClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up switch platform from configuration.yaml."""
    client: ModbusRTUClient = hass.data[DOMAIN]["client"]
    relays_config = hass.data[DOMAIN]["relays"]
    
    # Créer les entités de relais dynamiquement depuis la config
    entities = []
    for idx, relay_conf in enumerate(relays_config):
        relay_id = f"relay_{idx + 1}"
        name = relay_conf[CONF_RELAY_NAME]
        address = relay_conf[CONF_RELAY_ADDRESS]
        icon = relay_conf.get(CONF_RELAY_ICON, "mdi:electric-switch")
        device_class = relay_conf.get(CONF_RELAY_DEVICE_CLASS)
        
        entities.append(
            IMORelaySwitch(
                client=client,
                relay_id=relay_id,
                address=address,
                name=name,
                icon=icon,
                device_class=device_class,
            )
        )
    
    async_add_entities(entities, True)


class IMORelaySwitch(SwitchEntity):
    """Représente un relais IMO Ismart."""
    
    _attr_has_entity_name = True
    
    def __init__(
        self,
        client: ModbusRTUClient,
        relay_id: str,
        address: int,
        name: str,
        icon: str | None = None,
        device_class: str | None = None,
    ):
        """Initialiser le switch."""
        self.client = client
        self.relay_id = relay_id
        self.address = address
        self._attr_name = name
        self._attr_unique_id = f"imo_relay_{relay_id}"
        self._attr_icon = icon or "mdi:electric-switch"
        if device_class:
            self._attr_device_class = device_class
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
        # Désactivé pour éviter les erreurs de lecture
        # Les relais Modbus RTU ne supportent pas toujours la lecture d'état
        # L'état est mis à jour après chaque write_coil
        pass
        # try:
        #     state = await self.hass.async_add_executor_job(
        #         self.client.read_coil, self.address
        #     )
        #     if state is not None:
        #         self._state = state
        #     else:
        #         _LOGGER.warning(f"Failed to read state of {self._attr_name}")
        # except Exception as e:
        #     _LOGGER.error(f"Error updating {self._attr_name}: {e}")
