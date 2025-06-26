import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import discord
from discord.ext import commands # Import commands for Bot type hinting
from datetime import datetime
import functools # Import functools for partial
from src.utils.discord_utils import get_display_name_for_user_id
from src.utils.formatters import format_large_number
from src.core import constants
from src.core.logging import get_logger

async def generate_leaderboard_bar_plot(
    interaction: discord.Interaction,
    ranked_data: list[tuple[int, float]],
    bot: commands.Bot, # Accept bot object to access loop and db_manager
    target_user_id: int,
    title: str,
    x_label: str,
    limit: int = 10
) -> io.BytesIO | None:
    """
    Generates a horizontal bar plot for a leaderboard.
    Returns a BytesIO buffer containing the plot image.
    """
    if not ranked_data:
        return None

    data_to_plot = ranked_data[:limit]
    data_to_plot.reverse()  # To plot top-to-bottom

    user_ids = [d[0] for d in data_to_plot]
    scores = [d[1] for d in data_to_plot]

    names = []
    for uid in user_ids:
        name = await get_display_name_for_user_id(uid, interaction.guild, bot) # Pass bot
        names.append(name[:15] + '...' if len(name) > 18 else name)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(names, scores, color=constants.PRIMARY_BAR_COLOR)

    try:
        highlight_index = user_ids.index(target_user_id)
        bars[highlight_index].set_color(constants.HIGHLIGHT_BAR_COLOR)
    except ValueError:
        pass  # Target user not in top N

    ax.set_xlabel(x_label)
    ax.set_title(title, fontsize=constants.PLOT_TITLE_FONTSIZE)
    fig.patch.set_facecolor(constants.PLOT_BG_COLOR)
    ax.set_facecolor(constants.AXES_BG_COLOR)
    ax.tick_params(axis='x', colors='white') # Make x-axis ticks visible on dark background
    ax.tick_params(axis='y', colors='white') # Make y-axis ticks visible on dark background
    plt.tight_layout(pad=2)

    buf = io.BytesIO()
    await bot.loop.run_in_executor(None, functools.partial(plt.savefig, buf, format='png', dpi=100)) # Run savefig in executor
    buf.seek(0)
    await bot.loop.run_in_executor(None, plt.close, fig) # Close figure in executor
    await bot.loop.run_in_executor(None, plt.style.use, 'default') # Reset style in executor
    return buf

async def generate_leaderboard_string(
    interaction: discord.Interaction,
    ranked_data: list[tuple[int, float]],
    bot: commands.Bot, # Accept bot object to access loop and db_manager
    metric_name: str,
    limit: int = 10
) -> str | None:
    """
    Generates a formatted string for a leaderboard.
    """
    if not ranked_data:
        return None

    leaderboard_lines = [f"\n\n**🏆 Top {min(limit, len(ranked_data))} Leaderboard (by {metric_name}):**"]
    
    for i, (user_id, score_value) in enumerate(ranked_data[:limit]):
        rank_num = i + 1
        name_to_display = await get_display_name_for_user_id(user_id, interaction.guild, bot) # Pass bot
        
        if len(name_to_display) > 25:
            name_to_display = name_to_display[:22] + "..."

        leaderboard_lines.append(f"`{rank_num:2d}.` **{name_to_display}** - `{format_large_number(score_value)}`")
    return "\n".join(leaderboard_lines)
