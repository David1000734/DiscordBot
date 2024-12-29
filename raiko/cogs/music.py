import discord
from discord.ext import commands
import asyncio
import yt_dlp


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        # Dictionary, store our queue of songs
        self.queues = {}
        self.youtube_BaseURL = "youtube.com/watch?"

        self.voice_clients = {}
        self.yt_dl_ops = {'format': 'bestaudio/best', 'noplaylist': 'True'}
        self.ytdl = yt_dlp.YoutubeDL(self.yt_dl_ops)
        self.ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',   # noqa: E501
                               'options': '-vn'}

        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.vc = None

    # *************** Non-command/event Functions ***************
    def check_queue(self, ctx, id):
        # if id is in our dictionary, and it is non-null
        if self.queues[id] != []:
            # Non-null, play the next song
            voice = ctx.guild.voice_client
            source = self.queues[id].pop(0)      # pop from top of stack
            # player = voice.play(source)     # play song
            voice.play(source)     # play song

    def search_yt(self, item):
        try:
            self.ytdl.extract_info
            info = self.ytdl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]   # noqa: E501
        except Exception:
            return False
        return {'source': info['url'], 'title': info['title']}

    def play_Next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.ffmpeg_options), after=lambda e: self.play_Next())    # noqa: E501
        else:
            self.is_playing = False

    async def play_Music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc is None:
                    await ctx.send("Could not connect to voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.ffmpeg_options), after=lambda e: self.play_Next())    # noqa: E501
        else:
            self.is_playing = False

    @commands.command(name="play",
                      aliases=["p", "playing"],
                      help="Play the selected song from youtube")
    async def play(self, ctx, *args):
        # Build string by adding space to each argument provided
        query = " ".join(args)
        voice_channel = ctx.author.voice

        try:
            # Check to see if user is in a voice channel.
            if voice_channel is None:
                # If not, prompt to join one
                raise AttributeError(ctx.message.author.nick +
                                     " is not currently in a channel.")

            # See if we are only currently paused
            if self.is_paused:
                self.vc.resume()
            else:
                song = self.search_yt(query)
                # if type(song) == type(True):
                if song is True:
                    await ctx.send("Could not download song. Incorrect format, try a different keyword.")   # noqa: E501
                else:
                    await ctx.send("Song added to queue")
                    self.music_queue.append([song, voice_channel.channel])

                    if self.is_playing is False:
                        await self.play_Music(ctx)
        except AttributeError as e:
            await ctx.send("Error: %s" % e)

    @commands.command(name="skip",
                      aliases=["s"],
                      help="Skips the currently played song")
    async def skip(self, ctx, *args):
        if self.vc is not None and self.vc:
            self.vc.stop()
            await self.play_Music(ctx)

    @commands.command(name="queue",
                      aliases=["q"],
                      help="Display all songs in queue")
    async def queue(self, ctx):
        retval = ""

        for i in range(0, len(self.music_queue)):
            if (i > 4):
                break
            retval += self.music_queue[i][0]['title'] + '\n'

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue.")

    @commands.command(name="clear",
                      aliases=["c", "bin"],
                      help="Stops current song and clear queue")
    async def clear(self, ctx, *args):
        if self.vc is not None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared")

    async def music_Play_URL(self, ctx, url):
        voice_client = None
        try:
            # Try to make a voice client in this server
            voice_client = await ctx.author.voice.channel.connect()

            # Successful create, store info
            self.voice_clients[voice_client.guild.id] = voice_client
        except Exception:
            # If one already exist, grab it
            voice_client = self.voice_clients[ctx.guild.id]

        # Function will run independently from the program
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=False))    # noqa: E501

        song = data['url']
        player = discord.FFmpegPCMAudio(song, **self.ffmpeg_options)

        voice_client.play(player)

    # *************** Discord command/event Functions ***************
    @commands.command(pass_context=True)
    async def leave(self, ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            self.is_playing = False
            self.is_paused = False
            await ctx.send("I left the voice chat.")
        else:
            await ctx.send("Currently not in a voice chat. Unable to leave.")

    @commands.command(pass_content=True)
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if (voice.is_playing()):
            voice.pause()
            self.is_playing = False
            self.is_paused = True
        else:
            await ctx.send("No audio playing.")

    @commands.command(pass_content=True)
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if (voice.is_paused()):
            voice.resume()
            self.is_playing = True
            self.is_paused = False
        else:
            await ctx.send("No audio is paused.")

    @commands.command(pass_content=True)
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        voice.stop()
        await ctx.send("Audio has been stopped.")

    # @commands.command(pass_content = True)
    # async def play(self, ctx, *arg):
    #     voice = ctx.guild.voice_client
    #     source = FFmpegPCMAudio(arg)

    #     # Check to see if there is anything currently playing
    #     if (voice.is_playing()):
    #         # Is currently playing, place in queue.

    #         # Get the id of the discord server
    #         guild_id = ctx.message.guild.id

    #         # Attempt to find our serverID in current queue
    #         if (guild_id in self.queues):
    #             # Found, so just add into queue to be played next
    #             self.queues[guild_id].append(source)
    #         else:
    #             # Not found, nothing in queue. Add one
    #             self.queues[guild_id] = [source]

    #         await ctx.send("Added to queue")
    #     else:
    #         # Not currently playing. So play the song

    #         # After the initial run, check the function (check_queue) to
    #         # see if there is any queues songs. If there is, play it, else end.   # noqa: E501
    #         player = voice.play(source, \
    #                 after = lambda x = None: self.check_queue(ctx, ctx.message.guild.id)) # noqa: E501


async def setup(client):
    await client.add_cog(Music(client))
