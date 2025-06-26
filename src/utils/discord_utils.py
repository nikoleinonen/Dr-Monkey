import discord
from discord.ext import commands
from src.core.logging import get_logger
import functools

logger = get_logger("DiscordUtils")

async def get_display_name_for_user_id(
    user_id: int,
    guild: discord.Guild | None,
    bot: commands.Bot,
    default_name: str = "Unknown User",
) -> str:
    """
    Resolves a user's display name.
    Prioritizes live guild member data, then cached data, then database, and finally a default.
    """
    if guild:
        member = guild.get_member(user_id)
        if member:
            return member.display_name
        
        # If user not found in guild cache, try fetching from the database.
        # Run database query in a separate thread to avoid blocking the event loop.
        get_profile_func = functools.partial(bot.db_manager.get_user_profile, user_id, guild.id)
        profile = await bot.loop.run_in_executor(None, get_profile_func)
        if profile and profile.get('username'):
            return profile['username']
    
    # Fallback to default name if not found in guild or database.
    return default_name
