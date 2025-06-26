import os
from dotenv import load_dotenv
from src.core.logging import get_logger
# Load environment variables from .env file.
load_dotenv()
# Initialize logger for configuration.
logger = get_logger("Config")

def _parse_comma_separated_ids(ids_str: str | None) -> list[int]:
    """Parses a comma-separated string of IDs into a list of integers."""
    if not ids_str:
        return []
    try:
        return [int(id_val.strip()) for id_val in ids_str.split(',') if id_val.strip().isdigit()]
    except ValueError:
        # Log a warning if non-integer values are found.
        logger.warning("Invalid non-integer value found in one of the ID lists in .env. The list will be empty.")
        return []

# --- Bot Configuration ---
# Discord bot token.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# --- Database ---
# Path to the SQLite database file.
DATABASE_FILE_PATH = os.getenv("DATABASE_FILE_PATH", "data/bot.db")

# --- Logging ---
# Minimum logging level.
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
# Path for log file.
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "data/bot.log")

# --- Permissions ---
# Raw string of whitelisted guild IDs from environment.
WHITELISTED_GUILD_IDS_STR = os.getenv("WHITELISTED_GUILD_IDS", "")
# Raw string of bot channel IDs from environment.
BOT_CHANNEL_IDS_STR = os.getenv("BOT_CHANNEL_IDS", "")
# Parsed list of whitelisted guild IDs.
WHITELISTED_GUILD_IDS = _parse_comma_separated_ids(WHITELISTED_GUILD_IDS_STR)
# Parsed list of bot channel IDs.
BOT_CHANNEL_IDS = _parse_comma_separated_ids(BOT_CHANNEL_IDS_STR)
