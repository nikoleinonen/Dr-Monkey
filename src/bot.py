import discord
from discord.ext import commands
from discord import app_commands
from src.core.database import DatabaseManager # Import the class
from src.core.logging import get_logger
from src import config, constants

app_logger = get_logger("DrMonkeyBot")

# Initialize intents (Yes these are setup in DEV website)
intents = discord.Intents.default()
intents.members = True

class DrMonkey(commands.Bot):
    def __init__(self, db_manager: DatabaseManager) -> None: # Accept db_manager
        super().__init__(command_prefix="!", intents=intents)
        self.db_manager = db_manager # Store the db_manager
        self.bot_channel_ids = config.BOT_CHANNEL_IDS
        self.whitelisted_servers = config.WHITELISTED_GUILD_IDS
        self._one_time_setup_done = False
        self.tree.on_error = self.on_app_command_error

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Global error handler for all application commands."""
        if isinstance(error, app_commands.CheckFailure):
            # This error is raised when a check fails. The check itself should have
            # sent a response. The default behavior logs this as an ERROR, which is what we want to avoid.
            app_logger.info(
                f"Command '{interaction.command.name}' check failed for user {interaction.user.id} "
                f"in channel {interaction.channel.id}. This is expected for permission checks."
            )
        elif isinstance(error, app_commands.CommandOnCooldown):
            # Handle cooldowns gracefully
            await interaction.response.send_message(
                constants.DEFAULT_COOLDOWN_MESSAGE.format(retry_after=error.retry_after),
                ephemeral=True
            )
        else:
            # For any other errors, we log them as an error and notify the user.
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
        # All commands using this check are implicitly guild-only.
        if interaction.guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return False

        if not self.whitelisted_servers:
            app_logger.warning("WHITELISTED_GUILD_IDS is not set. Allowing command as no restrictions are configured.")
            return True

        if interaction.guild.id in self.whitelisted_servers:
            return True
        else:
            app_logger.info(f"Command attempt in non-whitelisted guild: {interaction.guild.name} (ID: {interaction.guild.id}).")
            await interaction.response.send_message("This bot is not enabled in this server.", ephemeral=True)
            return False

    async def setup_hook(self) -> None:
        app_logger.info("Running setup_hook...")
        self.db_manager.initialize_database() # Use the manager instance

        if not self.whitelisted_servers:
            app_logger.warning("No servers whitelisted! The bot will not respond to commands in any server.")
        else:
            app_logger.info(f"Server whitelist loaded. The bot will only respond in guilds: {self.whitelisted_servers}")

        cogs_to_load = [
            "src.cogs.analyze",
            "src.cogs.monkeyoff",
            "src.cogs.ranks",
        ]

        for cog_path in cogs_to_load:
            try:
                await self.load_extension(cog_path)
                app_logger.info(f"Successfully loaded cog: {cog_path}")
            except Exception as e:
                app_logger.error(f"Failed to load '{cog_path}' cog.", exc_info=e)

        synced = await self.tree.sync()
        app_logger.info(f"Synced {len(synced)} application commands.")

    async def on_ready(self) -> None:
        activity = discord.CustomActivity(name="🍌🍌🍌🍌🍌")
        await self.change_presence(status=discord.Status.online, activity=activity)
        app_logger.info(f'Logged in as {self.user.name} (ID: {self.user.id})')
        app_logger.warning('Bot is ready and online!')
