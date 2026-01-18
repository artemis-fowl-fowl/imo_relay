# Configuration pour config_entries (optionnel - future enhancement)

import voluptuous as vol
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, CONF_PORT, CONF_BAUDRATE, CONF_BYTESIZE, CONF_SLAVE_ID, CONF_NAME

class ConfigFlow:
    """Config flow pour IMO Relay."""
    
    VERSION = 1
    CONNECTION_CLASS = None
    
    async def async_step_user(self, user_input=None):
        """Configuration initiale."""
        if user_input is not None:
            # Valider et créer l'entrée
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input
            )
        
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_PORT): cv.string,
                vol.Required(CONF_BAUDRATE, default=38400): cv.positive_int,
                vol.Required(CONF_BYTESIZE, default=8): cv.positive_int,
                vol.Required(CONF_SLAVE_ID, default=1): cv.positive_int,
                vol.Optional(CONF_NAME, default="IMO Relay"): cv.string,
            })
        )
