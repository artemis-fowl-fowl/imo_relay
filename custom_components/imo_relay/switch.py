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
    CONF_RELAY_READ_ADDRESS,
    CONF_RELAY_ICON,
    CONF_RELAY_DEVICE_CLASS,
    CONF_RELAY_DEVICE_ID,
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
        read_address = relay_conf.get(CONF_RELAY_READ_ADDRESS)  # Optionnel
        icon = relay_conf.get(CONF_RELAY_ICON, "mdi:electric-switch")
        device_class = relay_conf.get(CONF_RELAY_DEVICE_CLASS)
        device_id = relay_conf.get(CONF_RELAY_DEVICE_ID)
        
        entities.append(
            IMORelaySwitch(
                client=client,
                relay_id=relay_id,
                address=address,
                read_address=read_address,
                name=name,
                icon=icon,
                device_class=device_class,
                device_id=device_id,
            )
        )
    
    async_add_entities(entities, True)


class IMORelaySwitch(SwitchEntity):
    """Représente un relais IMO Ismart."""
    
    _attr_has_entity_name = True
    _attr_assumed_state = False  # L'état est basé sur les dernières commandes envoyées
    
    def __init__(
        self,
        client: ModbusRTUClient,
        relay_id: str,
        address: int,
        read_address: int | None,
        name: str,
        icon: str | None = None,
        device_class: str | None = None,
        device_id: int | None = None,
    ):
        """Initialiser le switch."""
        self.client = client
        self.relay_id = relay_id
        self.address = address  # Adresse pour écrire
        self.read_address = read_address or address  # Adresse pour lire (si différente)
        self.device_id = device_id
        self._attr_name = name
        self._attr_unique_id = f"imo_relay_{relay_id}"
        self._attr_icon = icon or "mdi:electric-switch"
        if device_class:
            self._attr_device_class = device_class
        self._state = False  # État par défaut: OFF
    
    @property
    def is_on(self) -> bool | None:
        """Retourner l'état du relais."""
        return self._state
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Allumer le relais."""
        try:
            # Envoyer True pour allumer
            result = await self.hass.async_add_executor_job(
                self.client.write_coil, self.address, True, self.device_id
            )
            if result:
                _LOGGER.info(f"{self._attr_name} write coil ON command sent")
                # Lire l'état réel après l'écriture
                await self.async_update()
            else:
                _LOGGER.error(f"Failed to turn ON {self._attr_name}")
        except Exception as e:
            _LOGGER.error(f"Error turning ON {self._attr_name}: {e}")
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Éteindre le relais."""
        try:
            # Envoyer False pour éteindre
            result = await self.hass.async_add_executor_job(
                self.client.write_coil, self.address, False, self.device_id
            )
            if result:
                _LOGGER.info(f"{self._attr_name} write coil OFF command sent")
                # Lire l'état réel après l'écriture
                await self.async_update()
            else:
                _LOGGER.error(f"Failed to turn OFF {self._attr_name}")
        except Exception as e:
            _LOGGER.error(f"Error turning OFF {self._attr_name}: {e}")
    
    async def async_update(self) -> None:
        """Mettre à jour l'état du relais en lisant le coil Modbus."""
        try:
            _LOGGER.debug(f"Attempting to read state for {self._attr_name} at READ address {self.read_address:04X}")
            # Lire l'état réel depuis le Modbus à l'adresse de lecture (auto: coils puis discrete inputs)
            state = await self.hass.async_add_executor_job(
                self.client.read_bit, self.read_address, self.device_id
            )
            _LOGGER.info(f"Read bit {self.read_address:04X} result: {state}")
            if state is not None:
                # État réel sans inversion: True = ON, False = OFF
                self._state = bool(state)
                self.async_write_ha_state()
                _LOGGER.info(f"Updated {self._attr_name} state: {self._state}")
            else:
                _LOGGER.warning(f"Could not read state of {self._attr_name} (None returned)")
        except Exception as e:
            _LOGGER.error(f"Error reading {self._attr_name}: {e}", exc_info=True)
