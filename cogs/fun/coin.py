# coin.py
import discord
from discord.ext import commands
from discord import app_commands
from config import GUILD_ID
import random

class Coin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @app_commands.command(name="coin", description="flips a coin")
  @app_commands.guilds(discord.Object(id=GUILD_ID))
  async def coin(self, interaction: discord.Interaction):
    flipped_coin = random.choice(["Heads", "Tails"])
    await interaction.response.send_message(flipped_coin)

async def setup(bot):
  await bot.add_cog(Coin(bot))

