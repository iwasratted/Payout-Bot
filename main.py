import keep_alive
keep_alive.keep_alive()

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import random

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create bot instance with necessary intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Event triggered when bot is ready
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} slash command(s)')
    except Exception as e:
        print(f'❌ Error syncing commands: {e}')

# Slash command to give MCFA lines via DM
@bot.tree.command(name="give", description="Give a user MCFA lines")
async def give_mcfa(interaction: discord.Interaction, user: discord.User, amount: int):
    try:
        with open('mcfa.txt', 'r') as file:
            mcfa_lines = file.readlines()

        if amount < 1 or amount > len(mcfa_lines):
            await interaction.response.send_message(f"⚠️ Enter a valid amount between 1 and {len(mcfa_lines)}.", ephemeral=True)
            return

        selected_lines = random.sample(mcfa_lines, amount)
        await user.send('\n'.join(selected_lines))
        await interaction.response.send_message(f"📤 Sent {amount} MCFA line(s) to {user.mention}.", ephemeral=True)

    except discord.Forbidden:
        await interaction.response.send_message("🚫 Cannot DM that user. They may have DMs disabled.", ephemeral=True)
    except FileNotFoundError:
        await interaction.response.send_message("❌ `mcfa.txt` file not found.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ An unexpected error occurred: {e}", ephemeral=True)

# Run bot
bot.run(TOKEN)
