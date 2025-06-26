import discord
from discord import app_commands
from src.core.logging import get_logger

logger = get_logger("UtilsChecks")

def is_allowed_bot_channel():
    """
    A discord.py check decorator to verify if a command is used in an allowed bot channel.
    If no bot channels are configured in .env, commands are allowed everywhere (respecting guild whitelist).
    """
    async def predicate(interaction: discord.Interaction) -> bool:
        # Ensure the client is the bot instance to access custom attributes
        if not hasattr(interaction.client, "bot_channel_ids"):
            logger.error("Bot channel check: Bot client does not have 'bot_channel_ids' attribute.")
            await interaction.response.send_message("An internal error occurred with channel permissions. Please contact an admin. DONT ACTUALLY", ephemeral=True)
            return False

        allowed_channels: list[int] = interaction.client.bot_channel_ids
        if not allowed_channels:
            return True
        
        if interaction.channel and interaction.channel.id in allowed_channels:
            return True
        else:
            await interaction.response.send_message("This command is not allowed in this channel. Please use a designated bot channel.", ephemeral=True)
            return False
    return app_commands.check(predicate)
    
def is_whitelisted_guild():
    """
    A discord.py check decorator to verify if a command is used in a whitelisted guild.
    Relies on the bot's `check_guild` method.
    """
    async def predicate(interaction: discord.Interaction) -> bool:
        if hasattr(interaction.client, "check_guild") and callable(interaction.client.check_guild):
            return await interaction.client.check_guild(interaction)
        return False
    return app_commands.check(predicate)
