import discord
from discord.ext import commands
from discord import FFmpegPCMAudio      # Play audio
import asyncio
import yt_dlp

import misc.customException as ex

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        # Dictionary, store our queue of songs
        self.queues = {}

        self.voice_clients = {}
        self.yt_dl_ops = {'format': 'bestaudio/best'}
        self.ytdl = yt_dlp.YoutubeDL(self.yt_dl_ops)
        self.ffmpeg_options = {'options': '-vn'}

    # *************** Non-command/event Functions ***************
    def check_queue(self, ctx, id):
        # if id is in our dictionary, and it is non-null
        if self.queues[id] != []:
            # Non-null, play the next song
            voice = ctx.guild.voice_client
            source = self.queues[id].pop(0)      # pop from top of stack
            player = voice.play(source)     # play song

    async def music_Play_URL(self, ctx, url):
        voice_client = None
        try:
            # Try to make a voice client in this server
            voice_client = await ctx.author.voice.channel.connect()

            # Successful create, store info
            self.voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            # If one already exist, grab it
            voice_client = self.voice_clients[ctx.guild.id]

        # Function will run independently from the program
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download = False))

        song = data['url']
        player = discord.FFmpegPCMAudio(song, **self.ffmpeg_options)

        voice_client.play(player)
    
    async def music_Pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)

        if (voice.is_playing()):
            voice.pause()
        else:
            await ctx.send("No audio playing.")

    async def music_Resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)

        if (voice.is_paused()):
            voice.resume()
        else:
            await ctx.send("No audio is paused.")
        
    async def music_Stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)

        if voice:
            voice.stop()
            await self.music_Leave(ctx)
            await ctx.send("Audio has been stopped.")
        else:
            raise ex.InvalidCommand("Not currently in voice. Unable to leave.")
    
    async def music_Leave(self, ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()

    # *************** Discord command/event Functions ***************
    @commands.command()
    async def music(self, ctx, *arg):
        # Main entry point for music
        print(arg)
        try:
            match arg[0].lower():
                case "play":
                    await self.music_Play_URL(ctx, arg[1])
                
                case "pause":
                    await self.music_Pause(ctx)

                case "resume":
                    await self.music_Resume(ctx)

                case "stop":
                    await self.music_Stop(ctx)

                case _:
                    raise IndexError()

        except IndexError as e:
            await ctx.send("Usage: !music [command]\n"+
                     "`!music help` for more info!")

        except ex.InvalidCommand as e:
            await ctx.send("Unable to complete \"%s\": %s" % \
                           (arg[0], e))

        except Exception as e:
            await ctx.send("Error: %s" % e)
            raise

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