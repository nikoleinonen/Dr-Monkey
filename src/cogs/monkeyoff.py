import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
import functools
from src.core.logging import get_logger 
from src.resources import monkeyoff_responses, monkey_types
from src.core import constants
from src.utils.checks import is_whitelisted_guild

# Initialize logger for the MonkeyOff cog.
logger = get_logger("C_MonkeyOff")

class MonkeyOffCommand(commands.Cog):
    """Cog for the /monkeyoff command, allowing users to challenge each other."""
    def __init__(self, bot: commands.Bot) -> None:
        # Store the bot instance.
        self.bot = bot
    
    @app_commands.command(name="monkeyoff", description=f"Challenge another user to a monkey-off!")
    @app_commands.describe(opponent="The user you're challenging.")
    @is_whitelisted_guild()
    async def monkeyoff(self, interaction: discord.Interaction, opponent: discord.Member) -> None:
        """Challenges another user to a monkey-off, determining a winner based on random percentages."""
        # Extract challenger and opponent details.
        challenger = interaction.user
        guild_id = interaction.guild.id
        challenger_id = challenger.id
        challenger_name = challenger.display_name
        opponent_id = opponent.id
        opponent_name = opponent.display_name
        guild_name = interaction.guild.name
        
        # Prevent self-challenge.
        if challenger.id == opponent.id:
            await interaction.response.send_message("You can't monkey-off against yourself! Find a worthy adversary. OOK!", ephemeral=True)
            return

        # Since DB operations can take a moment, defer the response.
        await interaction.response.defer()

        # Ensure both challenger and opponent profiles exist in the database.
        # Run database operations in a separate thread to avoid blocking the event loop.
        ensure_challenger_func = functools.partial(self.bot.db_manager.ensure_user_exists, challenger_id, guild_id, challenger_name)
        ensure_opponent_func = functools.partial(self.bot.db_manager.ensure_user_exists, opponent_id, guild_id, opponent_name)
        await self.bot.loop.run_in_executor(None, ensure_challenger_func)
        await self.bot.loop.run_in_executor(None, ensure_opponent_func)
        # Generate random monkey percentages
        challenger_percentage = random.randint(0, 100)
        opponent_percentage = random.randint(0, 100)
        
        # Determine winner_id for database recording
        winner_id = None
        if challenger_percentage > opponent_percentage:
            winner_id = challenger_id
        elif opponent_percentage > challenger_percentage:
            winner_id = opponent_id
        
        # Record the monkey-off result in the database
        record_func = functools.partial(
            self.bot.db_manager.record_monkeyoff_result,
            challenger_id, opponent_id, guild_id, challenger_percentage, opponent_percentage, winner_id
        )
        await self.bot.loop.run_in_executor(None, record_func)
        # Get random monkey types for flavor
        challenger_monkey_type = monkey_types.get_random_monkey_type()
        opponent_monkey_type = monkey_types.get_random_monkey_type()
        
        logger.debug(f"Monkeyoff in ({guild_name}) {guild_id}: {challenger_name} ({challenger_id}) got {challenger_percentage}%.")
        logger.debug(f"Monkeyoff in ({guild_name}) {guild_id}: {opponent_name} ({opponent_id}) got {opponent_percentage}%.")
        
        embed_color = discord.Color.default()
        if challenger_percentage > opponent_percentage:
            embed_color = discord.Color.green()
        elif challenger_percentage < opponent_percentage:
            embed_color = discord.Color.red()
        else:
            embed_color = discord.Color.gold()
        
        # Get structured response data based on the outcome.
        response_data = monkeyoff_responses.get_monkeyoff_response(
            challenger, challenger_percentage, opponent, opponent_percentage,
            challenger_monkey_type, opponent_monkey_type
        )
        
        # Use title and description from the structured response data.
        embed_title = response_data.get("title", "🐒 Monkey-Off Results! 🐒")
        embed_description = response_data.get("description", "The monkey-off has concluded! Check the transaction note for details if something went wrong.")
        
        # Create and send the embed.
        embed = discord.Embed(
            title=embed_title,
            description=embed_description,
            color=embed_color
        )

        embed.add_field(name=f"{challenger.display_name}'s Form", value=f"**{challenger_monkey_type}**!", inline=True)
        embed.add_field(name=f"{opponent.display_name}'s Form", value=f"**{opponent_monkey_type}**!", inline=True)

        await interaction.followup.send(embed=embed)

        # If the command was used in a non-designated bot channel,
        # wait and then edit the message to a compact form.
        allowed_channels = getattr(interaction.client, "bot_channel_ids", [])
        if interaction.channel and interaction.channel.id not in allowed_channels:
            await asyncio.sleep(constants.MESSAGE_CLEANUP_DELAY_SECONDS)

            final_message = ""
            if winner_id is None:  # Tie
                final_message = constants.COMPACT_MONKEYOFF_TIE_MESSAGE.format(
                    challenger_name=challenger_name,
                    challenger_percentage=challenger_percentage,
                    opponent_name=opponent_name,
                    opponent_percentage=opponent_percentage,
                )
            else:
                winner_name = challenger_name if winner_id == challenger_id else opponent_name
                final_message = constants.COMPACT_MONKEYOFF_MESSAGE.format(
                    challenger_name=challenger_name,
                    challenger_percentage=challenger_percentage,
                    opponent_name=opponent_name,
                    opponent_percentage=opponent_percentage,
                    winner_name=winner_name,
                )

            try:
                # Edit the original message to a compact text format.
                await interaction.edit_original_response(content=final_message, embed=None)
            except discord.NotFound:
                logger.warning(
                    f"Could not edit original monkeyoff message for {challenger_name} vs {opponent_name}, "
                    f"it was likely deleted before cleanup."
                )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MonkeyOffCommand(bot))
