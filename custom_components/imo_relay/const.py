"""Constants for IMO Relay integration."""

DOMAIN = "imo_relay"        # C'est ce nom de "domaine" qui doit être utilisé dans les yaml: "imo_relay:"
                            # Le répertoire du module doit être dans custom_components et doit avoir le même nom que le domaine.

# Configuration keys
CONF_PORT = "port"
CONF_BAUDRATE = "baudrate"
CONF_BYTESIZE = "bytesize"
CONF_SLAVE_ID = "slave_id"
CONF_NAME = "name"
CONF_RELAYS = "relays"
CONF_SHUTTER = "shutters"
CONF_LIGHT = "lights"

# Light configuration keys
CONF_LIGHT_NAME = "name"
CONF_LIGHT_DEVICE_ID = "device_id"
CONF_LIGHT_COIL_ADDRESS = "coil"
CONF_LIGHT_READ_ADDRESS = "read_address"
CONF_LIGHT_POSITION = "position"
CONF_LIGHT_ICON = "icon"
CONF_LIGHT_DEVICE_CLASS = "device_class"

# Shutter configuration keys
CONF_SHUTTER_NAME = "name"
CONF_SHUTTER_DEVICE_ID = "device_id"
CONF_SHUTTER_UP_COIL = "up_coil"
CONF_SHUTTER_DOWN_COIL = "down_coil"
CONF_SHUTTER_OUTPUT_ADDRESS = "out_address"
CONF_SHUTTER_UP_POSITION = "up_pos"
CONF_SHUTTER_DOWN_POSITION = "down_pos"
CONF_SHUTTER_STATE_ADDRESS = "state_address"
CONF_SHUTTER_STATE_UP_POSITION = "state_up_pos"
CONF_SHUTTER_STATE_DOWN_POSITION = "state_down_pos"
CONF_SHUTTER_ICON = "icon"
CONF_SHUTTERT_DEVICE_CLASS = "device_class"  

# Relay configuration keys
CONF_RELAY_NAME = "name"
CONF_RELAY_ADDRESS = "address"
CONF_RELAY_READ_ADDRESS = "read_address"  # Adresse pour lire l'état
CONF_RELAY_ICON = "icon"
CONF_RELAY_DEVICE_CLASS = "device_class"
CONF_RELAY_DEVICE_ID = "device_id"

DEFAULT_ICON = "mdi:electric-switch"    # Icon interrupteur très simple

# Modbus RS485 link parameters
DEFAULT_BAUDRATE = 38400            #38400 bauds
DEFAULT_BYTESIZE = 8                # 8bits
DEFAULT_SLAVE_ID = 1                    # !!! N'a pas beaucoup de sens à supprimmer



#DEFAULT_PARITY = "E"        # Even parity to be corrected ?

DEFAULT_PARITY = "N"                # No parity
DEFAULT_STOPBITS = 1                # One stop bit
DEFAULT_TIMEOUT = 5
DEFAULT_DELAY = 0
DEFAULT_MESSAGE_WAIT_MS = 30
