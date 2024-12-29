from raiko import client, load_extensions
from raiko.types import parameters  # noqa F401


# Upon bot is ready, exectute this constructor event
@client.event
async def on_ready():
    # load all cogs from "cogs" folder
    await load_extensions()

    # parameters.init()       # DEBUG
    # Do stuff with global variable in parameters
    # print(parameters.server_list)       # DEBUG

    print("Hello I'm ready, enter a command!")
    print("------------------------------")
    pass
# Constructor, END

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
