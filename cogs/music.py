import discord
from discord.ext import commands
from discord import FFmpegPCMAudio      # Play audio

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        # Dictionary, store our queue of songs
        self.queues = {}

    def check_queue(self, ctx, id):
        # if id is in our dictionary, and it is non-null
        if self.queues[id] != []:
            # Non-null, play the next song
            voice = ctx.guild.voice_client
            source = self.queues[id].pop(0)      # pop from top of stack
            player = voice.play(source)     # play song

    @commands.command(pass_context = True)
    async def join(self, ctx):
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('yaosobi.mp4')

            await ctx.send("Now playing.")
            player = voice.play(source)
        else:
            await ctx.send(ctx.message.author.nick + " is not currently in a channel.")

    @commands.command(pass_context = True)
    async def leave(self, ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("I left the voice chat.")
        else:
            await ctx.send("Currently not in a voice chat. Unable to leave.")

    @commands.command(pass_content = True)
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)

        if (voice.is_playing()):
            voice.pause()
        else:
            await ctx.send("No audio playing.")

    @commands.command(pass_content = True)
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)

        if (voice.is_paused()):
            voice.resume()
        else:
            await ctx.send("No audio is paused.")

    @commands.command(pass_content = True)
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)

        voice.stop()
        await ctx.send("Audio has been stopped.")           # DEBUG

    @commands.command(pass_content = True)
    async def play(self, ctx, arg):
        voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(arg)

        # Check to see if there is anything currently playing
        if (voice.is_playing()):
            # Is currently playing, place in queue.

            # Get the id of the discord server
            guild_id = ctx.message.guild.id

            # Attempt to find our serverID in current queue
            if (guild_id in self.queues):
                # Found, so just add into queue to be played next
                self.queues[guild_id].append(source)
            else:
                # Not found, nothing in queue. Add one
                self.queues[guild_id] = [source]

            await ctx.send("Added to queue")
        else:
            # Not currently playing. So play the song

            # After the initial run, check the function (check_queue) to
            # see if there is any queues songs. If there is, play it, else end.
            player = voice.play(source, \
                    after = lambda x = None: self.check_queue(ctx, ctx.message.guild.id))

async def setup(client):
    await client.add_cog(Music(client))