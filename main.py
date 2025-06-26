import asyncio
from src.bot import DrMonkey
from src.core.logging import setup_logging, get_logger
from src.core.database import DatabaseManager
from src import config
# Configure logging for the application.
setup_logging(
    log_level_str=config.LOG_LEVEL,
    log_file_path=config.LOG_FILE_PATH,
    log_to_file=False
)
# Initialize the application-wide logger.
app_logger = get_logger("DrMonkey")

async def run_bot():
    """Configures, connects, and runs the bot, ensuring cleanup."""
    # Check if the Discord token is available.
    if not config.DISCORD_TOKEN:
        app_logger.critical("DISCORD_TOKEN not found in environment variables.")
        return
    
    # Initialize the database manager and configure its path.
    db_manager = DatabaseManager()
    db_manager.configure_database_path(config.DATABASE_FILE_PATH)
    
    # Create an instance of the bot.
    bot = DrMonkey(db_manager=db_manager)
    try:
        # Start the bot with the provided Discord token.
        await bot.start(config.DISCORD_TOKEN)
    finally:
        # Ensure the bot and database connection are properly closed on shutdown.
        await bot.close()
        app_logger.info("Bot has been shut down and database connection closed.")

def main():
    """Main entry point to run the asynchronous bot."""
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        app_logger.info("Bot shutdown requested by user.")

if __name__ == "__main__":
    main()