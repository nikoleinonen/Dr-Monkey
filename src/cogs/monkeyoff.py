import discord
from discord.ext import commands
from discord import app_commands
import random
from src.core.logging import get_logger 
from src.resources import monkeyoff_responses, monkey_types
from src.utils.checks import is_whitelisted_guild


logger = get_logger("C_MonkeyOff")

class MonkeyOffCommand(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="monkeyoff", description=f"Challenge another user to a monkey-off!")
    @is_whitelisted_guild()
    @app_commands.describe(opponent="The user you're challenging.")
    async def monkeyoff(self, interaction: discord.Interaction, opponent: discord.Member) -> None:

        challenger = interaction.user
        guild_id = interaction.guild.id
        challenger_id = challenger.id
        challenger_name = challenger.display_name
        opponent_id = opponent.id
        opponent_name = opponent.display_name
        guild_name = interaction.guild.name # Safe to access now

        if challenger.id == opponent.id:
            await interaction.response.send_message("You can't monkey-off against yourself! Find a worthy adversary. OOK!", ephemeral=True)
            return

        # Ensure users exist in the database (for profile updates like username)
        self.bot.db_manager.ensure_user_exists(challenger_id, guild_id, challenger_name)
        self.bot.db_manager.ensure_user_exists(opponent_id, guild_id, opponent_name)

        # Generate random monkey percentages
        challenger_percentage = random.randint(0, 100)
        opponent_percentage = random.randint(0, 100)

        # Get random monkey types for flavor
        challenger_monkey_type = monkey_types.get_random_monkey_type()
        opponent_monkey_type = monkey_types.get_random_monkey_type()

        logger.info(f"Monkeyoff in ({guild_name}) {guild_id}: {challenger_name} ({challenger_id}) got {challenger_percentage}%.")
        logger.info(f"Monkeyoff in ({guild_name}) {guild_id}: {opponent_name} ({opponent_id}) got {opponent_percentage}%.")

        embed_color = discord.Color.default()
        if challenger_percentage > opponent_percentage:
            embed_color = discord.Color.green()
        elif challenger_percentage < opponent_percentage:
            embed_color = discord.Color.red()
        else:
            embed_color = discord.Color.gold()

        response_data = monkeyoff_responses.get_monkeyoff_response(
            challenger, challenger_percentage, opponent, opponent_percentage,
            challenger_monkey_type, opponent_monkey_type
        )
        
        # Use title and description from the structured response data
        embed_title = response_data.get("title", "🐒 Monkey-Off Results! 🐒")
        embed_description = response_data.get("description", "The monkey-off has concluded! Check the transaction note for details if something went wrong.")

        embed = discord.Embed(
            title=embed_title,
            description=embed_description,
            color=embed_color
        )

        embed.add_field(name=f"{challenger.display_name}'s Form", value=f"**{challenger_monkey_type}**!", inline=True)
        embed.add_field(name=f"{opponent.display_name}'s Form", value=f"**{opponent_monkey_type}**!", inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MonkeyOffCommand(bot))
