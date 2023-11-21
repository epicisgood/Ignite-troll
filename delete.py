import asyncio
import discord
from discord import Forbidden
from discord.ext import commands, bridge

class Delete_commands(commands.Cog):
  def __init__(self, client):
    self.client = client

  @bridge.bridge_command(description="nukes a server ",
     channel_message="message to send in new channe",
     administrator=True)
  async def nuke(self, ctx, channel_names: str, channel_message: str):
    try:
      server = ctx.guild
      text_channels = [
        channel for channel in server.channels
        if isinstance(channel, discord.TextChannel)
        ]
      for channel in text_channels:
        await channel.delete()
      for i in range(25):
        new_channel = await server.create_text_channel(channel_names)
      for j in range(20):
        await new_channel.send(channel_message)
        await asyncio.sleep(0.5)
    except Forbidden:
      await ctx.send(content="I don't have permission to delete that channel",ephemeral=True)
    
  
  @bridge.bridge_command(aliases=["del all", "del_all", "del-all","delete_channels"],description="Deletes all textchannels in the server",
     administrator=True)
  async def delete_all(self, ctx):
    try:
      server = ctx.guild
    # Get a list of all text channels in the guild
      text_channels = [
      channel for channel in server.channels
      if isinstance(channel, discord.TextChannel)
      ]
      for channel in text_channels:
        await channel.delete()
        await server.create_text_channel("general")
    except Forbidden:
      await ctx.reply(content="I don't have permission to delete channels!", ephemeral=True)

  


def setup(client):
  client.add_cog(Delete_commands(client))