from dotenv import load_dotenv
import discord
from discord.ext import commands
import os
import asyncio
from src.logging_config import setup_logging, get_logger
import src.database_manager

load_dotenv()
DATABASE_FILE_PATH = os.getenv("DATABASE_FILE_PATH")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
WHITELISTED_GUILD_IDS_STR = os.getenv("WHITELISTED_GUILD_IDS", "")
BOT_CHANNEL_IDS_STR = os.getenv("BOT_CHANNEL_IDS", "")

setup_logging(log_level_str="DEBUG")
app_logger = get_logger("DrMonkey")

intents = discord.Intents.default()
intents.members = True

class DrMonkey(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=intents)
        self.bot_channel_ids = self._parse_comma_separated_ids(BOT_CHANNEL_IDS_STR, "Bot Channel")
        self._one_time_setup_done = False
        self.tree.on_error = self.on_app_command_error

    async def on_app_command_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        """Global error handler for all application commands."""
        if isinstance(error, discord.app_commands.CheckFailure):
            # This error is raised when a check fails. The check itself should have
            # The default behavior logs this as an ERROR, which is what we want to avoid.
            app_logger.info(
                f"Command '{interaction.command.name}' check failed for user {interaction.user.id} "
                f"in channel {interaction.channel.id}. This is expected for permission checks."
            )
        elif isinstance(error, discord.app_commands.CommandOnCooldown):
            # Handle cooldowns gracefully
            await interaction.response.send_message(
                f"You're on cooldown! Please try again in {error.retry_after:.2f} seconds.",
                ephemeral=True
            )
        else:
            # For any other errors, we log them as an error and notify the user.
            app_logger.error(f"An unhandled exception occurred in command '{interaction.command.name}':", exc_info=error)

            # Try to send a generic error message
            error_message = "An unexpected error occurred. The developers have been notified. (LOL not)"
            if interaction.response.is_done():
                await interaction.followup.send(error_message, ephemeral=True)
            else:
                await interaction.response.send_message(error_message, ephemeral=True)

    def _parse_comma_separated_ids(self, ids_str: str, category_name: str) -> list[int]:
        """Helper to parse comma-separated integer IDs from a string."""
        if not ids_str:
            app_logger.info(f"No IDs configured for {category_name}.")
            return []
        try:
            return [int(id_val.strip()) for id_val in ids_str.split(',') if id_val.strip().isdigit()]
        except ValueError:
            app_logger.error(f"Invalid non-integer value found for {category_name} IDs. Please check your .env file. No restrictions will be applied for {category_name} due to this error.")
            return [] # Return empty list on error to effectively disable restriction

    async def check_guild(self, interaction: discord.Interaction) -> bool:
        """
        Checks if the interaction's guild is whitelisted.
        This is now a method of the DrMonkey class.
        """
        if interaction.guild is None or interaction.guild.id in self.whitelisted_servers:
            return True
        else:
            app_logger.info(f"Command attempt in non-whitelisted guild: {interaction.guild.name} (ID: {interaction.guild.id}).")
            await interaction.response.send_message("This bot is not enabled in this server.", ephemeral=True)
            return False

    def _load_server_whitelist(self) -> list[int]:
        """
        Loads the server whitelist exclusively from the WHITELISTED_GUILD_IDS environment variable.
        """
        if not WHITELISTED_GUILD_IDS_STR:
            app_logger.warning("WHITELISTED_GUILD_IDS environment variable not set. No servers will be whitelisted.")
            return []

        try:
            server_ids = [int(guild_id.strip()) for guild_id in WHITELISTED_GUILD_IDS_STR.split(',') if guild_id.strip().isdigit()]
            if server_ids:
                app_logger.info(f"Loaded server whitelist from WHITELISTED_GUILD_IDS environment variable: {server_ids}")
                return server_ids
            else:
                app_logger.warning("WHITELISTED_GUILD_IDS is set but empty or contains no valid IDs. No servers will be whitelisted.")
                return []
        except ValueError:
            app_logger.error("Invalid non-integer value in WHITELISTED_GUILD_IDS. No servers will be whitelisted due to this error.")
            return []

    async def setup_hook(self) -> None:
        # Database initialization always runs, as it's a single bot instance for all guilds.
        src.database_manager.configure_database_path(DATABASE_FILE_PATH)
        app_logger.info(f"Attempting to initialize database")
        src.database_manager.initialize_database()

        # Load server whitelist before commands are loaded to ensure checks can be applied
        self.whitelisted_servers = self._load_server_whitelist()
        if not self.whitelisted_servers:
            app_logger.warning("No servers whitelisted! The bot will not respond to commands in any server.")
        else:
            app_logger.info(f"Server whitelist loaded. The bot will only respond in guilds: {self.whitelisted_servers}")

        cogs_to_load = [
            "src.commands.analyze",
            "src.commands.monkeyoff",
            "src.commands.ranks",
        ]

        for cog_path in cogs_to_load:
            try:
                await self.load_extension(cog_path)
            except Exception:
                app_logger.error(f"Failed to load '{cog_path}' cog.", exc_info=True)

        # Sync commands. Global commands are synced first, then guild-specific ones.
        try:
            # Sync global commands
            synced_global = await self.tree.sync()
            app_logger.info(f"Synced {len(synced_global)} global application commands.")
        except Exception as e:
            app_logger.error("Failed to sync global application commands.", exc_info=True)

    async def on_ready(self) -> None:
        # --- Set custom bot status ---
        activity = discord.CustomActivity(name="🍌🍌🍌🍌🍌")
        await self.change_presence(status=discord.Status.online, activity=activity)

        # --- Run one-time setup tasks that require the bot to be connected ---
        if not self._one_time_setup_done:
            app_logger.info("Bot is ready, running one-time setup tasks...")

            self._one_time_setup_done = True
            app_logger.info("One-time setup tasks complete.")
        
        app_logger.info(f'Logged in as {self.user.name} (ID: {self.user.id})')
        app_logger.warning('Bot is ready and online!')

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        app_logger.critical("DISCORD_TOKEN not found in environment variables.")
        exit(1)

    bot = DrMonkey()
    asyncio.run(bot.start(DISCORD_TOKEN))