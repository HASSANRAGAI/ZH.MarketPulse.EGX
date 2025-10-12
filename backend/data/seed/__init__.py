# Seed data package - JSON fixtures for database seeding

import json
import os
from pathlib import Path
from typing import Dict, Any, List

# Seed data directory
SEED_DIR = Path(__file__).parent

def load_default_config() -> Dict[str, Any]:
    """Load default configuration from JSON file."""
    config_file = SEED_DIR / "default_config.json"
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_sample_stocks() -> List[Dict[str, Any]]:
    """Load sample stock data from JSON file."""
    stocks_file = SEED_DIR / "sample_stocks.json"
    with open(stocks_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_seed_files() -> List[str]:
    """Get list of available seed files."""
    return [f for f in os.listdir(SEED_DIR) if f.endswith('.json')]

__all__ = [
    'load_default_config',
    'load_sample_stocks',
    'get_seed_files',
    'SEED_DIR'
]