#!/usr/bin/env python3
"""
ZhEaIsNsAaBn MarketPulse EGX Configuration
Centralized configuration management with JSON defaults and database overrides.
"""

import json
import os
from typing import Any, Dict, Optional
from pathlib import Path

# Import database dependencies
from .db_engine import get_session
from .custom_logging import logger, log_error_with_exception

class ConfigManager:
    """Manages configuration with JSON defaults and database overrides."""

    def __init__(self, config_file: str = None):
        self.config_file = config_file or Path(__file__).parent.parent / "data" / "seed" / "default_config.json"
        self._config_cache = None
        self._db_config_cache = None

    def _load_json_config(self) -> Dict[str, Any]:
        """Load default configuration from JSON file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_file}. Using empty defaults.")
            return {}
        except json.JSONDecodeError as e:
            log_error_with_exception("Invalid JSON in config file")
            return {}

    def _load_db_config(self) -> Dict[str, Any]:
        """Load configuration overrides from database."""
        if self._db_config_cache is not None:
            return self._db_config_cache

        db_overrides = {}
        try:
            with get_session() as session:
                from data.models import Config
                configs = session.query(Config).filter(Config.is_active == True).all()

                for config in configs:
                    # Parse nested keys like 'retry.max_attempts'
                    keys = config.key.split('.')
                    current = db_overrides

                    # Navigate/create nested structure
                    for key in keys[:-1]:
                        if key not in current:
                            current[key] = {}
                        current = current[key]

                    # Set the final value with proper type conversion
                    current[keys[-1]] = self._convert_value(config.value, config.value_type)

        except Exception as e:
            logger.warning(f"Failed to load config from database: {e}")

        self._db_config_cache = db_overrides
        return db_overrides

    def _convert_value(self, value: str, value_type: str) -> Any:
        """Convert string value to appropriate type."""
        try:
            if value_type == 'int':
                return int(value)
            elif value_type == 'float':
                return float(value)
            elif value_type == 'bool':
                return value.lower() in ('true', '1', 'yes', 'on')
            elif value_type == 'list':
                return json.loads(value)
            elif value_type == 'dict':
                return json.loads(value)
            else:  # 'str'
                return value
        except (ValueError, json.JSONDecodeError):
            logger.warning(f"Failed to convert config value '{value}' to type '{value_type}'")
            return value

    def _merge_configs(self, base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge override config into base config."""
        result = base.copy()

        for key, value in overrides.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def get_config(self, force_reload: bool = False) -> Dict[str, Any]:
        """Get the complete configuration (JSON defaults + DB overrides)."""
        if self._config_cache is None or force_reload:
            json_config = self._load_json_config()
            db_config = self._load_db_config()
            self._config_cache = self._merge_configs(json_config, db_config)

        return self._config_cache

    def get(self, key: str, default: Any = None) -> Any:
        """Get a specific configuration value by dot-notation key."""
        config = self.get_config()
        keys = key.split('.')
        current = config

        try:
            for k in keys:
                current = current[k]
            return current
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any, category: str = None, description: str = None) -> bool:
        """Set a configuration value in the database."""
        try:
            with get_session() as session:
                from data.models import Config

                # Determine value type
                if isinstance(value, bool):
                    value_type = 'bool'
                    str_value = str(value).lower()
                elif isinstance(value, int):
                    value_type = 'int'
                    str_value = str(value)
                elif isinstance(value, float):
                    value_type = 'float'
                    str_value = str(value)
                elif isinstance(value, (list, dict)):
                    value_type = 'list' if isinstance(value, list) else 'dict'
                    str_value = json.dumps(value)
                else:
                    value_type = 'str'
                    str_value = str(value)

                # Determine category if not provided
                if category is None:
                    category = key.split('.')[0] if '.' in key else 'general'

                # Update or create config entry
                config_entry = session.query(Config).filter(Config.key == key).first()
                if config_entry:
                    config_entry.value = str_value
                    config_entry.value_type = value_type
                    config_entry.category = category
                    if description:
                        config_entry.description = description
                else:
                    config_entry = Config(
                        key=key,
                        value=str_value,
                        value_type=value_type,
                        category=category,
                        description=description
                    )
                    session.add(config_entry)

                session.commit()

                # Clear cache to force reload
                self._config_cache = None
                self._db_config_cache = None

                logger.info(f"Updated config: {key} = {value}")
                return True

        except Exception as e:
            log_error_with_exception(f"Failed to set config {key}")
            return False

    def delete(self, key: str) -> bool:
        """Delete a configuration value from the database."""
        try:
            with get_session() as session:
                from data.models import Config
                config_entry = session.query(Config).filter(Config.key == key).first()
                if config_entry:
                    session.delete(config_entry)
                    session.commit()

                    # Clear cache
                    self._config_cache = None
                    self._db_config_cache = None

                    logger.info(f"Deleted config: {key}")
                    return True
                else:
                    logger.warning(f"Config key not found: {key}")
                    return False

        except Exception as e:
            log_error_with_exception(f"Failed to delete config {key}")
            return False

    def list_configs(self, category: str = None) -> Dict[str, Dict[str, Any]]:
        """List all configuration entries."""
        try:
            with get_session() as session:
                from data.models import Config
                query = session.query(Config)
                if category:
                    query = query.filter(Config.category == category)

                configs = {}
                for config in query.all():
                    configs[config.key] = {
                        'value': self._convert_value(config.value, config.value_type),
                        'type': config.value_type,
                        'category': config.category,
                        'description': config.description,
                        'updated_at': config.updated_at
                    }

                return configs

        except Exception as e:
            log_error_with_exception("Failed to list configs")
            return {}

    def reload(self):
        """Force reload of configuration from sources."""
        self._config_cache = None
        self._db_config_cache = None
        logger.info("Configuration reloaded")

# Global config manager instance
config_manager = ConfigManager()

# Backward compatibility functions
def get_config():
    """Get the main configuration dictionary (backward compatibility)."""
    return config_manager.get_config()

def get_field_mappings(language='english'):
    """Get field mappings for specified language (placeholder)."""
    # This would need to be implemented based on your field mapping needs
    return {}

def update_retry_config(max_attempts=None, base_delay=None):
    """Update retry configuration dynamically (backward compatibility)."""
    if max_attempts is not None:
        config_manager.set('retry.max_attempts', max_attempts, 'retry', 'Maximum retry attempts')
    if base_delay is not None:
        config_manager.set('retry.base_delay', base_delay, 'retry', 'Base delay between retries')

def display_retry_info():
    """Display retry configuration information (backward compatibility)."""
    retry_config = config_manager.get('retry', {})
    print("\n🔄 Smart Retry Configuration:")
    print(f"   - Max attempts: {retry_config.get('max_attempts', 'N/A')}")
    print(f"   - Base delay: {retry_config.get('base_delay', 'N/A')}s")
    print(f"   - Max delay: {retry_config.get('max_delay', 'N/A')}s")
    print(f"   - Backoff factor: {retry_config.get('backoff_factor', 'N/A')}")
    print()

# Convenience access to config
CONFIG = config_manager.get_config()