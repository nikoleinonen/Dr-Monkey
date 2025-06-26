import discord
import src.database_manager as db
from src.logging_config import get_logger

logger = get_logger("DiscordUtils")

async def get_display_name_for_user_id(
    user_id: int,
    guild: discord.Guild | None,
    default_name: str = "Unknown User"
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
        profile = db.get_user_profile(user_id, guild.id)
        if profile and profile.get('username'):
            return profile['username']
    
    # Fallback if no guild context or not found in DB
    return default_name
