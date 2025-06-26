import asyncio
from src.bot import DrMonkey
from src.core.logging import setup_logging, get_logger
from src.core import database
from src import config

setup_logging(
    log_level_str=config.LOG_LEVEL,
    log_to_file=True, # Assuming we always want to log to file if path is provided
    log_file_path=config.LOG_FILE_PATH
)
app_logger = get_logger("DrMonkey")

async def run_bot():
    """Configures, connects, and runs the bot, ensuring cleanup."""
    if not config.DISCORD_TOKEN:
        app_logger.critical("DISCORD_TOKEN not found in environment variables.")
        return

    database.configure_database_path(config.DATABASE_FILE_PATH)
    database.connect_database()

    bot = DrMonkey()
    try:
        await bot.start(config.DISCORD_TOKEN)
    finally:
        await bot.close()
        database.close_database()
        app_logger.info("Bot has been shut down and database connection closed.")

def main():
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        app_logger.info("Bot shutdown requested by user.")

if __name__ == "__main__":
    main()