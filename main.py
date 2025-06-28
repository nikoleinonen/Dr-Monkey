import asyncio
from aiohttp import web
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

async def download_db_handler(request: web.Request) -> web.Response:
    """Handles requests to download the database file."""
    # Check for secret key in query parameters
    secret = request.query.get("secret")
    if not secret or secret != config.DOWNLOAD_SECRET:
        app_logger.warning("Unauthorized attempt to download database.")
        return web.Response(text="Unauthorized", status=403)

    db_path = config.DATABASE_FILE_PATH
    if not db_path:
        app_logger.error("DATABASE_FILE_PATH is not configured. Cannot serve download.")
        return web.Response(text="Database path not configured on server.", status=500)

    try:
        app_logger.info(f"Authorized database download request received. Serving file from {db_path}")
        return web.FileResponse(path=db_path, headers={
            "CONTENT-DISPOSITION": "attachment; filename=\"dr_monkey_backup.db\""
        })
    except FileNotFoundError:
        app_logger.error(f"Database file not found at configured path: {db_path}")
        return web.Response(text="Database file not found on server.", status=404)
    except Exception as e:
        app_logger.error(f"An error occurred during database download: {e}", exc_info=True)
        return web.Response(text="An internal server error occurred.", status=500)

async def run_bot():
    """Configures, connects, and runs the bot and web server, ensuring cleanup."""
    # Check if the Discord token is available.
    if not config.DISCORD_TOKEN:
        app_logger.critical("DISCORD_TOKEN not found in environment variables.")
        return
    
    if not config.DOWNLOAD_SECRET:
        app_logger.warning("DOWNLOAD_SECRET is not set. The database download endpoint will be disabled.")

    # Initialize the database manager and configure its path.
    db_manager = DatabaseManager()
    db_manager.configure_database_path(config.DATABASE_FILE_PATH)
    
    # Create an instance of the bot.
    bot = DrMonkey(db_manager=db_manager)

    # --- Setup aiohttp web server ---
    app = web.Application()
    if config.DOWNLOAD_SECRET:
        app.router.add_get("/download-db", download_db_handler)
        app_logger.info("Database download endpoint is enabled at /download-db")

    runner = web.AppRunner(app)
    await runner.setup()
    # Railway provides the PORT env var. We listen on 0.0.0.0 to be accessible.
    site = web.TCPSite(runner, '0.0.0.0', config.WEB_SERVER_PORT)
    await site.start()
    app_logger.info(f"Web server started on 0.0.0.0:{config.WEB_SERVER_PORT}")

    try:
        # Start the bot with the provided Discord token.
        await bot.start(config.DISCORD_TOKEN)
    finally:
        # Ensure the bot, web server, and database connection are properly closed on shutdown.
        await bot.close()
        await runner.cleanup() # Gracefully shut down the web server
        app_logger.info("Bot has been shut down and database connection closed.")

def main():
    """Main entry point to run the asynchronous bot."""
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        app_logger.info("Bot shutdown requested by user.")

if __name__ == "__main__":
    main()