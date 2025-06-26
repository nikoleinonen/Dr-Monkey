import discord
from discord.ext import commands
from discord import app_commands, ui
import functools # Import functools for partial
from src.utils.plot_utils import generate_leaderboard_bar_plot, generate_leaderboard_string
from src.core.logging import get_logger
import io
from src.utils.checks import is_whitelisted_guild, is_allowed_bot_channel

logger = get_logger("C_Ranks")

# A more complex view with 9 buttons to cover all ranking types and metrics.
class RankAnalysisView(ui.View):
    def __init__(self, bot: commands.Bot, original_interaction: discord.Interaction, target_user: discord.Member):
        super().__init__(timeout=180.0)
        self.bot = bot
        self.original_interaction = original_interaction
        self.target_user = target_user
        # Set default state for the initial view
        self.ranking_type = "average"
        self.mode = "combined"

    async def on_timeout(self) -> None:
        # Disable all buttons on timeout
        for item in self.children:
            item.disabled = True
        try:
            await self.original_interaction.edit_original_response(view=self)
        except discord.NotFound:
            pass # Message was deleted, nothing to do.

    async def update_view(self, interaction: discord.Interaction, ranking_type: str, mode: str, initial: bool = False):
        # Update the view's state
        self.ranking_type = ranking_type
        self.mode = mode

        if not initial:
            await interaction.response.defer()

        # Update button styles to show the active view
        for child in self.children:
            if isinstance(child, ui.Button):
                is_active = (child.custom_id == f"rank_{self.ranking_type}_{self.mode}")
                child.style = discord.ButtonStyle.primary if is_active else discord.ButtonStyle.secondary
                child.disabled = is_active

        analysis_data = []
        # Run database queries in a separate thread to avoid blocking the event loop
        db_manager_func = None
        if self.ranking_type == "average":
            db_manager_func = functools.partial(self.bot.db_manager.get_average_analysis_data_for_guild, interaction.guild.id)
        elif self.ranking_type == "top":
            db_manager_func = functools.partial(self.bot.db_manager.get_single_record_analysis_data_for_guild, interaction.guild.id, metric=self.mode, order="DESC")
        elif self.ranking_type == "lowest":
            db_manager_func = functools.partial(self.bot.db_manager.get_single_record_analysis_data_for_guild, interaction.guild.id, metric=self.mode, order="ASC")
        elif self.ranking_type == "wins": # New: Top Wins
            db_manager_func = functools.partial(self.bot.db_manager.get_top_wins_data_for_guild, interaction.guild.id)
        elif self.ranking_type == "win_rate": # New: Highest Win Rate
            db_manager_func = functools.partial(self.bot.db_manager.get_top_win_rate_data_for_guild, interaction.guild.id)
        
        if db_manager_func: # Ensure a function was selected before executing
            analysis_data = await self.bot.loop.run_in_executor(None, db_manager_func)

        if not analysis_data:
            message = "No analysis data found for any monkeys in this server yet. Use `/analyze` to get started!"
            if initial:
                await interaction.followup.send(message)
            else:
                await interaction.edit_original_response(content=message, view=self, attachments=[])
            self.stop()
            return

        plot_buffer, leaderboard_data = None, []
        metric_name_for_leaderboard = ""
        metric_name_for_plot_label = ""
        plot_title = ""

        # Determine sorting order based on ranking_type
        # For "average" and "top", we want descending order (highest scores first)
        # For "lowest", we want ascending order (lowest scores first)
        reverse_sort = True if self.ranking_type in ["average", "top"] else False

        if self.mode == "combined":
            # Data for sorting and leaderboard
            ranked_data = sorted(analysis_data, key=lambda d: d[1] + d[2], reverse=reverse_sort) 
            leaderboard_data = [(uid, iq + monkey) for uid, iq, monkey in ranked_data]

            metric_name_for_plot_label = "Combined Score"
            metric_name_for_leaderboard = f"{'Combined Score (IQ + Monkey %)' if self.ranking_type == 'average' else ('Highest Combined Score (IQ + Monkey %)' if self.ranking_type == 'top' else 'Lowest Combined Score (IQ + Monkey %)')}"
            plot_title = f"{'Top' if self.ranking_type == 'top' else ('Lowest' if self.ranking_type == 'lowest' else 'Top')} 10 Monkeys by {'Average ' if self.ranking_type == 'average' else ''}Combined Score"
            plot_buffer = await generate_leaderboard_bar_plot(
                interaction, leaderboard_data, self.bot, # Pass bot instead of db_manager
                self.target_user.id, plot_title, metric_name_for_plot_label
            )
        elif self.mode == "iq":
            ranked_data = sorted(analysis_data, key=lambda d: d[1], reverse=reverse_sort)
            leaderboard_data = [(uid, iq) for uid, iq, _ in ranked_data]
            metric_name_for_plot_label = "IQ Score"
            metric_name_for_leaderboard = f"{'IQ Score' if self.ranking_type == 'average' else ('Highest IQ Score' if self.ranking_type == 'top' else 'Lowest IQ Score')}"
            plot_title = f"{'Top' if self.ranking_type == 'top' else ('Lowest' if self.ranking_type == 'lowest' else 'Top')} 10 Monkeys by {'Average ' if self.ranking_type == 'average' else ''}IQ Score"
            plot_buffer = await generate_leaderboard_bar_plot(
                interaction, leaderboard_data, self.bot, # Pass bot instead of db_manager
                self.target_user.id, plot_title, metric_name_for_plot_label
            )
        elif self.mode == "monkey":
            ranked_data = sorted(analysis_data, key=lambda d: d[2], reverse=reverse_sort)
            leaderboard_data = [(uid, monkey) for uid, _, monkey in ranked_data]
            metric_name_for_plot_label = "Monkey Purity %"
            metric_name_for_leaderboard = f"{'Monkey Purity %' if self.ranking_type == 'average' else ('Highest Monkey Purity %' if self.ranking_type == 'top' else 'Lowest Monkey Purity %')}"
            plot_title = f"{'Top' if self.ranking_type == 'top' else ('Lowest' if self.ranking_type == 'lowest' else 'Top')} 10 Monkeys by {'Average ' if self.ranking_type == 'average' else ''}Monkey Purity %"
            plot_buffer = await generate_leaderboard_bar_plot(
                interaction, leaderboard_data, self.bot, # Pass bot instead of db_manager
                self.target_user.id, plot_title, metric_name_for_plot_label
            )

        elif self.ranking_type == "wins":
            leaderboard_data = analysis_data
            metric_name_for_leaderboard = "Total Monkey-Off Wins"
            plot_title = "Top 10 Monkeys by Total Wins"
            plot_buffer = await generate_leaderboard_bar_plot(interaction, analysis_data, self.bot, self.target_user.id, plot_title, metric_name_for_leaderboard)
        elif self.ranking_type == "win_rate":
            leaderboard_data = analysis_data
            metric_name_for_leaderboard = "Monkey-Off Win Rate (%)"
            plot_title = "Top 10 Monkeys by Win Rate"
            # The x-axis label for the plot should be the same as the leaderboard metric name
            plot_buffer = await generate_leaderboard_bar_plot(interaction, analysis_data, self.bot, self.target_user.id, plot_title, metric_name_for_leaderboard)
        leaderboard_text = await generate_leaderboard_string(interaction, leaderboard_data, self.bot, metric_name_for_leaderboard)
        plot_file = discord.File(plot_buffer, filename=f"{self.ranking_type}_{self.mode}_rank_plot.png") if plot_buffer else None
        content = leaderboard_text if leaderboard_text else "Could not generate leaderboard."

        if initial:
            await interaction.followup.send(content=content, file=plot_file, view=self)
        else:
            await interaction.edit_original_response(content=content, attachments=[plot_file] if plot_file else [], view=self)
    
    # --- Row 1: Average Rankings ---
    @ui.button(label="Avg Combined", style=discord.ButtonStyle.secondary, custom_id="rank_average_combined", row=0)
    async def avg_combined_button(self, interaction: discord.Interaction, button: ui.Button): await self.update_view(interaction, "average", "combined")
    @ui.button(label="Avg IQ", style=discord.ButtonStyle.secondary, custom_id="rank_average_iq", row=0)
    async def avg_iq_button(self, interaction: discord.Interaction, button: ui.Button): await self.update_view(interaction, "average", "iq")
    @ui.button(label="Avg Monkey %", style=discord.ButtonStyle.secondary, custom_id="rank_average_monkey", row=0)
    async def avg_monkey_button(self, interaction: discord.Interaction, button: ui.Button): await self.update_view(interaction, "average", "monkey")

    # --- Row 2: Top Rankings ---
    @ui.button(label="Top Combined", style=discord.ButtonStyle.secondary, custom_id="rank_top_combined", row=1)
    async def top_combined_button(self, interaction: discord.Interaction, button: ui.Button): await self.update_view(interaction, "top", "combined")
    @ui.button(label="Top IQ", style=discord.ButtonStyle.secondary, custom_id="rank_top_iq", row=1)
    async def top_iq_button(self, interaction: discord.Interaction, button: ui.Button): await self.update_view(interaction, "top", "iq")
    @ui.button(label="Top Monkey %", style=discord.ButtonStyle.secondary, custom_id="rank_top_monkey", row=1)
    async def top_monkey_button(self, interaction: discord.Interaction, button: ui.Button): await self.update_view(interaction, "top", "monkey")

    # --- Row 3: Lowest Rankings ---
    @ui.button(label="Lowest Combined", style=discord.ButtonStyle.secondary, custom_id="rank_lowest_combined", row=2)
    async def low_combined_button(self, interaction: discord.Interaction, button: ui.Button): await self.update_view(interaction, "lowest", "combined")
    @ui.button(label="Lowest IQ", style=discord.ButtonStyle.secondary, custom_id="rank_lowest_iq", row=2)
    async def low_iq_button(self, interaction: discord.Interaction, button: ui.Button): await self.update_view(interaction, "lowest", "iq")
    @ui.button(label="Lowest Monkey %", style=discord.ButtonStyle.secondary, custom_id="rank_lowest_monkey", row=2)
    async def low_monkey_button(self, interaction: discord.Interaction, button: ui.Button): await self.update_view(interaction, "lowest", "monkey")

    # --- Row 4: Monkey-Off Rankings ---
    @ui.button(label="Top Wins", style=discord.ButtonStyle.secondary, custom_id="rank_wins_count", row=3)
    async def top_wins_button(self, interaction: discord.Interaction, button: ui.Button): await self.update_view(interaction, "wins", "count")
    @ui.button(label="Highest Win %", style=discord.ButtonStyle.secondary, custom_id="rank_win_rate_percentage", row=3)
    async def highest_win_rate_button(self, interaction: discord.Interaction, button: ui.Button): await self.update_view(interaction, "win_rate", "percentage")

@is_whitelisted_guild()
@is_allowed_bot_channel()
class RanksCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # The user requested the command to be called /ranks directly, not /rank analysis.
    # So, we'll make 'ranks' the main command.
    # If we wanted subcommands like /ranks analysis, /ranks wins, we'd keep the group.
    # For now, let's make /ranks the main command that opens the view.
    # rank_group = app_commands.Group(name="rank", description="Commands for viewing user rankings.")

    @app_commands.command(name="ranks", description="Shows user rankings by various metrics (Analysis, Wins, Win Rate).")
    @app_commands.describe(user="The user to highlight on the plot (optional).")
    async def analysis(self, interaction: discord.Interaction, user: discord.Member = None):
        """
        Shows a comprehensive ranking view with options for average, top, and lowest
        scores across combined, IQ, and monkey percentage metrics.
        """
        await interaction.response.defer(ephemeral=False)
        target_user = user if user else interaction.user
        
        view = RankAnalysisView(self.bot, interaction, target_user)
        # The initial response will be the "average" "combined" view by default.
        await view.update_view(interaction, ranking_type="average", mode="combined", initial=True)

async def setup(bot: commands.Bot):
    cog = RanksCog(bot)
    # If using a group, you'd add the group to the tree:
    # bot.tree.add_command(cog.rank_group)
    # But since we're making /ranks a top-level command, just add the cog.
    await bot.add_cog(cog)
