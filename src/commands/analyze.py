import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
from src.logging_config import get_logger
from src.commands.responses import analysis_responses
import src.database_manager as db

logger = get_logger("C_Analyze")

# Moved from the old iq.py
def generate_weighted_iq() -> int:
    """Generates an IQ score with a weighted distribution."""
    iq_ranges_config = [
        # (min_iq, max_iq, weight)
        (0, 0, 5),
        (1, 19, 10),
        (20, 39, 20),
        (40, 59, 100),
        (60, 120, 3000),
        (121, 160, 100),
        (161, 180, 20),
        (181, 199, 10),
        (200, 200, 5)
    ]

    ranges = [(r[0], r[1]) for r in iq_ranges_config]
    weights = [r[2] for r in iq_ranges_config]

    chosen_min, chosen_max = random.choices(ranges, weights=weights, k=1)[0]
    return random.randint(chosen_min, chosen_max)

class AnalyzeCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="analyze", description="Get your comprehensive primate analysis!")
    @app_commands.check(lambda interaction: interaction.client.check_guild(interaction))
    async def analyze(self, interaction: discord.Interaction) -> None:
        iq_score = generate_weighted_iq()
        monkey_percentage = random.randint(0, 100)

        user = interaction.user
        username = user.display_name

        # Record the analysis result in the database
        # The guild check decorator ensures interaction.guild is not None
        if not db.record_analysis_result(user.id, interaction.guild.id, iq_score, monkey_percentage, username):
            logger.error(f"Failed to record analysis for user {user.id} in guild {interaction.guild.id}")

        # Always send the full embed first, in every channel
        raw_response_body = analysis_responses.get_analysis_response(iq_score, monkey_percentage)
        embed = discord.Embed(title=f"🔬 Primate Analysis Complete! 🔬", description=f"{raw_response_body}", color=discord.Color.purple())
        embed.add_field(name="IQ Score", value=f"**{iq_score}**", inline=True)
        embed.add_field(name="Monkey Purity", value=f"**{monkey_percentage}%**", inline=True)
        embed.set_footer(text=f"Subject: {username}")

        await interaction.response.send_message(embed=embed)

        # If the command was used in a channel that is NOT a designated bot channel,
        # wait 30s and then clean up the message to a more compact form.
        allowed_channels = getattr(interaction.client, "bot_channel_ids", [])
        if interaction.channel and interaction.channel.id not in allowed_channels:
            await asyncio.sleep(30)
            final_message = f"{username} is **{monkey_percentage}%** monkey and has an IQ of **{iq_score}**"
            try:
                # Edit the original message to remove the embed and show the compact text
                await interaction.edit_original_response(content=final_message, embed=None)
            except discord.NotFound:
                logger.warning(f"Could not edit original analysis message for {username}, it was likely deleted before cleanup.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AnalyzeCommand(bot))
