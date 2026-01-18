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
            is_connected = self.client.connect()
            if is_connected:
                _LOGGER.info(f"{self.name} connected to {self.port}")
                return True
            else:
                _LOGGER.error(f"Failed to connect to {self.port}")
                return False
        except Exception as e:
            _LOGGER.error(f"Connection error: {e}")
            return False
    
    def close(self) -> None:
        """Fermer la connexion."""
        try:
            self.client.close()
            _LOGGER.info(f"{self.name} disconnected")
        except Exception as e:
            _LOGGER.error(f"Error closing connection: {e}")
    
    def write_coil(self, address: int, state: bool) -> bool:
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
                address=address,
                value=state,
                slave=self.slave_id
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
    
    def read_coil(self, address: int) -> Optional[bool]:
        """
        Lire une bobine (coil).
        
        Args:
            address: Adresse de la bobine
        
        Returns:
            bool ou None: État de la bobine ou None si erreur
        """
        try:
            _LOGGER.debug(f"Reading coil {address:04X}")
            
            result = self.client.read_coils(
                address=address,
                count=1,
                slave=self.slave_id
            )
            
            if isinstance(result, ExceptionResponse):
                _LOGGER.error(f"Modbus exception: {result}")
                return None
            
            if result.isError():
                _LOGGER.error(f"Failed to read coil: {result}")
                return None
            
            state = result.bits[0] if result.bits else False
            _LOGGER.debug(f"Read coil {address:04X} = {state}")
            return state
            
        except ModbusException as e:
            _LOGGER.error(f"Modbus error: {e}")
            return None
        except Exception as e:
            _LOGGER.error(f"Unexpected error reading coil: {e}")
            return None
    
    def write_register(self, address: int, value: int) -> bool:
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
                address=address,
                value=value,
                slave=self.slave_id
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
    
    def read_register(self, address: int) -> Optional[int]:
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
                address=address,
                count=1,
                slave=self.slave_id
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
