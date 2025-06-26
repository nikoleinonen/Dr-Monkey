import os
from dotenv import load_dotenv

load_dotenv()

def _parse_comma_separated_ids(ids_str: str | None) -> list[int]:
    """Helper to parse comma-separated integer IDs from a string."""
    if not ids_str:
        return []
    try:
        return [int(id_val.strip()) for id_val in ids_str.split(',') if id_val.strip().isdigit()]
    except ValueError:
        # In a real app, you'd want to log this error.
        # For now, we'll return an empty list to prevent crashes.
        print(f"Warning: Invalid non-integer value found in one of the ID lists in .env. The list will be empty.")
        return []

# --- Bot Configuration ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# --- Database ---
DATABASE_FILE_PATH = os.getenv("DATABASE_FILE_PATH", "data/bot.db")

# --- Logging ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "data/bot.log")

# --- Permissions ---
WHITELISTED_GUILD_IDS_STR = os.getenv("WHITELISTED_GUILD_IDS", "")
BOT_CHANNEL_IDS_STR = os.getenv("BOT_CHANNEL_IDS", "")

WHITELISTED_GUILD_IDS = _parse_comma_separated_ids(WHITELISTED_GUILD_IDS_STR)
BOT_CHANNEL_IDS = _parse_comma_separated_ids(BOT_CHANNEL_IDS_STR)

