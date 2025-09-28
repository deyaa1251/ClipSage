"""
Configuration management for ClipSage
"""

import os
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
import json


class Config:
    """Configuration manager for ClipSage application"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or self._get_default_config_path()
        self._config: Dict[str, Any] = {}
        self.load_config()
    
    @staticmethod
    def _get_default_config_path() -> str:
        """Get the default configuration file path"""
        config_dir = Path.home() / ".config" / "clipsage"
        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir / "config.json")
    
    def load_config(self) -> None:
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}")
                self._config = {}
        
        # Set defaults
        self._set_defaults()
    
    def save_config(self) -> None:
        """Save configuration to file"""
        try:
            config_dir = Path(self.config_file).parent
            config_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def _set_defaults(self) -> None:
        """Set default configuration values"""
        defaults = {
            "clipboard_path": str(Path(tempfile.gettempdir()) /
                                  "clipboard_manager"),
            "embedding_model": "all-minilm:22m",
            "max_items": 1000,
            "refresh_interval": 5000,  # milliseconds
            "auto_refresh": True,
            "window": {
                "width": 1200,
                "height": 800,
                "x": 100,
                "y": 100
            },
            "search": {
                "max_results": 10,
                "enable_semantic": True
            },
            "ui": {
                "theme": "light",
                "font_size": 12,
                "show_preview": True
            }
        }
        
        for key, value in defaults.items():
            if key not in self._config:
                self._config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        keys = key.split('.')
        config = self._config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    @property
    def clipboard_path(self) -> Path:
        """Get clipboard storage path"""
        return Path(self.get("clipboard_path"))
    
    @property
    def embedding_model(self) -> str:
        """Get embedding model name"""
        return self.get("embedding_model", "all-minilm:22m")
    
    @property
    def max_items(self) -> int:
        """Get maximum number of clipboard items"""
        return self.get("max_items", 1000)
    
    @property
    def refresh_interval(self) -> int:
        """Get refresh interval in milliseconds"""
        return self.get("refresh_interval", 5000)


# Global config instance
config = Config()