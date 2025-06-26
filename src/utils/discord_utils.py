import discord
from src.core.database import DatabaseManager # Import DatabaseManager
from src.core.logging import get_logger

logger = get_logger("DiscordUtils")

async def get_display_name_for_user_id(
    user_id: int,
    guild: discord.Guild | None,
    db_manager: DatabaseManager, # Add db_manager parameter
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
        profile = db_manager.get_user_profile(user_id, guild.id)
        if profile and profile.get('username'):
            return profile['username']
    
    # Fallback if no guild context or not found in DB
    return default_name
