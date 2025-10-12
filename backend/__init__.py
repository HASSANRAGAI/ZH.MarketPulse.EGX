# Backend package for ZH.MarketPulse.EGX

# Import main pipeline components
from .shared import config_manager, db_engine, logging
from .collector import stock_collector

# Version info
__version__ = "1.0.0"
__author__ = "ZhEaIsNsAaBn"

# Main pipeline entry point (when main.py is implemented)
def run_pipeline():
    """Run the complete data pipeline: collect → sanitize → train"""
    # This will be implemented when the pipeline modules are created
    pass

__all__ = [
    'config_manager',
    'db_engine',
    'logging',
    'stock_collector',
    'run_pipeline'
]