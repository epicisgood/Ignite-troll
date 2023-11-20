import os

import discord
from discord.ext import commands
import discord.utils

from cogs import Simple_commands, Troll_commands
from school import Link_commands


intents = discord.Intents.all()
client = commands.Bot(command_prefix=".", intents=intents)
my_secret = os.environ['TOKEN']

@client.event
async def on_ready():
  print(f"{client.user} is working")
  await load_cogs()
  try:
    synced = await client.tree.sync()
    print(f"Synced {len(synced)} commands")
  except Exception as e:
    print(e)


async def load_cogs():
  await client.wait_until_ready()
  try:
      simple_command_cog = Simple_commands(client)
      troll_commands_cog = Troll_commands(client)
      link_command_cog = Link_commands(client)
      await client.add_cog(simple_command_cog)
      await client.add_cog(troll_commands_cog)
      await client.add_cog(link_command_cog)
  except Exception as e:
      print(f"Error loading cogs: {e}")










client.run(my_secret)
