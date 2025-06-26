import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import discord
from datetime import datetime
from src.core.database import DatabaseManager # Import DatabaseManager
from src.utils.discord_utils import get_display_name_for_user_id
from src.utils.formatters import format_large_number
from src.core import constants
from src.core.logging import get_logger

logger = get_logger("PlotUtils")

async def generate_scatter_rank_plot(
    interaction: discord.Interaction,
    data_tuples: list[tuple[int, float, float]],
    target_user_id: int,
    title: str,
    y_label: str,
    x_label: str
) -> io.BytesIO | None:
    """
    Generates a scatter plot for rankings (e.g., IQ vs Monkey Purity).
    Returns a BytesIO buffer containing the plot image.
    """
    if not data_tuples:
        return None

    plot_actual_user_ids = [d[0] for d in data_tuples]
    plot_actual_y_values = [d[1] for d in data_tuples]
    plot_actual_x_values = [d[2] for d in data_tuples]

    plt.style.use('dark_background') # This is a global change, which is a separate issue. I'll leave it for now.
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scatter_colors = [constants.PRIMARY_SCATTER_COLOR] * len(plot_actual_user_ids)
    scatter_sizes = [constants.PRIMARY_SCATTER_SIZE] * len(plot_actual_user_ids)
    try:
        scatter_highlight_index = plot_actual_user_ids.index(target_user_id)
        scatter_colors[scatter_highlight_index] = constants.HIGHLIGHT_SCATTER_COLOR
        scatter_sizes[scatter_highlight_index] = constants.HIGHLIGHT_SCATTER_SIZE
    except ValueError:
        pass # Target user not in this specific data set

    ax.scatter(plot_actual_x_values, plot_actual_y_values, c=scatter_colors, s=scatter_sizes, alpha=constants.SCATTER_ALPHA)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title, fontsize=constants.PLOT_TITLE_FONTSIZE)
    ax.grid(True, linestyle=':', alpha=0.4, color=constants.GRID_COLOR)
    fig.patch.set_facecolor(constants.PLOT_BG_COLOR)
    ax.set_facecolor(constants.AXES_BG_COLOR)

    # Specific axis limits for analysis plot
    if "Monkey Purity %" in x_label and "IQ Score" in y_label:
        ax.set_xlim(constants.ANALYSIS_PLOT_X_LIMITS)
        ax.set_ylim(constants.ANALYSIS_PLOT_Y_LIMITS)

    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close(fig)
    plt.style.use('default')
    return buf

async def generate_leaderboard_string(
    interaction: discord.Interaction,
    ranked_data: list[tuple[int, float]],
    db_manager: DatabaseManager, # Add db_manager parameter
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
        name_to_display = await get_display_name_for_user_id(user_id, interaction.guild, db_manager)
        
        if len(name_to_display) > 25:
            name_to_display = name_to_display[:22] + "..."

        leaderboard_lines.append(f"`{rank_num:2d}.` **{name_to_display}** - `{format_large_number(score_value)}`")
    return "\n".join(leaderboard_lines)
