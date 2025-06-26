import discord
from discord import app_commands
from src.logging_config import get_logger

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

async def guild_whitelist_check(interaction: discord.Interaction) -> bool:
    """A predicate that checks if the command is used in a whitelisted guild."""
    # The `check_guild` method is defined on our custom DrMonkey bot class.
    if hasattr(interaction.client, "check_guild") and callable(interaction.client.check_guild):
        return await interaction.client.check_guild(interaction)

    logger.warning("guild_whitelist_check: interaction.client is missing 'check_guild' method.")
    return False # Fails safely if the method doesn't exist.
