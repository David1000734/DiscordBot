import os
from discord.ext import commands

discord_botspam = os.getenv("DISCORD_BOTSPAM")


class Greetings (commands.Cog):
    def __init__(self, client):
        self.client = client

    # Hello event, ctx: "inputs" from discord
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello from the bot!")

    # Event, someone joins the server
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(discord_botspam)
        await channel.send("Welcome %s! Hope you enjoy your stay" %
                           (member.name))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(discord_botspam)
        await channel.send("Goodbye %s. You strange mammal" %
                           (member.name))


async def setup(client):
    await client.add_cog(Greetings(client))
