"""Constants for IMO Relay integration."""

DOMAIN = "imo_relay"

# Configuration keys
CONF_PORT = "port"
CONF_BAUDRATE = "baudrate"
CONF_BYTESIZE = "bytesize"
CONF_SLAVE_ID = "slave_id"
CONF_NAME = "name"
CONF_RELAYS = "relays"

# Defaults
DEFAULT_BAUDRATE = 38400
DEFAULT_BYTESIZE = 8
DEFAULT_SLAVE_ID = 1

# Modbus defaults
DEFAULT_PARITY = "N"
DEFAULT_STOPBITS = 1
DEFAULT_TIMEOUT = 3

# SMT-CD-T20 Modbus addresses
RELAY_ADDRESSES = {
    "relay_1": 0x0551,
    "relay_2": 0x0552,
    "relay_3": 0x0553,
    "relay_4": 0x0554,
}
