import asyncio
from src.bot import DrMonkey
from src.core.logging import setup_logging, get_logger
from src.core import database
from src import config

setup_logging(log_level_str=config.LOG_LEVEL)
app_logger = get_logger("DrMonkey")

def main():
    if not config.DISCORD_TOKEN:
        app_logger.critical("DISCORD_TOKEN not found in environment variables.")
        return

    database.configure_database_path(config.DATABASE_FILE_PATH)

    bot = DrMonkey()
    asyncio.run(bot.start(config.DISCORD_TOKEN))

if __name__ == "__main__":
    main()