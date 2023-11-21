import os

import discord
from discord.ext import bridge

intents = discord.Intents.all()
client = bridge.Bot(command_prefix="!", intents=intents)


my_secret = os.environ['TOKEN']

@client.event
async def on_ready():
  print(f"{client.user} is working")

@bridge.bridge_command(description="Test the ping of the bot")
async def ping(ctx):
  latency = round(ctx.client.latency * 1000, 2)
  await ctx.reply(content=f"Pong! Responded in {latency}ms!")


client.load_extensions("create","delete")

client.run(my_secret)
