#!/usr/bin/env python3
"""
Retry Utilities Module
Contains the smart retry mechanism using tenacity with exponential backoff.
"""

import time
import random
from functools import wraps
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .config_manager import CONFIG
from .custom_logging import logger, time_method, log_error_with_exception



def smart_retry(operation_name="operation"):
    """
    Smart retry decorator using tenacity with exponential backoff and jitter.

    Args:
        operation_name: Name of the operation for logging purposes
    """
    def decorator(func):
        @wraps(func)
        @time_method
        @retry(
            stop=stop_after_attempt(CONFIG['retry']['max_attempts']),
            wait=wait_exponential(
                multiplier=CONFIG['retry']['base_delay'],
                max=CONFIG['retry']['max_delay'],
                exp_base=CONFIG['retry']['backoff_factor']
            ),
            retry=retry_if_exception_type(tuple(CONFIG['retry']['retryable_exceptions'])),
            before_sleep=lambda retry_state: (
                logger.warning(
                    f"⚠️ {operation_name} failed (attempt {retry_state.attempt_number}/{CONFIG['retry']['max_attempts']}): {retry_state.outcome.exception()}"
                ),
                logger.info(
                    f"⏳ Retrying {operation_name} in {retry_state.next_action.sleep:.1f} seconds..."
                )
            )[0]  # Execute both logging statements
        )
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except tuple(CONFIG['retry']['non_retryable_exceptions']) as e:
                # Don't retry these exceptions
                log_error_with_exception(f"❌ {operation_name} failed with non-retryable error")
                raise
            except Exception as e:
                # For unexpected exceptions, log and re-raise (tenacity won't retry them since they're not in retryable_exceptions)
                log_error_with_exception(f"❌ {operation_name} failed with unexpected error")
                raise

        return wrapper
    return decorator