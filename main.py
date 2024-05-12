import discord
from discord.ext import commands
import apikey as key

debug_Separator = "------------------------------"

# Commands will be predicated with a '!', 
# Enables all intents from developer portal
client = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

# New Event
@client.event

# Upon bot is ready, exectute this constructor
async def on_ready():
    print("Hello I'm ready, enter a command!")      # DEBUG
    print(debug_Separator)                          # DEBUG
    pass
# Event, END

@client.command()

# Hello event, ctx: "inputs" from discord
async def hello(ctx):
    await ctx.send("Hello from the bot!")
# Command, END

client.run(key.disc_token)
