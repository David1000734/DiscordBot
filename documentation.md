# Documentation for developers
Helpful resources:
* Markdown Cheat Sheet: https://www.markdownguide.org/cheat-sheet/

# Installation
Youtube reference: https://www.youtube.com/watch?v=cCiqcu2NP8I&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP

Discord Documentation: https://discordpy.readthedocs.io/en/latest/

Reddit Documentation: https://apraw.readthedocs.io/en/latest/index.html

aPRAW: https://pypi.org/project/aPRAW/

### TEMP

Check Time: https://stackoverflow.com/questions/63625246/discord-py-bot-run-function-at-specific-time-every-day

Youtube Bot: https://www.youtube.com/watch?v=KgRNnTb5kZ0

Youtube Searching: https://stackoverflow.com/questions/64021026/youtube-search-command-for-discord-py

Youtube Bot #2: https://www.youtube.com/watch?v=dRHUW_KnHLs

### Steps for gettings started:

* Install discord library

    `pip install discord.py`
* Install async reddit library

    `pip install asyncpraw`
* Install asyncio

    `pip install asyncio`
* To run the bot

    `python3 main.py`

### Example codes
* Detecting a specific word in a message and sending an emoji. Static and animated
```python
@client.event
async def on_message(message):
    # Format for a custom emoji is as follows:
    # <:EmojiName:Emoji_ID>
    # For an animated emoji:
    # <a:EmojiName:Emoji_ID>
    if ("hi" in message.content):
        await message.channel.send("<:SCREEEM:1225961865449050183>")
        await message.channel.send("<a:bonk:1241902336113119232>")
```
NOTE: Emoji ID can be found by sending the emoji, copy link, paste, and copying the numbers that appear just before the .gif or .png

![alt text](/misc/images/emoji_id.png)

* Adding reactions to messages is very similar to sending an emoji
```python
    if ("noice" in msgContent):
        await message.add_reaction("<:SCREEEM:1225961865449050183>")
        await message.add_reaction("<a:bonk:1241902336113119232>")
```

* Changing nickname of the bot itself
``` python
    # Changing nickname to the author's nickname
    await msg.guild.me.edit(nick = msg.author.nick)
    await msg.guild.me.edit(nick = None)
```
* To get all new submissions
``` python
    subreddit = await reddit_instance.subreddit(arg)
    async for submission in subreddit.stream.submissions():
        print(submission.id)
```

* Difference when using cogs and no cogs. <strong>For commands</strong>
``` python
# Regular, no cogs
@client.command()

# Using cogs
@commands.command()
```

* Difference when using cogs and no cogs. <strong>For events</strong>
``` python
# Regular, no cogs
@client.event

# Using cogs
@ commands.Cog.listener()
```

* How to setup a new cog folder using Music as an example
``` python
# music.py, Cog file
import discord
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
    

async def setup(client):
    await client.add_cog(Music(client))

# Main file
import discord
from discord.ext import commands

async def on_ready():
    await client.load_extension("cogs." + "music")

bot.run(DISCORD_TOKEN)
```

* Remember to include the neccessary function at the end when <ins>re-defining</ins>
the on_message function. <br></br>
Note, in cogs, they are <strong>NOT</strong> redefined.
``` python
# Within main.py
@client.event
async def on_message(msg):
    # Do stuff here

    # Needed to ensure all other commands are called after.
    await client.process_commands(msg)
```

* Taking more than one argument
``` python
# Just taking two
@client.command()
async def args(ctx, arg1, arg2):
    await ctx.send("Command1: $s, Command2: $s" % (arg1, arg2))

# All passed as list
@client.command()
async def args(ctx, *args):
    await ctx.send("Commands: " + (','.join(args)))

# All passed as one argument
@client.command()
async def args(ctx, *, arg):
    await ctx.send(arg)
```

* Connecting to a server's webhook
``` python
from discord import SyncWebhook

webhook = SyncWebhook.from_url("URL of server's webhook bot")
webhook.send("Hello World!")
```
