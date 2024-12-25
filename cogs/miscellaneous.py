import discord
from discord.ext import commands
import re
from discord import FFmpegPCMAudio
import asyncio


class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    # *************** Non-command/event Functions ***************
    async def check_emoji(self, msg):
        # Build the string for the bot to print it
        tempContent = msg.content

        # Check every emoji in server.
        for emoji in msg.guild.emojis:
            # We will need to update the message as we do replacements
            currStr = tempContent
            # Only do replacements if the emoji is animated
            if emoji.animated:
                # If it is animated, search for it in the message and replace
                # it with the emoji equivilant.
                tempContent = re.sub(rf":({emoji.name}):", str(emoji), currStr)

        if len(msg.content) < len(tempContent):
            await msg.delete()

            # Grab author's name
            nickName = msg.author.display_name

            # Create a webhook to send a message
            webhook = await msg.channel.create_webhook(name=nickName)

            # Use webhook to send message as the author
            await webhook.send(
                str(tempContent), username=nickName,
                avatar_url=msg.author.avatar
            )

            # Remove webhook after done using them
            webhooks = await msg.channel.webhooks()
            for webhook in webhooks:
                await webhook.delete()
            # emoji is in the server list

    # *************** Discord command/event Functions ***************
    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(
            title="Goooooooooogle", url="https://google.com",
            description="Heres google", color=0x5A2F26
        )
        embed.set_author(
            name=ctx.author.display_name, url="https://bing.com",
            icon_url=ctx.author.avatar
        )
        embed.set_thumbnail(
            url="https://w0.peakpx.com/wallpaper/208/932/HD-wallpaper-mountin-calm-lake-simple.jpg"  # noqa: E501
        )
        embed.add_field(name="Labradore", value="Cute Dog", inline=True)
        embed.add_field(name="Chihuahua", value="Little Devil", inline=True)
        embed.set_footer(text="Thanks for reading :)")

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, msg):
        # Get the user that sent this message
        author = msg.guild.get_member(msg.author.id)

        # Check to see if they have premium. Only run if false
        # Ignore all messages from a bot
        if (not msg.author.bot and author.premium_since is None):
            await self.check_emoji(msg)
        # if premium or bot, END

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # https://discordpy.readthedocs.io/en/latest/api.html#discord.on_voice_state_update
        # Only play if this is the first time the user joined a voice channel
        if (member.name == "chapnews" and before.channel is None):
            voice = await after.channel.connect()
            # player = voice.play(FFmpegPCMAudio("bombastic.mp3"))
            voice.play(FFmpegPCMAudio("bombastic.mp3"))
            await asyncio.sleep(6)
            await member.guild.voice_client.disconnect()


async def setup(client):
    await client.add_cog(Miscellaneous(client))
