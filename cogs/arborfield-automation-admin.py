import discord
import asyncio
import datetime
import os

from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

class AdminCog(commands.Cog, name="Admin Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="ban", description="Ban a member")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @app_commands.describe(member="The member to ban", reason="The reason for the ban")
    async def ban_command(self, ctx: commands.Context, member: discord.Member = None, *, reason: str = None):
        if member == None and reason == None:
            embed=discord.Embed(
                title='**Command: Ban**',
                type='rich',
                colour=discord.Color.blue(),
                description='''**Aliases:** /ban
**Description:** Ban a member
**Cooldown:** 3 seconds
**Usage:**
!ban <user> <reason>
**Example:**
!ban @B_aconxv spamming
'''
            )
        else:
            #channel = ctx.bot.get_channel(os.getenv("LogChannel"))
            await member.ban(reason=reason)
            embed=discord.Embed(
                colour=discord.Color.green(),
                description=f''':white_check_mark: ***{member} was banned*** | {reason}'''
                )
            #embed2=discord.Embed(
            #    colour=discord.Color.red()
            #    )
            #embed2.set_author(name=f"Ban | {member}", icon_url=member.avatar_url)
            #embed2.add_field(name="User", value=f"{member.mention}", inline=True).add_field(name="Moderator", value=f"{ctx.author.mention}", inline=True).add_field(name="Reason", value=f"{reason}", inline=True)
            #embed2.set_footer(text=f"ID: {member.id}")
            #embed2.timestamp=datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            #await channel.send(embed=embed2)
            pass
        pass

    @commands.hybrid_command(name="kick", description="Kick a member.")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @app_commands.describe(member="The member to kick", reason="The reason for kicking the member")
    async def kick_command(self, ctx: commands.Context, member: discord.Member = None, *, reason: str = None):
        if member == None and reason == None:
            embed=discord.Embed(
                title='**Command: !kick**',
                colour=discord.Color.blue(),
                description='''**Aliases: /kick**
**Description:** Kick a member.
**Cooldown:** 3 seconds
**Usage:** !kick <user> <reason>
**Example:** !kick @B_aconxv Spamming'''
            )
            await ctx.send(embed=embed)
        else:
            #channel = ctx.bot.get_channel(os.getenv("LogChannel"))
            await member.kick(reason=reason)
            embed=discord.Embed(
                colour=discord.Color.green(),
                description=f''':white_check_mark: ***{member} was kicked*** | {reason}'''
                )
            #embed2=discord.Embed(
            #    colour=discord.Color.red()
            #    )
            #embed2.set_author(name=f"Kick | {member}", icon_url=member.avatar_url)
            #embed2.add_field(name="User", value=f"{member.mention}", inline=True).add_field(name="Moderator", value=f"{ctx.author.mention}", inline=True).add_field(name="Reason", value=f"{reason}", inline=True)
            #embed2.set_footer(text=f"ID: {member.id}")
            #embed2.timestamp=datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            #await channel.send(embed=embed2)
            pass
        pass

    @commands.hybrid_command(name="unban", description="Unban a member")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @app_commands.describe(member="The member to unban")
    async def unban_command(self, ctx: commands.Context, *, member: discord.User = None):
        if member == None:
            embed=discord.Embed(
                title='**Command: !unban**',
                colour=discord.Color.blue(),
                description='''**Aliases:** /unban
**Description:** Unban a member
**Cooldown:** 3 seconds
**Usage:** !unban <user>
**Example:** !unban @B_aconxv'''
            )
            await ctx.send(embed=embed)
        else:
            #channel = ctx.bot.get_channel(os.getenv("LogChannel"))
            await ctx.guild.unban(member)
            embed=discord.Embed(
                colour=discord.Color.green(),
                description=f''':white_check_mark: ***{member} was unbanned***'''
                )
            #embed2=discord.Embed(
            #    colour=discord.Color.green()
            #    )
            #embed2.set_author(name=f"Unban | {member}", icon_url=member.avatar_url)
            #embed2.add_field(name="User", value=f"{member.mention}", inline=True).add_field(name="Moderator", value=f"{ctx.author.mention}", inline=True)
            #embed2.set_footer(text=f"ID: {member.id}")
            #embed2.timestamp=datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            #await channel.send(embed=embed2)
            pass
        pass

    @commands.hybrid_command(name="mute", description="Mute a member")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @app_commands.describe(member="The member to mute", time="The amount of time to mute the member for", reason="The reason for muting the member")
    async def mute_command(self, ctx: commands.Context, member: discord.Member = None, time: str = None, *, reason: str = None):
        if member == None and time == None and reason == None:
            embed=discord.Embed(
                title='**Command: !mute**',
                colour=discord.Color.blue(),
                description='''**Aliases:** /mute
**Description:** Mute a member
**Cooldown:** 3 seconds
**Usage:** !mute <user> <time> <reason>
**Example:** !mute @B_aconxv 1h Spamming'''
            )
            await ctx.send(embed=embed)
        else:
            #channel = ctx.bot.get_channel(os.getenv("LogChannel"))
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            if role == None:
                await ctx.guild.create_role(name="Muted")
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True, read_messages=True)
            await member.add_roles(role, reason=reason)
            embed=discord.Embed(
                colour=discord.Color.green(),
                description=f''':white_check_mark: ***{member} was muted*** | {reason}'''
                )
            #embed2=discord.Embed(
            #    colour=discord.Color.red()
            #    )
            #embed2.set_author(name=f"Mute | {member}", icon_url=member.avatar_url)
            #embed2.add_field(name="User", value=f"{member.mention}", inline=True).add_field(name="Moderator", value=f"{ctx.author.mention}", inline=True).add_field(name="Reason", value=f"{reason}", inline=True)
            #embed2.set_footer(text=f"ID: {member.id}")
            #embed2.timestamp=datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            #await channel.send(embed=embed2)
            if time != None:
                if time.endswith("s"):
                    time = int(time[:-1])
                    await asyncio.sleep(time)
                elif time.endswith("m"):
                    time = int(time[:-1])
                    time = time * 60
                    await asyncio.sleep(time)
                elif time.endswith("h"):
                    time = int(time[:-1])
                    time = time * 60 * 60
                    await asyncio.sleep(time)
                elif time.endswith("d"):
                    time = int(time[:-1])
                    time = time * 60 * 60 * 24
                    await asyncio.sleep(time)
            await member.remove_roles(role)

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminCog(bot))