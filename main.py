import asyncio
from src.bot import DrMonkey
from src.core.logging import setup_logging, get_logger
from src.core.database import DatabaseManager # Import the class
from src import config

setup_logging(
    log_level_str=config.LOG_LEVEL,
    log_to_file=True,
    log_file_path=config.LOG_FILE_PATH
)
app_logger = get_logger("DrMonkey")

async def run_bot():
    """Configures, connects, and runs the bot, ensuring cleanup."""
    if not config.DISCORD_TOKEN:
        app_logger.critical("DISCORD_TOKEN not found in environment variables.")
        return

    db_manager = DatabaseManager() # Instantiate the manager
    db_manager.configure_database_path(config.DATABASE_FILE_PATH)
    db_manager.connect_database()

    bot = DrMonkey(db_manager=db_manager) # Pass the manager to the bot
    try:
        await bot.start(config.DISCORD_TOKEN)
    finally:
        await bot.close()
        db_manager.close_database() # Close connection via manager
        app_logger.info("Bot has been shut down and database connection closed.")

def main():
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        app_logger.info("Bot shutdown requested by user.")

if __name__ == "__main__":
    main()