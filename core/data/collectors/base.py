from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseCollector(ABC):
    """
    Abstract base class for all data collectors.
    Defines the interface that all collectors must implement.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the collector with configuration.
        
        Args:
            config: Dictionary containing collector configuration
        """
        self.config = config
        self.is_running = False

    @abstractmethod
    async def connect(self) -> bool:
        """
        Establish connection to the data source.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """
        Close connection to the data source.
        
        Returns:
            bool: True if disconnection successful, False otherwise
        """
        pass

    @abstractmethod
    async def collect(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Collect data from the source.
        
        Args:
            params: Optional parameters for data collection
            
        Returns:
            List of collected data items
        """
        pass

    @abstractmethod
    async def validate(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate collected data.
        
        Args:
            data: List of collected data items
            
        Returns:
            List of validated data items
        """
        pass 