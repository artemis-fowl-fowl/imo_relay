"""Modbus RTU client for IMO Ismart devices."""
import logging
from typing import Optional
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException
from pymodbus.pdu import ExceptionResponse

_LOGGER = logging.getLogger(__name__)


class ModbusRTUClient:
    """Client Modbus RTU pour contrôler les relais IMO Ismart."""
    
    def __init__(
        self,
        port: str,
        baudrate: int = 38400,
        bytesize: int = 8,
        parity: str = "N",
        stopbits: int = 1,
        timeout: int = 3,
        slave_id: int = 1,
        name: str = "IMO Relay"
    ):
        """Initialiser le client Modbus RTU."""
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.slave_id = slave_id
        self.name = name
        
        self.client = ModbusSerialClient(
            port=port,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout,
        )
        
        _LOGGER.debug(f"Initialized {name} client on {port}")
    
    def connect(self) -> bool:
        """Connecter au device Modbus."""
        try:
            if self.client.connected:
                _LOGGER.info(f"{self.name} already connected to {self.port}")
                return True
            
            is_connected = self.client.connect()
            if is_connected:
                _LOGGER.info(f"{self.name} connected to {self.port} - slave_id: {self.slave_id}")
                return True
            else:
                _LOGGER.error(f"Failed to connect to {self.port} - Check device and port")
                return False
        except Exception as e:
            _LOGGER.error(f"Connection error on {self.port}: {e}", exc_info=True)
            return False
    
    def close(self) -> None:
        """Fermer la connexion."""
        try:
            self.client.close()
            _LOGGER.info(f"{self.name} disconnected")
        except Exception as e:
            _LOGGER.error(f"Error closing connection: {e}")
    
    def write_coil(self, address: int, state: bool, device_id: int | None = None) -> bool:
        """
        Écrire une bobine (coil).
        
        Args:
            address: Adresse de la bobine (ex: 0x0551)
            state: État de la bobine (True/False)
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            _LOGGER.debug(f"Writing coil {address:04X} = {state}")
            
            result = self.client.write_coil(
                address,
                state,
                device_id=device_id or self.slave_id
            )
            
            if isinstance(result, ExceptionResponse):
                _LOGGER.error(f"Modbus exception: {result}")
                return False
            
            if result.isError():
                _LOGGER.error(f"Failed to write coil: {result}")
                return False
            
            _LOGGER.info(f"Successfully wrote coil {address:04X} = {state}")
            return True
            
        except ModbusException as e:
            _LOGGER.error(f"Modbus error: {e}")
            return False
        except Exception as e:
            _LOGGER.error(f"Unexpected error writing coil: {e}")
            return False
    
    def read_coil(self, address: int, device_id: int | None = None) -> Optional[bool]:
        """
        Lire une bobine (coil).
        
        Args:
            address: Adresse de la bobine
        
        Returns:
            bool ou None: État de la bobine ou None si erreur
        """
        try:
            if not self.client.connected:
                _LOGGER.warning(f"Client not connected, attempting to reconnect...")
                self.connect()
            
            _LOGGER.debug(f"Reading coil {address:04X} (dec:{address}) from slave {device_id or self.slave_id}")
            
            result = self.client.read_coils(
                address=address,
                count=1,
                unit=device_id or self.slave_id
            )
            
            if isinstance(result, ExceptionResponse):
                _LOGGER.error(f"Modbus exception reading coil {address:04X}: {result}")
                return None
            
            if result.isError():
                _LOGGER.error(f"Failed to read coil {address:04X}: {result}")
                return None
            
            if not hasattr(result, 'bits') or not result.bits:
                _LOGGER.error(f"Invalid response for coil {address:04X}: no bits data")
                return None
            
            state = result.bits[0]
            _LOGGER.debug(f"Read coil {address:04X} = {state}")
            return state
            
        except ModbusException as e:
            _LOGGER.error(f"Modbus error reading coil {address:04X}: {e}")
            return None

    def read_bit(self, address: int, device_id: int | None = None) -> Optional[bool]:
        """
        Lire un bit en tentant d'abord les coils (FC01) puis les discrete inputs (FC02).

        Args:
            address: Adresse du bit
            device_id: Esclave Modbus à interroger

        Returns:
            bool ou None
        """
        # Essai lecture en coils
        state = self.read_coil(address, device_id)
        if state is not None:
            return state

        # Fallback: lecture en discrete inputs
        try:
            if not self.client.connected:
                _LOGGER.warning("Client not connected, attempting to reconnect...")
                self.connect()

            _LOGGER.debug(f"Reading discrete input {address:04X} from slave {device_id or self.slave_id}")
            result = self.client.read_discrete_inputs(
                address=address,
                count=1,
                unit=device_id or self.slave_id,
            )

            if isinstance(result, ExceptionResponse):
                _LOGGER.error(f"Modbus exception reading discrete input {address:04X}: {result}")
                return None

            if result.isError():
                _LOGGER.error(f"Failed to read discrete input {address:04X}: {result}")
                return None

            if not hasattr(result, 'bits') or not result.bits:
                _LOGGER.error(f"Invalid response for discrete input {address:04X}: no bits data")
                return None

            di_state = result.bits[0]
            _LOGGER.debug(f"Read discrete input {address:04X} = {di_state}")
            return di_state
        except Exception as e:
            _LOGGER.error(f"Unexpected error reading discrete input {address:04X}: {e}", exc_info=True)
            return None

    def read_coils_bulk(self, address: int, count: int = 16, device_id: int | None = None) -> Optional[list]:
        """
        Lire plusieurs coils d'un coup (16 par défaut pour un automate complet Q+Y).

        Args:
            address: Adresse de départ
            count: Nombre de coils à lire (16 par défaut)
            device_id: Esclave Modbus à interroger

        Returns:
            list[bool] ou None: Liste des bits ou None si erreur
        """
        try:
            if not self.client.connected:
                _LOGGER.warning("Client not connected, attempting to reconnect...")
                self.connect()

            _LOGGER.debug(f"Reading {count} coils from {address:04X} on slave {device_id or self.slave_id}")
            result = self.client.read_coils(
                address=address,
                count=count,
                unit=device_id or self.slave_id,
            )

            if isinstance(result, ExceptionResponse):
                _LOGGER.error(f"Modbus exception reading {count} coils from {address:04X}: {result}")
                return None

            if result.isError():
                _LOGGER.error(f"Failed to read {count} coils from {address:04X}: {result}")
                return None

            if not hasattr(result, 'bits') or not result.bits:
                _LOGGER.error(f"Invalid response for {count} coils from {address:04X}: no bits data")
                return None

            _LOGGER.debug(f"Read {count} coils from {address:04X}: {result.bits}")
            return result.bits

        except Exception as e:
            _LOGGER.error(f"Unexpected error reading {count} coils from {address:04X}: {e}", exc_info=True)
            return None

        except AttributeError as e:
            _LOGGER.error(f"Attribute error reading coil {address:04X}: {e} - Check Modbus connection")
            return None
        except Exception as e:
            _LOGGER.error(f"Unexpected error reading coil {address:04X}: {e}", exc_info=True)
            return None
    
    def write_register(self, address: int, value: int, device_id: int | None = None) -> bool:
        """
        Écrire un registre.
        
        Args:
            address: Adresse du registre
            value: Valeur à écrire
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            _LOGGER.debug(f"Writing register {address:04X} = {value}")
            
            result = self.client.write_register(
                address,
                value,
                device_id=device_id or self.slave_id
            )
            
            if isinstance(result, ExceptionResponse):
                _LOGGER.error(f"Modbus exception: {result}")
                return False
            
            if result.isError():
                _LOGGER.error(f"Failed to write register: {result}")
                return False
            
            _LOGGER.info(f"Successfully wrote register {address:04X} = {value}")
            return True
            
        except ModbusException as e:
            _LOGGER.error(f"Modbus error: {e}")
            return False
        except Exception as e:
            _LOGGER.error(f"Unexpected error writing register: {e}")
            return False
    
    def read_register(self, address: int, device_id: int | None = None) -> Optional[int]:
        """
        Lire un registre.
        
        Args:
            address: Adresse du registre
        
        Returns:
            int ou None: Valeur du registre ou None si erreur
        """
        try:
            _LOGGER.debug(f"Reading register {address:04X}")
            
            result = self.client.read_holding_registers(
                address,
                count=1,
                device_id=device_id or self.slave_id
            )
            
            if isinstance(result, ExceptionResponse):
                _LOGGER.error(f"Modbus exception: {result}")
                return None
            
            if result.isError():
                _LOGGER.error(f"Failed to read register: {result}")
                return None
            
            value = result.registers[0] if result.registers else 0
            _LOGGER.debug(f"Read register {address:04X} = {value}")
            return value
            
        except ModbusException as e:
            _LOGGER.error(f"Modbus error: {e}")
            return None
        except Exception as e:
            _LOGGER.error(f"Unexpected error reading register: {e}")
            return None
