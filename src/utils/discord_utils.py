import discord
from discord.ext import commands # Import commands for Bot type hinting
from src.core.logging import get_logger
import functools # Import functools for partial

logger = get_logger("DiscordUtils")

async def get_display_name_for_user_id(
    user_id: int,
    guild: discord.Guild | None,
    bot: commands.Bot, # Accept bot object to access loop and db_manager
    default_name: str = "Unknown User",
) -> str:
    """
    Resolves a user's display name, prioritizing live guild data, then cached data,
    then database, and finally a default.
    """
    if guild:
        member = guild.get_member(user_id)
        if member:
            return member.display_name
        
        # If not in guild (e.g., user left, or not cached), try database
        # Run database query in a separate thread to avoid blocking
        get_profile_func = functools.partial(bot.db_manager.get_user_profile, user_id, guild.id)
        profile = await bot.loop.run_in_executor(None, get_profile_func)
        if profile and profile.get('username'):
            return profile['username']
    
    # Fallback if no guild context or not found in DB
    return default_name
