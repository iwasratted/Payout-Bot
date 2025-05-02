import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import random

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create a bot instance with the necessary intents
intents = discord.Intents.default()
intents.message_content = True  # To allow reading message content
bot = commands.Bot(command_prefix="!", intents=intents)

# Registering slash commands
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    # Syncing the commands to Discord
    await bot.tree.sync()
    print("Slash commands synced.")

# Slash command to give MCFA to a user
@bot.tree.command(name="give", description="Give a user MCFA")
async def give_mcfa(interaction: discord.Interaction, user: discord.User, amount: int):
    # Read the MCFA file
    with open('mcfa.txt', 'r') as file:
        mcfa_lines = file.readlines()

    # Ensure the amount is within the valid range
    if amount < 1 or amount > len(mcfa_lines):
        await interaction.response.send_message(f"Please provide a valid amount between 1 and {len(mcfa_lines)}.", ephemeral=True)
        return

    # Select random MCFA lines based on the requested amount
    selected_lines = random.sample(mcfa_lines, amount)

    # Send the MCFA lines to the user via DM
    try:
        await user.send('\n'.join(selected_lines))
        await interaction.response.send_message(f"Sent {amount} MCFA lines to {user.mention}!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message(f"Could not send DM to {user.mention}. They may have DMs disabled.", ephemeral=True)

# Run the bot with the provided TOKEN from .env file
bot.run(TOKEN)
