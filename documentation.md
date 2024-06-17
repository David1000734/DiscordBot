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

* Install the base discord library

    `pip install discord.py`
* Install async reddit library

    `pip install asyncpraw`
* Install 
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