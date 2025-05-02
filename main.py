import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

# Load environment variables from .env file
load_dotenv()

# Create bot instance with intents and command prefix
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

# Function to read MCFA lines from file
def get_mcfa():
    """Reads MCFA data from mcfa.txt."""
    try:
        with open('mcfa.txt', 'r') as file:
            mcfa_lines = file.readlines()
        return mcfa_lines
    except FileNotFoundError:
        return []

# Command to give MCFA to a user
@bot.command()
async def give(ctx, user: discord.User, amount: int):
    """Gives MCFA to a user in a nice format."""
    # Get MCFA lines from the file
    mcfa_lines = get_mcfa()

    # Handle case if mcfa.txt is missing or empty
    if not mcfa_lines:
        await ctx.send("⚠️ Error: The MCFA file is missing or empty. Please check the file!")
        return

    # Validate that the requested amount is within the range of available MCFA
    if amount < 1 or amount > len(mcfa_lines):
        await ctx.send("❌ Invalid amount. Please choose a number within the range of available MCFA lines.")
        return
    
    # Select random MCFA lines to send to the user
    selected_mcfa = random.sample(mcfa_lines, amount)
    mcfa_message = '\n'.join(selected_mcfa)

    # Create an embed for a professional and visually appealing message
    embed = discord.Embed(
        title=f"🎉 You've received {amount} MCFA(s) 🎉",
        description=mcfa_message,
        color=discord.Color.blue()
    )

    embed.set_footer(text="Enjoy your MCFA!", icon_url=ctx.author.avatar_url)

    try:
        # Send the MCFA embed to the user via DM
        await user.send(embed=embed)
        await ctx.send(f"✅ Successfully sent **{amount} MCFA(s)** to {user.name}!")
    except discord.errors.Forbidden:
        await ctx.send(f"🚫 Couldn't send a DM to {user.name}. They may have DMs disabled.")

# On ready event to indicate the bot has successfully logged in
@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')

# On error event to catch unexpected errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Unknown command. Use `/help` for available commands.")
    else:
        await ctx.send("❌ An unexpected error occurred. Please try again later.")
        print(f"Error: {error}")

# Run the bot
keep_alive()  # Keeps the bot alive
bot.run(os.getenv('DISCORD_TOKEN'))
