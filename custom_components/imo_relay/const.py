"""Constants for IMO Relay integration."""

DOMAIN = "imo_relay"

# Configuration keys
CONF_PORT = "port"
CONF_BAUDRATE = "baudrate"
CONF_BYTESIZE = "bytesize"
CONF_SLAVE_ID = "slave_id"
CONF_NAME = "name"
CONF_RELAYS = "relays"

# Relay configuration keys
CONF_RELAY_NAME = "name"
CONF_RELAY_ADDRESS = "address"
CONF_RELAY_ICON = "icon"
CONF_RELAY_DEVICE_CLASS = "device_class"

# Defaults
DEFAULT_BAUDRATE = 38400
DEFAULT_BYTESIZE = 8
DEFAULT_SLAVE_ID = 1
DEFAULT_ICON = "mdi:electric-switch"

# Modbus defaults
DEFAULT_PARITY = "N"
DEFAULT_STOPBITS = 1
DEFAULT_TIMEOUT = 3
