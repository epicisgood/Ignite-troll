import asyncio
import datetime
import pytz

import discord
from discord import Forbidden
from discord import app_commands
from discord.ext import commands

class Reminder_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name="reminder")
    @app_commands.describe(seconds="The time to set the reminder for", reminder="The reminder to set")
    async def reminder(self, interaction: discord.Interaction, seconds: int, reminder: str):
        try:
            await interaction.response.send_message(f"Reminder set for {seconds} seconds!")
            await asyncio.sleep(int(seconds))
            await interaction.user.send(reminder)
        except Forbidden:
            await interaction.response.send_message("I do not have permission to send messages in this channel.")
    @app_commands.command(name="epooch", description="Convert epooch to time")
    @app_commands.describe(epooch="Command group for epoch time conversion")
    async def convert_epoch(self,interaction: discord.Interaction, epooch: str):
        # Remove any non-numeric characters from the input
        epoch_time = ''.join(filter(str.isdigit, epooch))

        try:
            epoch_time = int(epoch_time[:10])
            est = pytz.timezone('US/Eastern') 
            est_time = datetime.datetime.utcfromtimestamp(epoch_time).replace(tzinfo=pytz.utc).astimezone(est) 
            readable_time = est_time.strftime('%Y, %b, %d, %I:%M:%S %p')
            await interaction.response.send_message(readable_time)
        except ValueError:
            await interaction.response.send_message('Invalid epoch time provided.')




