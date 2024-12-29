from raiko import client

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
