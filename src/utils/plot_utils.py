import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import discord
from datetime import datetime
from src.utils.discord_utils import get_display_name_for_user_id
from src.utils.formatters import format_large_number
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
    Generates a scatter plot for rankings (e.g., IQ vs Monkey Purity, Net Gambling vs Games Played).
    Returns a BytesIO buffer containing the plot image.
    """
    if not data_tuples:
        return None

    plot_actual_user_ids = [d[0] for d in data_tuples]
    plot_actual_y_values = [d[1] for d in data_tuples]
    plot_actual_x_values = [d[2] for d in data_tuples]

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scatter_colors = ['#4287f5'] * len(plot_actual_user_ids) 
    scatter_sizes = [30] * len(plot_actual_user_ids)       
    try:
        scatter_highlight_index = plot_actual_user_ids.index(target_user_id)
        scatter_colors[scatter_highlight_index] = '#f5d442' 
        scatter_sizes[scatter_highlight_index] = 100
    except ValueError:
        pass # Target user not in this specific data set

    ax.scatter(plot_actual_x_values, plot_actual_y_values, c=scatter_colors, s=scatter_sizes, alpha=0.7)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title, fontsize=14)
    ax.grid(True, linestyle=':', alpha=0.4, color='grey')
    fig.patch.set_facecolor('#2E2E2E')
    ax.set_facecolor('#3C3C3C')

    # Specific axis limits for analysis plot
    if "Monkey Purity %" in x_label and "IQ Score" in y_label:
        ax.set_xlim(0, 100) 
        ax.set_ylim(0, 200) 

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
        name_to_display = await get_display_name_for_user_id(user_id, interaction.guild)
        
        if len(name_to_display) > 25:
            name_to_display = name_to_display[:22] + "..."

        leaderboard_lines.append(f"`{rank_num:2d}.` **{name_to_display}** - `{format_large_number(score_value)}`")
    return "\n".join(leaderboard_lines)
