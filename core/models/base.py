from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import torch

class BaseModel(ABC):
    """
    Abstract base class for all AI models in the system.
    Defines the interface that all models must implement.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the model with configuration.
        
        Args:
            config: Dictionary containing model configuration
        """
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None

    @abstractmethod
    async def load(self) -> bool:
        """
        Load the model and its weights.
        
        Returns:
            bool: True if loading successful, False otherwise
        """
        pass

    @abstractmethod
    async def predict(self, inputs: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Make predictions using the model.
        
        Args:
            inputs: Input data for prediction
            
        Returns:
            Dictionary containing prediction results
        """
        pass

    @abstractmethod
    async def validate(self, data: Dict[str, Any]) -> bool:
        """
        Validate input data format.
        
        Args:
            data: Input data to validate
            
        Returns:
            True if validation passes, False otherwise
        """
        pass

    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the model.
        
        Returns:
            Dictionary containing model metadata
        """
        pass

    @abstractmethod
    async def save_checkpoint(self, path: str) -> bool:
        """
        Save model checkpoint.
        
        Args:
            path: Path to save the checkpoint
            
        Returns:
            True if saving successful, False otherwise
        """
        pass 