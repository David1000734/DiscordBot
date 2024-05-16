import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

# Import neccesary tokens
import apikey as key

intents = discord.Intents.all()
intents.members = True

# Dictionary, store our queue of songs
queues = {}

def check_queue(ctx, id):
    # if id is in our dictionary, and it is non-null
    if queues[id] != []:
        # Non-null, play the next song
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)      # pop from top of stack
        player = voice.play(source)     # play song

# Commands will be predicated with a '!', 
# Enables all intents from developer portal
client = commands.Bot(command_prefix = '!', intents = intents)

# Upon bot is ready, exectute this constructor event
@client.event
async def on_ready():
    print("Hello I'm ready, enter a command!")      # DEBUG
    print("------------------------------")         # DEBUG
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
        await ctx.send(ctx.message.author.name + " is not currently in a channel.")

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

        if guild_id in queues:
            queues[guild_id].append(source)
        else:
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

client.run(key.disc_token)
