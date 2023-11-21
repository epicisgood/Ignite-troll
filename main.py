import os

import discord
from discord.ext import bridge

intents = discord.Intents.all()
client = bridge.Bot(command_prefix="!", intents=intents)


my_secret = os.environ['TOKEN']

@client.event
async def on_ready():
  print(f"{client.user} is working")
  



client.load_extensions("cogs","school")

client.run(my_secret)
