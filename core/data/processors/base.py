from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseProcessor(ABC):
    """
    Abstract base class for all data processors.
    Defines the interface for data processing pipeline components.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the processor with configuration.
        
        Args:
            config: Dictionary containing processor configuration
        """
        self.config = config

    @abstractmethod
    async def process(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process the input data.
        
        Args:
            data: List of data items to process
            
        Returns:
            List of processed data items
        """
        pass

    @abstractmethod
    async def validate_output(self, data: List[Dict[str, Any]]) -> bool:
        """
        Validate the processed output.
        
        Args:
            data: List of processed data items
            
        Returns:
            True if validation passes, False otherwise
        """
        pass

    @abstractmethod
    async def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the processor.
        
        Returns:
            Dictionary containing processor metadata
        """
        pass 