import logging
import sys
import os

def setup_logging(log_level_str: str, log_to_file: bool, log_file_path: str) -> None:
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)

    handlers = [logging.StreamHandler(sys.stdout)]

    if log_to_file:
        log_dir = os.path.dirname(log_file_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        handlers.append(logging.FileHandler(log_file_path))

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=handlers
    )

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
