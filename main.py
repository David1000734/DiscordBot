import discord
from discord.ext import commands
import os

# Import bot tokens
import misc.botInfo.apikey as key

intents = discord.Intents.all()
intents.members = True

# Commands will be predicated with a '!', 
# Enables all intents from developer portal
client = commands.Bot(command_prefix = '!', intents = intents)

# Upon bot is ready, exectute this constructor event
@client.event
async def on_ready():
    # load all cogs from "cogs" folder
    await load_extensions()

    print("Hello I'm ready, enter a command!")
    print("------------------------------")
    pass
# Constructor, END

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if (filename.endswith("py")):
            await client.load_extension("cogs." + filename[:-3])

# Start of main()
client.run(key.disc_token)
