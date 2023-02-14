import discord
import datetime

from discord.ext import commands
from datetime import timedelta
from typing import Literal

class EmergencyCog(commands.Cog, name="Arborfield Alert System Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="emergency-setup", description="Sets up the emergency alert system")
    async def emergency(self, ctx):
        if ctx.author == discord.utils.get(ctx.guild.roles, id=578723625390309390) or ctx.author == discord.utils.get(ctx.guild.roles, id=806150833842421760) or ctx.author == self.bot.owner:
            embed = discord.Embed(
                title="Arborfield Emergency Alert System",
                colour=discord.Colour.default(),
                description="This is the Arborfield Emergency Alert System. This system is used to alert the Arborfield community of any emergencies that may occur. This system is only used in the event of an emergency.\n\n:green_square: Green - **No Active Incidents**\n:yellow_square: Yellow - **City Notices & Incidents**\n:red_square: Red - **Active Emergency**"
            )
            await ctx.send(embed=embed)
            pass
        pass

    @commands.hybrid_command(name="emergency-send", description="Sends an emergency alert")
    @commands.check_any(commands.has_any_role(578723625390309390, 806150833842421760), commands.is_owner())
    @commands.guild_only()
    async def emergency_send(self, ctx, level:Literal["Green", "Yellow", "Red"], *, message: str = None):
        channel = ctx.bot.get_channel(999011771140546600)
        if level == "Green":
            embed = discord.Embed(
                title="Arborfield Emergency Alert System",
                colour=discord.Colour.green(),
                description="No active incidents."
            )
        elif level == "Yellow":
            embed = discord.Embed(
                title="Arborfield Emergency Alert System",
                colour=discord.Colour.gold(),
                description=f"{message}"
            )
            embed.set_footer(text=f"Issued by {ctx.author} at")
            embed.timestamp = datetime.datetime.now()
        elif level == "Red":
            embed = discord.Embed(
                title="Arborfield Emergency Alert System",
                colour=discord.Colour.red(),
                description=f"**Active Emergency**\n\n{message}"
            )
            embed.set_footer(text=f"Issued by {ctx.author} at")
            embed.timestamp = datetime.datetime.now()
            await ctx.send("Alert sent!", ephemeral=True)
        if ctx.channel.id == 999011771140546600:
            if ctx.interaction == None:
                await ctx.message.delete()
        await channel.send(embed=embed)
        pass

async def setup(bot):
    await bot.add_cog(EmergencyCog(bot))