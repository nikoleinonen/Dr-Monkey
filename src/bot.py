import discord
from discord.ext import commands
from discord import app_commands
from src.core.database import DatabaseManager
from src.core.logging import get_logger
from src import config
from src.core import constants
# Initialize the logger for the bot.
app_logger = get_logger("DrMonkeyBot")

# Configure Discord intents for the bot.
intents = discord.Intents.default()
intents.members = True

class DrMonkey(commands.Bot):
    """Custom Discord bot class with database integration and error handling."""
    def __init__(self, db_manager: DatabaseManager) -> None:
        # Initialize the base commands.Bot class.
        super().__init__(command_prefix="!", intents=intents)
        # Store the database manager instance.
        self.db_manager = db_manager
        self.bot_channel_ids = config.BOT_CHANNEL_IDS
        self.whitelisted_servers = config.WHITELISTED_GUILD_IDS
        self.tree.on_error = self.on_app_command_error

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Global error handler for all application commands."""
        if isinstance(error, app_commands.CheckFailure):
            # Log check failures as info, as they are often expected (e.g., permission issues).
            app_logger.info(
                f"Command '{interaction.command.name}' check failed for user {interaction.user.id} "
                f"in channel {interaction.channel.id}. This is expected for permission checks."
            )
        elif isinstance(error, app_commands.CommandOnCooldown):
            # Inform the user if a command is on cooldown.
            await interaction.response.send_message(
                constants.DEFAULT_COOLDOWN_MESSAGE.format(retry_after=error.retry_after),
                ephemeral=True
            )
        else:
            # Log unhandled exceptions and send a generic error message to the user.
            app_logger.error(f"An unhandled exception occurred in command '{interaction.command.name}':", exc_info=error)

            # Try to send a generic error message
            error_message = constants.GENERIC_ERROR_MESSAGE
            try:
                if interaction.response.is_done():
                    await interaction.followup.send(error_message, ephemeral=True)
                else:
                    await interaction.response.send_message(error_message, ephemeral=True)
            except discord.HTTPException:
                app_logger.error("Failed to send error message to user.")

    async def check_guild(self, interaction: discord.Interaction) -> bool:
        """Checks if the interaction is in a whitelisted guild. Rejects DM interactions."""
        # Commands using this check are intended for guilds only.
        if interaction.guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return False
        
        # If no whitelisted servers are configured, allow the command.
        if not self.whitelisted_servers:
            app_logger.warning("WHITELISTED_GUILD_IDS is not set. Allowing command as no restrictions are configured.")
            return True
        
        # Check if the guild ID is in the whitelist.
        if interaction.guild.id in self.whitelisted_servers:
            return True
        else:
            # Inform the user if the bot is not enabled in their server.
            app_logger.info(f"Command attempt in non-whitelisted guild: {interaction.guild.name} (ID: {interaction.guild.id}).")
            await interaction.response.send_message("This bot is not enabled in this server.", ephemeral=True)
            return False

    async def setup_hook(self) -> None:
        """Performs setup tasks before the bot connects to Discord."""
        app_logger.info("Running setup_hook...")
        # Initialize the database tables.
        self.db_manager.initialize_database()
        
        # Log the status of the server whitelist.
        if not self.whitelisted_servers:
            app_logger.warning("No servers whitelisted! The bot will not respond to commands in any server.")
        else:
            app_logger.info(f"Server whitelist loaded. The bot will only respond in guilds: {self.whitelisted_servers}")
        
        # Define paths for cogs to load.
        cogs_to_load = [
            "src.cogs.analyze",
            "src.cogs.monkeyoff",
            "src.cogs.ranks",
        ]
        
        # Load each cog and log success or failure.
        for cog_path in cogs_to_load:
            try:
                await self.load_extension(cog_path)
                app_logger.info(f"Successfully loaded cog: {cog_path}")
            except Exception as e:
                app_logger.error(f"Failed to load '{cog_path}' cog.", exc_info=e)

        # Sync application commands with Discord.
        synced = await self.tree.sync()
        app_logger.info(f"Synced {len(synced)} application commands.")

    async def on_ready(self) -> None:
        """Event handler for when the bot is ready and connected."""
        activity = discord.CustomActivity(name="🍌🍌🍌🍌🍌")
        await self.change_presence(status=discord.Status.online, activity=activity)
        app_logger.info(f'Logged in as {self.user.name} (ID: {self.user.id})')
        app_logger.warning('Bot is ready and online!')
