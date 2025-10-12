#!/usr/bin/env python3
"""
Database Initialization Script
Handles database setup and seeding for the ZhEaIsNsAaBn MarketPulse EGX application.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from shared.db_engine import create_tables, check_connection, get_session
from shared.custom_logging import logger, log_error_with_exception
from data.models import Stock, Config

class DatabaseInitializer:
    """Handles database initialization and seeding."""

    def __init__(self):
        self.fixtures_dir = Path(__file__).parent.parent / "data" / "seed"
        self.initialized = False

    def is_database_empty(self) -> bool:
        """Check if the database has any tables."""
        try:
            with get_session() as session:
                # Try to query the stock table (one of our main tables)
                result = session.query(Stock).limit(1).all()
                return len(result) == 0
        except Exception:
            # If query fails, database might not be set up yet
            return True

    def create_database_schema(self) -> bool:
        """Create all database tables."""
        try:
            logger.info("Creating database schema...")
            create_tables()
            logger.info("✅ Database schema created successfully")
            return True
        except Exception as e:
            log_error_with_exception("❌ Failed to create database schema")
            return False

    def seed_config_data(self) -> bool:
        """Seed default configuration data from JSON."""
        try:
            config_file = self.fixtures_dir / "default_config.json"
            if not config_file.exists():
                logger.warning(f"Config file not found: {config_file}")
                return True  # Not a fatal error

            logger.info("Seeding configuration data...")

            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            # Flatten nested config to dot notation
            flat_configs = self._flatten_config(config_data)

            with get_session() as session:
                for key, value in flat_configs.items():
                    # Skip if config already exists
                    existing = session.query(Config).filter(Config.key == key).first()
                    if existing:
                        continue

                    # Determine category and type
                    category = key.split('.')[0] if '.' in key else 'general'
                    value_type = self._get_value_type(value)

                    # Convert value to string for storage
                    if isinstance(value, (list, dict)):
                        str_value = json.dumps(value)
                        value_type = 'list' if isinstance(value, list) else 'dict'
                    else:
                        str_value = str(value)

                    config_entry = Config(
                        key=key,
                        value=str_value,
                        value_type=value_type,
                        category=category,
                        description=f"Default {category} configuration"
                    )
                    session.add(config_entry)

                session.commit()

            logger.info("✅ Configuration data seeded successfully")
            return True

        except Exception as e:
            log_error_with_exception("❌ Failed to seed configuration data")
            return False


    def _flatten_config(self, config: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        """Flatten nested config dictionary to dot notation."""
        flat = {}
        for key, value in config.items():
            full_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                flat.update(self._flatten_config(value, full_key))
            else:
                flat[full_key] = value

        return flat

    def _get_value_type(self, value: Any) -> str:
        """Determine the type of a value for database storage."""
        if isinstance(value, bool):
            return 'bool'
        elif isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, list):
            return 'list'
        elif isinstance(value, dict):
            return 'dict'
        else:
            return 'str'

    def initialize_database(self, force: bool = False) -> bool:
        """Main initialization method."""
        logger.info("🚀 Starting database initialization...")

        # Check database connection
        if not check_connection():
            log_error_with_exception("❌ Cannot connect to database. Please check your DATABASE_URL.")
            return False

        # Check if database needs initialization
        if not force and not self.is_database_empty():
            logger.info("ℹ️ Database already initialized. Use --force to re-initialize.")
            self.initialized = True
            return True

        # Create schema
        if not self.create_database_schema():
            return False

        # Seed configuration data
        if not self.seed_config_data():
            return False


        self.initialized = True
        logger.info("🎉 Database initialization completed successfully!")
        return True

def main():
    """Command-line interface for database initialization."""
    import argparse

    parser = argparse.ArgumentParser(description="Initialize the MarketPulse EGX database")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-initialization even if database is not empty"
    )
    parser.add_argument(
        "--config-only",
        action="store_true",
        help="Only seed configuration data, skip sample data"
    )

    args = parser.parse_args()

    initializer = DatabaseInitializer()

    if args.config_only:
        # Only seed config data
        logger.info("Seeding configuration data only...")
        success = (
            check_connection() and
            initializer.create_database_schema() and
            initializer.seed_config_data()
        )
    else:
        # Full initialization
        success = initializer.initialize_database(force=args.force)

    if success:
        logger.info("✅ Database initialization completed successfully!")
        sys.exit(0)
    else:
        log_error_with_exception("❌ Database initialization failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()