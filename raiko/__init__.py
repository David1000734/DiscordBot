import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

# Commands will be predicated with a '!',
# Enables all intents from developer portal
client = commands.Bot(command_prefix='!', intents=intents)


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
    import os

    # Find the path to this file. 
    path_to_main = os.path.dirname(os.path.abspath(__file__))

    # Iterate through all files in cogs and add them
    for filename in os.listdir(path_to_main + '/cogs'):
        if ((filename != '__init__.py') and (filename.endswith("py"))):
            # File name without the .py at the end
            fn = filename[:-3]

            try:
                # For, python -m raiko
                await client.load_extension("raiko.cogs." + fn)
            except ModuleNotFoundError:
                print(f"No module found for raiko.cogs.{fn}\n" +
                      f"Try cogs.{fn}")
                # For, python raiko
                await client.load_extension("cogs." + fn)
        # If, END
    # For, END
# Load cogs, END
