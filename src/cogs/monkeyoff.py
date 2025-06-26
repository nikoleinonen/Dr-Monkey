import discord
from discord.ext import commands
from discord import app_commands
import random
from src.core.logging import get_logger
from src.resources import monkeyoff_responses
from src.core import database as db


logger = get_logger("C_MonkeyOff")

class MonkeyOffCommand(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="monkeyoff", description=f"Challenge another user to a monkey-off!")
    @app_commands.check(lambda interaction: interaction.client.check_guild(interaction)) # Keep guild check
    @app_commands.describe(opponent="The user you're challenging.")
    async def monkeyoff(self, interaction: discord.Interaction, opponent: discord.Member) -> None:
        if interaction.guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return
        guild_name = interaction.guild.name

        challenger = interaction.user
        guild_id = interaction.guild.id
        challenger_id = challenger.id
        challenger_name = challenger.display_name
        opponent_id = opponent.id
        opponent_name = opponent.display_name

        if challenger.id == opponent.id:
            await interaction.response.send_message("You can't monkey-off against yourself! Find a worthy adversary. OOK!", ephemeral=True)
            return

        # Ensure users exist in the database (for profile updates like username)
        db.ensure_user_exists(challenger_id, guild_id, challenger_name)
        db.ensure_user_exists(opponent_id, guild_id, opponent_name)

        # Generate random monkey percentages
        challenger_percentage = random.randint(0, 100)
        opponent_percentage = random.randint(0, 100)

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
            challenger, challenger_percentage, opponent, opponent_percentage
        )
        
        # Use title and description from the structured response data
        embed_title = response_data.get("title", "🐒 Monkey-Off Results! 🐒")
        embed_description = response_data.get("description", "The monkey-off has concluded! Check the transaction note for details if something went wrong.")

        embed = discord.Embed(
            title=embed_title,
            description=embed_description,
            color=embed_color
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MonkeyOffCommand(bot))
