import discord
from discord.ext import commands
from discord import app_commands
import functools
import asyncio
import random
from src.core.logging import get_logger
from src.resources.analysis_responses import get_analysis_response, generate_weighted_iq
from src.utils.checks import is_whitelisted_guild
from src.core import constants
# Initialize logger for the Analyze cog.
logger = get_logger("C_Analyze")

class AnalyzeCommand(commands.Cog):
    """Cog for the /analyze command, providing primate analysis."""
    def __init__(self, bot: commands.Bot) -> None:
        # Store the bot instance.
        self.bot = bot

    @app_commands.command(name="analyze", description="Get your comprehensive primate analysis!")
    @is_whitelisted_guild()
    async def analyze(self, interaction: discord.Interaction) -> None:
        """Generates and displays a primate analysis for the user."""
        # Generate random IQ and monkey percentage scores.
        iq_score: int = generate_weighted_iq()
        monkey_percentage: int = random.randint(constants.MIN_MONKEY_PERCENTAGE, constants.MAX_MONKEY_PERCENTAGE)
        
        # Get user and guild information.
        user = interaction.user
        username = user.display_name
        guild_name = interaction.guild.name
        
        # Record the analysis result in the database in a separate thread
        # to avoid blocking the event loop.
        record_func = functools.partial(self.bot.db_manager.record_analysis_result,
                                        user.id, interaction.guild.id, iq_score, monkey_percentage, username, guild_name)
        if not await self.bot.loop.run_in_executor(None, record_func):
            logger.error(f"Failed to record analysis for user {username} ({user.id}) in guild {guild_name} ({interaction.guild.id})")

        # Always send the full embed first, in every channel
        raw_response_body = get_analysis_response(iq_score, monkey_percentage)
        embed = discord.Embed(title=f"🔬 Primate Analysis Complete! 🔬", description=f"{raw_response_body}", color=discord.Color.purple())
        embed.add_field(name="IQ Score", value=f"**{iq_score}**", inline=True)
        embed.add_field(name="Monkey Purity", value=f"**{monkey_percentage}%**", inline=True)
        embed.set_footer(text=f"Subject: {username}")
        
        # Send the initial embed response.
        await interaction.response.send_message(embed=embed)
        
        # If the command was used in a non-designated bot channel,
        # wait and then edit the message to a compact form.
        allowed_channels = getattr(interaction.client, "bot_channel_ids", [])
        if interaction.channel and interaction.channel.id not in allowed_channels:
            await asyncio.sleep(constants.ANALYZE_CLEANUP_DELAY_SECONDS)
            final_message = constants.COMPACT_ANALYSIS_MESSAGE.format(
                username=username, monkey_percentage=monkey_percentage, iq_score=iq_score
            )
            try:
                # Edit the original message to a compact text format.
                await interaction.edit_original_response(content=final_message, embed=None)
            except discord.NotFound:
                logger.warning(f"Could not edit original analysis message for {username}, it was likely deleted before cleanup.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AnalyzeCommand(bot))
