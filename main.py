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
    for filename in os.listdir('./cogs'):
        if (filename.endswith("py")):
            await client.load_extension("cogs." + filename[:-3])
    # Load cogs, END

# Start of main()
if (__name__ == "__main__"):
    import os

    # Import discord token
    discord_token = os.getenv("DISCORD_TOKEN")

    if (discord_token is not None):
        client.run(discord_token)
    else:
        print("Unable to find Discord Token.")
    # Main, END
