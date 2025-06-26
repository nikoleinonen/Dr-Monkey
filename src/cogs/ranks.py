import discord
from discord.ext import commands
from discord import app_commands
from src.core import database as db
from src.utils.plot_utils import generate_scatter_rank_plot, generate_leaderboard_string
from src.core.logging import get_logger

logger = get_logger("C_Ranks")

class RanksCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Cog-wide check for all application commands in this cog.
        This is the modern approach for app_commands, replacing `cog_check`.
        It verifies that the command is used in a whitelisted guild and an allowed channel.
        """
        # 1. Guild Whitelist Check
        if hasattr(interaction.client, "check_guild") and callable(interaction.client.check_guild):
            if not await interaction.client.check_guild(interaction):
                return False  # The check_guild method sends its own response.
        else:
            logger.warning("RanksCog.interaction_check: client is missing 'check_guild' method.")
            return False

        # 2. Allowed Bot Channel Check
        if not hasattr(interaction.client, "bot_channel_ids"):
            logger.error("RanksCog.interaction_check: client does not have 'bot_channel_ids' attribute.")
            await interaction.response.send_message("An internal error occurred with channel permissions.", ephemeral=True)
            return False

        allowed_channels: list[int] = interaction.client.bot_channel_ids
        logger.debug(f"RanksCog channel check for user {interaction.user.id}. Channel: {interaction.channel.id}. Allowed: {allowed_channels}")
        if not allowed_channels or (interaction.channel and interaction.channel.id in allowed_channels):
            return True  # No restrictions, or channel is in the allowed list.

        await interaction.response.send_message("This command is not allowed in this channel. Please use a designated bot channel.", ephemeral=True)
        return False

    rank_group = app_commands.Group(name="rank", description="View user rankings based on various stats.")

    @rank_group.command(name="analysis", description="Shows a scatter plot of user IQ vs. Monkey %.")
    @app_commands.describe(user="The user to highlight on the plot (optional).")
    async def rank_analysis_plot(self, interaction: discord.Interaction, user: discord.Member = None):
        if interaction.guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=False)
        target_user = user if user else interaction.user

        # analysis_data is list of (user_id, iq_score, monkey_percentage)
        analysis_data = db.get_all_analysis_data_for_guild(interaction.guild.id)
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
        leaderboard_text = await generate_leaderboard_string(interaction, leaderboard_analysis_data, "Combined Score (IQ + Monkey %)")

        if plot_file:
            await interaction.followup.send(content=leaderboard_text, file=plot_file)
        else: # Fallback if plot generation failed but leaderboard text might exist
            await interaction.followup.send(content=leaderboard_text if leaderboard_text else "Could not generate analysis plot. No data or error.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(RanksCog(bot))
