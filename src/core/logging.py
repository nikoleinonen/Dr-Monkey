import logging
import sys
import os

def setup_logging(log_level_str: str, log_to_file: bool, log_file_path: str) -> None:
    """Configures the application's logging system."""
    # Convert string log level to logging module's constant.
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    
    # Always add a stream handler for console output.
    handlers = [logging.StreamHandler(sys.stdout)]
    # Add a file handler if logging to file is enabled.
    if log_to_file:
        log_dir = os.path.dirname(log_file_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        handlers.append(logging.FileHandler(log_file_path))
    
    # Configure the basic logging setup.
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=handlers
    )

def get_logger(name: str) -> logging.Logger:
    """Returns a logger instance with the specified name."""
    return logging.getLogger(name)
