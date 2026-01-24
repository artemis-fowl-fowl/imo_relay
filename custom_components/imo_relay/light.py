"""Switch platform for IMO Relay integration."""
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    DOMAIN,
    CONF_LIGHT_NAME,
    CONF_LIGHT_DEVICE_ID,
    CONF_LIGHT_COIL_ADDRESS,
    CONF_LIGHT_READ_ADDRESS,
    CONF_LIGHT_POSITION,
    CONF_LIGHT_ICON,
    CONF_LIGHT_DEVICE_CLASS,

)

from .modbus_client import ModbusRTUClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up light platform from configuration.yaml."""
    client: ModbusRTUClient = hass.data[DOMAIN]["client"]
    lights_config = hass.data[DOMAIN]["lights"]
    
    # Créer les entités de lights dynamiquement depuis la config
    entities = []
    for idx, light_conf in enumerate(lights_config):
        light_id = f"light_{idx + 1}"
        name = light_conf[CONF_LIGHT_NAME]
        coil_address = light_conf[CONF_LIGHT_COIL_ADDRESS]
        read_address = light_conf.get(CONF_LIGHT_READ_ADDRESS)
        position = light_conf.get(CONF_LIGHT_POSITION)
        icon = light_conf.get(CONF_LIGHT    _ICON, "mdi:electric-switch")
        device_class = light_conf.get(CONF_LIGHT_DEVICE_CLASS)
        device_id = light_conf.get(CONF_LIGHT_DEVICE_ID)
        
        entities.append(
            IMOLightSwitch(
                client = client,
                light_id = light_id,
                name = name,
                device_id = device_id,
                coil_address = coil_address,
                read_address = read_address,
                position = position,
                icon = icon,
                device_class = device_class,
            )
        )
    
    async_add_entities(entities, True)
    
    # Enregistrer les entités pour la boucle d'update automatique
    hass.data[DOMAIN]["entities"] = entities



class IMOLightSwitch(SwitchEntity):
    """Représente un relais IMO Ismart."""
    
    _attr_has_entity_name = True
    _attr_assumed_state = False  # L'état est basé sur les dernières commandes envoyées
    
    def __init__(
        self,
        client: ModbusRTUClient,
        light_id: str,
        device_id: int,
        coil_address: int,
        read_address: int,
        position: int,
        name: str,
        icon: str | None = None,
        device_class: str | None = None,
    ):
        """Initialiser le switch."""
        self.client = client
        self.light_id = light_id
        self.coil_address = coil_address    # Adresse pour écrire
        self.read_address = read_address    # Adresse pour lire (si différente)
        self.position = position
        self.device_id = device_id
        self._attr_name = name
        self._attr_unique_id = f"imo_relay_{relay_id}"
        self._attr_icon = icon or "mdi:electric-switch"
        # Ignorer device_class pour éviter les sliders (juste des switches simples)
        self._state = False  # État par défaut: OFF

    
    @property
    def is_on(self) -> bool | None:
        """Retourner l'état du relais."""
        return self._state
    
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Allumer la lumière"""
        try:
            # Envoyer True pour allumer
            result = await self.hass.async_add_executor_job(
                self.client.write_coil, self.coil_address, True, self.device_id
            )
            if result:
                _LOGGER.info(f"{self._attr_name} write coil ON command sent")
                # Lire l'état réel après l'écriture (sans attendre, la boucle d'update va rafraîchir)


            else:
                _LOGGER.error(f"Failed to turn ON {self._attr_name}")
        except Exception as e:
            _LOGGER.error(f"Error turning ON {self._attr_name}: {e}")
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Éteindre le relais."""
        try:
            # Envoyer False pour éteindre
            result = await self.hass.async_add_executor_job(
                self.client.write_coil, self.coil_address, True, self.device_id
            )
            if result:
                _LOGGER.info(f"{self._attr_name} write coil OFF command sent")
                # Lire l'état réel après l'écriture (sans attendre, la boucle d'update va rafraîchir)


            else:
                _LOGGER.error(f"Failed to turn OFF {self._attr_name}")
        except Exception as e:
            _LOGGER.error(f"Error turning OFF {self._attr_name}: {e}")
    
    async def async_update(self) -> None:
        """Mettre à jour l'état du relais en lisant le coil Modbus."""
        try:
            _LOGGER.debug(f"Manual update for {self._attr_name} at READ address {self.read_address:04X}")
            # Lire l'état réel depuis le Modbus à l'adresse de lecture (auto: coils puis discrete inputs)
            state = await self.hass.async_add_executor_job(self.client.read_bit, self.read_address, self.device_id)
            _LOGGER.debug(f"Read bit {self.read_address:04X} result: {state}")
            if state is not None:
                # État réel sans inversion: True = ON, False = OFF
                self._state = bool(state)
                self.async_write_ha_state()
                _LOGGER.debug(f"Updated {self._attr_name} state: {self._state}")
            else:
                _LOGGER.warning(f"Could not read state of {self._attr_name} (None returned)")
        except Exception as e:
            _LOGGER.error(f"Error reading {self._attr_name}: {e}", exc_info=True)
