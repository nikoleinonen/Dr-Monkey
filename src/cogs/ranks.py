import discord
from discord.ext import commands
from discord import app_commands
from src.utils.checks import is_allowed_bot_channel, is_whitelisted_guild
from src.core.database import DatabaseManager # Import DatabaseManager for type hinting
from src.utils.plot_utils import generate_scatter_rank_plot, generate_leaderboard_string
from src.core.logging import get_logger

logger = get_logger("C_Ranks")

class RanksCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    rank_group = app_commands.Group(name="rank", description="View user rankings based on various stats.")

    @rank_group.command(name="analysis", description="Shows a scatter plot of user IQ vs. Monkey %.")
    @app_commands.describe(user="The user to highlight on the plot (optional).")
    async def rank_analysis_plot(self, interaction: discord.Interaction, user: discord.Member = None):
        await interaction.response.defer(ephemeral=False)
        target_user = user if user else interaction.user

        # analysis_data is list of (user_id, iq_score, monkey_percentage)
        analysis_data = self.bot.db_manager.get_all_analysis_data_for_guild(interaction.guild.id)
        if not analysis_data:
            await interaction.followup.send("No analysis data found for users in this server yet. Use `/analyze` to get started!")
            return
        
        # analysis_data is list of (user_id, iq_score, monkey_percentage)
        # Sort for leaderboard (based on combined score)
        ranked_analysis_data = sorted(analysis_data, key=lambda d: d[1] + d[2], reverse=True)

        # For the leaderboard, we need user_id and the combined score (IQ + Monkey %)
        leaderboard_analysis_data = [(uid, iq_score + monkey_percentage) for uid, iq_score, monkey_percentage in ranked_analysis_data]

        plot_buffer = await generate_scatter_rank_plot(
            interaction,
            [(d[0], float(d[1]), float(d[2])) for d in analysis_data], # Convert to float for generic scatter
            target_user.id,
            "Primate Analysis Ranking", "IQ Score (0-200)", "Monkey Purity % (0-100)"
        )
        plot_file = discord.File(plot_buffer, filename="analysis_rank_plot.png") if plot_buffer else None
        leaderboard_text = await generate_leaderboard_string(interaction, leaderboard_analysis_data, self.bot.db_manager, "Combined Score (IQ + Monkey %)")

        if plot_file:
            await interaction.followup.send(content=leaderboard_text, file=plot_file)
        else: # Fallback if plot generation failed but leaderboard text might exist
            await interaction.followup.send(content=leaderboard_text if leaderboard_text else "Could not generate analysis plot. No data or error.", ephemeral=True)

async def setup(bot: commands.Bot):
    cog = RanksCog(bot)
    cog.rank_group.add_check(is_whitelisted_guild().predicate)
    cog.rank_group.add_check(is_allowed_bot_channel().predicate)
    await bot.add_cog(cog)
