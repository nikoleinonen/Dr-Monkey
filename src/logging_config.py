import logging
import sys
import os

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FILE_PATH = "data/bot.log"

def setup_logging(log_level_str: str | None = None, log_to_file: bool = False, log_file_path: str = DEFAULT_LOG_FILE_PATH) -> None:
    if log_level_str is None:
        log_level_str = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)
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
