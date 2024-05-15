import discord
from discord.ext import commands

# Import neccesary tokens
import apikey as key

intents = discord.Intents.all()
intents.members = True

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
        await channel.connect()
    else:
        await ctx.send(ctx.message.author.name + " is not currently in a channel.")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice chat.")
    else:
        await ctx.send("Currently not in a voice chat. Unable to leave.")

client.run(key.disc_token)
