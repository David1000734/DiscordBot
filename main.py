# Import Discord!!!
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions

# Reddit API. Use async version since discord bot
import asyncpraw

# Import neccesary tokens
import misc.botInfo.apikey as key

intents = discord.Intents.all()
intents.members = True

reddit_instance = 0
reddit_post = []        # TEMP, store current posts

# Dictionary, store our queue of songs
queues = {}

def check_queue(ctx, id):
    # if id is in our dictionary, and it is non-null
    if queues[id] != []:
        # Non-null, play the next song
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)      # pop from top of stack
        player = voice.play(source)     # play song

async def check_emoji(msg):
    # Get just the name of the sent emoji, no colons here
    emoji_name = msg.content[1:-1]

    # Get the user that sent this message
    author = msg.guild.get_member(msg.author.id)
    # Check to see if they have premium. Only run if false
    if (author.premium_since is None):
        # Look through the entire list of emoji from the server
        for emoji in msg.guild.emojis:
            # If one of the correct name is found, send it
            if emoji_name == emoji.name:
                # First remove the old message
                await msg.delete()

                # Grab author's name
                nickName = msg.author.display_name

                # Create a webhook to send a message
                webhook = await msg.channel.create_webhook(name = nickName)

                # Use webhook to send message as the author
                await webhook.send(
                    str(emoji), username = nickName, avatar_url = msg.author.avatar
                )

                # Remove webhook after done using them
                webhooks = await msg.channel.webhooks()
                for webhook in webhooks:
                    await webhook.delete()

                    break           # Emoji found, end loop
            # emoji is in the server list
        # for, END
    # if premium, END

# Commands will be predicated with a '!', 
# Enables all intents from developer portal
client = commands.Bot(command_prefix = '!', intents = intents)

# Upon bot is ready, exectute this constructor event
@client.event
async def on_ready():
    # Reference the global variable instead of local
    global reddit_instance

    # Instance must be created within async function
    # to allow for async for to work.
    reddit_instance = asyncpraw.Reddit(
        client_id = key.red_clientID,
        client_secret = key.red_secret,
        username = key.red_username,
        password = key.red_password,
        user_agent = "test_bot"
    )

    print("Hello I'm ready, enter a command!")
    print("------------------------------")
    pass
# Constructor, END

# Event, someone joins the server
@client.event
async def on_member_join(member):
    channel = client.get_channel(key.disc_botSpam)
    await channel.send("Welcome %s! Hope you enjoy your stay" % \
                        member.name)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(key.disc_botSpam)
    await channel.send("Goodbye %s. You strange mammal" % \
                        member.name)

# Hello event, ctx: "inputs" from discord
@client.command()
async def hello(ctx):
    await ctx.send("Hello from the bot!")

@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('yaosobi.mp4')

        await ctx.send("Now playing.")
        player = voice.play(source)
    else:
        await ctx.send(ctx.message.author.nick + " is not currently in a channel.")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice chat.")
    else:
        await ctx.send("Currently not in a voice chat. Unable to leave.")

@client.command(pass_content = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    if (voice.is_playing()):
        voice.pause()
    else:
        await ctx.send("No audio playing.")

@client.command(pass_content = True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    if (voice.is_paused()):
        voice.resume()
    else:
        await ctx.send("No audio is paused.")

@client.command(pass_content = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    voice.stop()
    await ctx.send("Audio has been stopped.")           # DEBUG

@client.command(pass_content = True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg)

    # Check to see if there is anything currently playing
    if (voice.is_playing()):
        # Is currently playing, place in queue.

        # Get the id of the discord server
        guild_id = ctx.message.guild.id

        # Attempt to find our serverID in current queue
        if (guild_id in queues):
            # Found, so just add into queue to be played next
            queues[guild_id].append(source)
        else:
            # Not found, nothing in queue. Add one
            queues[guild_id] = [source]

        await ctx.send("Added to queue")
    else:
        # Not currently playing. So play the song

        # After the initial run, check the function (check_queue) to
        # see if there is any queues songs. If there is, play it, else end.
        player = voice.play(source, \
                            after = lambda x = None: check_queue(ctx, ctx.message.guild.id))

# Remove this queue. One is present inside play...
@client.command(pass_content = True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio(arg)

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = [source]

    await ctx.send("Added %d to queue" % guild_id)
# Remove this queue. One is present inside play...

@client.event
async def on_message(msg):

    if (not msg.author.bot):
        # Detect if an emoji is sent; by, colon at start and end
        if ((":" == msg.content[0]) and (":" == msg.content[-1])):
            # https://stackoverflow.com/questions/4664850/how-to-find-all-occurrences-of-a-substring
            await check_emoji(msg)        # process emoji command
        # if premium, END

    # Needed to ensure all other commands are called after.
    await client.process_commands(msg)

@client.command()
@has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.send(f'user {member} has been kicked from the server.')

@kick.error
async def kick_error(ctx, error):
    if (isinstance(error, commands.MissingPermissions)):
        await ctx.send("You don't have permission to kick.")
        return
    await ctx.send("Something went wrong.")

@client.command()
@has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'User {member} has been banned.')

@ban.error
async def ban_error(ctx, error):
    if (isinstance(error, commands.MissingPermissions)):
        await ctx.send("You don't have permission to ban.")

@client.command()
@has_permissions(ban_members = True)
async def unban(ctx, member: discord.Member, *, reason = None):
    await ctx.guild.unban(member, reason = reason)
    await ctx.send(f'User {member} has been unbanned.')

@client.command()
async def embed(ctx):
    embed = discord.Embed(title = "Goooooooooogle", url = "https://google.com",\
                          description = "Heres google", color = 0x5A2F26)
    embed.set_author(name = ctx.author.display_name, url = "https://bing.com", icon_url = ctx.author.avatar)
    embed.set_thumbnail(url = "https://w0.peakpx.com/wallpaper/208/932/HD-wallpaper-mountin-calm-lake-simple.jpg")
    embed.add_field(name = "Labradore", value = "Cute Dog", inline = True)
    embed.add_field(name = "Chihuahua", value = "Little Devil", inline = True)
    embed.set_footer(text = "Thanks for reading :)")

    await ctx.send(embed = embed)

@client.command()
async def reddit(ctx, arg):
    global reddit_post
    is_dup = False
    temp_arr = []

    subreddit = await reddit_instance.subreddit(arg)
    retrieved_post = subreddit.hot(limit = 5)
    async for submission in retrieved_post:
        # For more efficiency, use merge sort and then compare only one 
        for post in reddit_post:
            if (post.id == submission.id):
                is_dup = True
                break

        if (not is_dup):
            print("yes print.")
            await ctx.send(submission.title + ' '\
                  + submission.url +'\n' + "https://www.reddit.com" + submission.permalink)
        else:
            print("no print.")
            print("submissionID: %s, postID: %s" % (submission.id, post.id))
        reddit_post.append(submission)
        temp_arr.append(submission)
        is_dup = False
    reddit_post = temp_arr

# start of main()
client.run(key.disc_token)
