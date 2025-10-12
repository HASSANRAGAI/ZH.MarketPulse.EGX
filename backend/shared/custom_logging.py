from loguru import logger;
from functools import wraps
from loguru import logger
import time
from functools import wraps
import sys
import traceback

# Configure the logger globally
logger.remove()  # Clear default handlers
logger.add("logs/app_{time}.log", rotation="50 MB", retention="2 days", compression="zip", level="DEBUG")
logger.add(lambda msg: print(msg, end=""), colorize=True, level="INFO")

def log_error_with_exception(message: str = "An error occurred", level: str = "ERROR"):
    """
    Log an error with detailed exception information including traceback, file, and line number.

    Args:
        message: Custom error message to log
        level: Log level (ERROR, WARNING, etc.)
    """
    exc_type, exc_value, exc_tb = sys.exc_info()

    if exc_tb is not None:
        frame = traceback.extract_tb(exc_tb)[-1]  # Last frame is the exception spot
        line_number = frame.lineno
        file_name = frame.filename

        # Log the error with detailed exception information
        logger.log(level, f"{message} | Exception: {exc_type.__name__}: {exc_value} | File: {file_name}:{line_number}")
    else:
        # Fallback if no exception info is available
        logger.log(level, message)

def time_method(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        logger.info(f"Starting {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time
        logger.info(f"Finished {func.__name__} in {duration:.4f} seconds")
        return result
    return wrapper
