# bot.py

import discord
from discord.ext import commands
from config import TOKEN, GUILD_ID
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="None", intents=intents)

@bot.event
async def on_ready():
  print(f"✅ Logged in as {bot.user}")
  try:
    synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"🔧 Synced {len(synced)} command(s) in guild.")
  except Exception as e:
    print(f"❌ Sync failed: {e}")


async def load_cogs():
  for root, _, files in os.walk("./cogs"):
    for file in files:
      if file.endswith(".py") and not file.startswith("_"):
        path = os.path.join(root, file)
        module = path.replace("\\", ".").replace("/", ".").replace(".py", "")[2:]
        await bot.load_extension(module)


async def main():
  async with bot:
    await load_cogs()
    await bot.start(TOKEN)

asyncio.run(main())
