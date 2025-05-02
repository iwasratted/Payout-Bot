import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

# Load environment variables
load_dotenv()

# Create bot instance with custom prefixes and intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

# Function to read mcfa.txt
def get_mcfa():
    try:
        with open('mcfa.txt', 'r') as file:
            mcfa_lines = file.readlines()
        return mcfa_lines
    except FileNotFoundError:
        return []

# Command to give MCFA to a user
@bot.command()
async def give(ctx, user: discord.User, amount: int):
    # Get the MCFA lines from the file
    mcfa_lines = get_mcfa()

    # Error handling if the file is empty
    if not mcfa_lines:
        await ctx.send("Oops! The MCFA file is missing or empty. Please check the file.")
        return

    # Ensure the amount is within the valid range
    if amount < 1 or amount > len(mcfa_lines):
        await ctx.send("⚠️ Invalid amount, please pick a number within the range of available MCFA lines.")
        return
    
    # Select random MCFA lines
    mcfa_message = '\n'.join(random.sample(mcfa_lines, amount))

    # Create embed for a professional look
    embed = discord.Embed(
        title=f"🎉 Here are your {amount} MCFA(s) 🎉",
        description=mcfa_message,
        color=discord.Color.blue()
    )

    embed.set_footer(text="Enjoy your MCFA!", icon_url=ctx.author.avatar_url)

    try:
        # Send the message to the user via DM
        await user.send(embed=embed)
        await ctx.send(f"✨ Successfully sent **{amount} MCFA(s)** to {user.name}!")
    except discord.errors.Forbidden:
        await ctx.send(f"🚫 Couldn't send a DM to {user.name}. They might have DMs disabled.")

# Run the bot
keep_alive()  # Keeps the bot alive
bot.run(os.getenv('DISCORD_TOKEN'))
