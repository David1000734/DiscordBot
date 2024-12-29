import os
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

discord_botspam = os.getenv("DISCORD_BOTSPAM")


class Control(commands.Cog):
    def __init__(self, client):
        self.client = client

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

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'user {member} has been kicked from the server.')

    @kick.error
    async def kick_error(self, ctx, error):
        if (isinstance(error, commands.MissingPermissions)):
            await ctx.send("You don't have permission to kick.")
            return
        await ctx.send("Something went wrong.")

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned.')

    @ban.error
    async def ban_error(self, ctx, error):
        if (isinstance(error, commands.MissingPermissions)):
            await ctx.send("You don't have permission to ban.")

    @commands.command()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.unban(member, reason=reason)
        await ctx.send(f'User {member} has been unbanned.')


async def setup(client):
    await client.add_cog(Control(client))
