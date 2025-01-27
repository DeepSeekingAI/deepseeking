from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod

class DeepSeekBase(ABC):
    """
    Base interface for DeepSeek AI integration.
    Provides standardized access to DeepSeek's multimodal capabilities.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize DeepSeek interface.
        
        Args:
            config: Configuration containing API keys and model settings
        """
        self.config = config
        self.api_key = config.get("api_key")
        self.model_version = config.get("model_version", "latest")
        self.base_url = config.get("base_url", "https://api.deepseek.ai/v1")

    @abstractmethod
    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text using DeepSeek's NLP capabilities.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Analysis results including sentiment, entities, etc.
        """
        pass

    @abstractmethod
    async def analyze_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        Analyze image using DeepSeek's computer vision capabilities.
        
        Args:
            image_data: Raw image data
            
        Returns:
            Analysis results including objects, features, etc.
        """
        pass

    @abstractmethod
    async def multimodal_analysis(
        self, 
        text: Optional[str] = None,
        image: Optional[bytes] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform multimodal analysis combining text and image data.
        
        Args:
            text: Optional text input
            image: Optional image data
            context: Additional context for analysis
            
        Returns:
            Combined analysis results
        """
        pass

    @abstractmethod
    async def generate_prediction(
        self,
        data: Dict[str, Any],
        prediction_type: str,
        confidence_threshold: float = 0.8
    ) -> Dict[str, Any]:
        """
        Generate predictions using DeepSeek models.
        
        Args:
            data: Input data for prediction
            prediction_type: Type of prediction to make
            confidence_threshold: Minimum confidence threshold
            
        Returns:
            Prediction results with confidence scores
        """
        pass

    @abstractmethod
    async def detect_anomalies(
        self,
        data: Union[List[Dict[str, Any]], Dict[str, Any]],
        detection_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Detect anomalies in data using DeepSeek's AI.
        
        Args:
            data: Input data to analyze
            detection_config: Configuration for anomaly detection
            
        Returns:
            Detected anomalies with severity scores
        """
        pass

    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about available DeepSeek models.
        
        Returns:
            Model information including versions and capabilities
        """
        pass 