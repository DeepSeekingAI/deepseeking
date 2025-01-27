from typing import Any, Dict, Optional
import os
import yaml
from pathlib import Path

class Config:
    """
    Configuration management system for DeepSeeking framework.
    Handles loading and validation of configuration from various sources.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Optional path to config file
        """
        self.config: Dict[str, Any] = {}
        self._load_defaults()
        
        if config_path:
            self.load_from_file(config_path)
        
        self._load_from_env()
        self._validate_config()

    def _load_defaults(self):
        """Load default configuration values."""
        self.config = {
            "deepseek": {
                "api": {
                    "base_url": "https://api.deepseek.ai/v1",
                    "timeout": 30,
                },
                "models": {
                    "text": {
                        "version": "latest",
                        "batch_size": 32,
                    },
                    "vision": {
                        "version": "latest",
                        "image_size": 512,
                    },
                    "multimodal": {
                        "version": "latest",
                        "max_text_length": 1024,
                        "max_image_size": 1024,
                    },
                },
            },
            "blockchain": {
                "networks": {
                    "ethereum": {
                        "chain_id": 1,
                    },
                    "polygon": {
                        "chain_id": 137,
                    },
                },
                "contracts": {
                    "prediction_market": {
                        "version": "1.0",
                    },
                    "insurance_pool": {
                        "version": "1.0",
                    },
                },
            },
            "data": {
                "collectors": {
                    "max_retries": 3,
                    "timeout": 10,
                },
                "storage": {
                    "retention_days": 30,
                    "compression": True,
                },
            },
            "services": {
                "prediction": {
                    "update_interval": 60,
                },
                "hedging": {
                    "risk_threshold": 0.8,
                },
                "alert": {
                    "notification_delay": 5,
                },
            },
        }

    def load_from_file(self, path: str):
        """
        Load configuration from YAML file.
        
        Args:
            path: Path to configuration file
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
            
        with open(path) as f:
            file_config = yaml.safe_load(f)
            self._merge_config(file_config)

    def _load_from_env(self):
        """Load configuration from environment variables."""
        # DeepSeek API key
        if api_key := os.getenv("DEEPSEEK_API_KEY"):
            self.config["deepseek"]["api"]["key"] = api_key
            
        # Blockchain RPC URLs
        if eth_rpc := os.getenv("ETH_RPC_URL"):
            self.config["blockchain"]["networks"]["ethereum"]["rpc_url"] = eth_rpc
        if poly_rpc := os.getenv("POLYGON_RPC_URL"):
            self.config["blockchain"]["networks"]["polygon"]["rpc_url"] = poly_rpc

    def _merge_config(self, new_config: Dict[str, Any]):
        """
        Merge new configuration with existing.
        
        Args:
            new_config: New configuration to merge
        """
        def merge_dict(base: Dict[str, Any], update: Dict[str, Any]):
            for k, v in update.items():
                if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                    merge_dict(base[k], v)
                else:
                    base[k] = v
                    
        merge_dict(self.config, new_config)

    def _validate_config(self):
        """Validate configuration values."""
        required_keys = [
            ("deepseek.api.key", "DEEPSEEK_API_KEY environment variable not set"),
            ("blockchain.networks.ethereum.rpc_url", "ETH_RPC_URL environment variable not set"),
        ]
        
        for key_path, error_msg in required_keys:
            if not self.get_nested(key_path):
                raise ValueError(error_msg)

    def get_nested(self, key_path: str) -> Any:
        """
        Get nested configuration value using dot notation.
        
        Args:
            key_path: Configuration key path (e.g. "deepseek.api.key")
            
        Returns:
            Configuration value
        """
        value = self.config
        for key in key_path.split("."):
            try:
                value = value[key]
            except (KeyError, TypeError):
                return None
        return value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value 