import discord
from discord.ext import commands

class Miscellaneous(commands.Cog):
    def __init__(self, client):
        self.client = client

    # *************** Non-command/event Functions ***************
    async def check_emoji(self, msg):
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

    # *************** Discord command/event Functions ***************
    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(title = "Goooooooooogle", url = "https://google.com",\
                            description = "Heres google", color = 0x5A2F26)
        embed.set_author(name = ctx.author.display_name, url = "https://bing.com", icon_url = ctx.author.avatar)
        embed.set_thumbnail(url = "https://w0.peakpx.com/wallpaper/208/932/HD-wallpaper-mountin-calm-lake-simple.jpg")
        embed.add_field(name = "Labradore", value = "Cute Dog", inline = True)
        embed.add_field(name = "Chihuahua", value = "Little Devil", inline = True)
        embed.set_footer(text = "Thanks for reading :)")

        await ctx.send(embed = embed)

    @commands.Cog.listener()
    async def on_message(self, msg):
        # Ignore all messages from a bot
        if (not msg.author.bot):
            # Detect if an emoji is sent; by, colon at start and end
            if ((":" == msg.content[0]) and (":" == msg.content[-1])):
                # https://stackoverflow.com/questions/4664850/how-to-find-all-occurrences-of-a-substring
                await self.check_emoji(msg)        # process emoji command
        # if premium, END

async def setup(client):
    await client.add_cog(Miscellaneous(client))