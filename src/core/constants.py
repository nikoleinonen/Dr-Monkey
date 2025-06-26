# --- Bot Behavior ---

# Delay in seconds before cleaning up messages in non-bot channels.
MESSAGE_CLEANUP_DELAY_SECONDS = 20

# Compact message format for analysis results after cleanup.
COMPACT_ANALYSIS_MESSAGE = "{username} is **{monkey_percentage}%** monkey and has an IQ of **{iq_score}**"

# Compact message format for monkey-off results after cleanup.
COMPACT_MONKEYOFF_MESSAGE = "**{challenger_name}** ({challenger_percentage}%) vs **{opponent_name}** ({opponent_percentage}%) | Winner: **{winner_name}**"

# Compact message format for a tied monkey-off result after cleanup.
COMPACT_MONKEYOFF_TIE_MESSAGE = "**{challenger_name}** ({challenger_percentage}%) vs **{opponent_name}** ({opponent_percentage}%) | It was a tie!"

# Default message for command cooldowns.
DEFAULT_COOLDOWN_MESSAGE = "You're on cooldown! Please try again in {retry_after:.2f} seconds."

# Generic error message for unhandled exceptions.
GENERIC_ERROR_MESSAGE = "An unexpected error occurred. The developers have been notified. (LOL not)"




# --- Analysis ---

# Minimum possible monkey percentage.
MIN_MONKEY_PERCENTAGE = 0

# Maximum possible monkey percentage.
MAX_MONKEY_PERCENTAGE = 100




# --- Plotting ---

# Background color for plots.
PLOT_BG_COLOR = '#2E2E2E'

# Background color for plot axes.
AXES_BG_COLOR = '#3C3C3C'

# Color for plot grid lines.
GRID_COLOR = 'grey'

# Primary color for bars in plots.
PRIMARY_BAR_COLOR = "#bbbbbb"

# Highlight color for specific bars in plots.
HIGHLIGHT_BAR_COLOR = "#ddd128"

# Font size for plot titles.
PLOT_TITLE_FONTSIZE = 14
