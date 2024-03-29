import discord
import datetime

from discord.ext import commands
from datetime import timedelta

class HelpCog(commands.Cog, name="Help Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="help")
    async def help(self, ctx, *, command: str = None):
        """Shows help about a command or the bot"""
        if command is None:
            embed = discord.Embed(
                title="Help",
                description="Here is a list of commands you can use with Arborfield Automation.",
                color=discord.Color.dark_red()
                )
            if discord.utils.get(ctx.author.roles, id=581574409832366086):
                embed.add_field(name="Council Commands", value="`propose`, `legal-review`, `charter`, `template`, `documents`", inline=False)
            if discord.utils.get(ctx.author.roles, id=578723625390309390) or discord.utils.get(ctx.author.roles, id=806150833842421760) or discord.utils.get(ctx.author.roles, id=581574602212507648):
                embed.add_field(name="Presiding Officer Commands", value="`docket`, `session`, `end-session`, `floor`, `dismiss`, `send`, `documents`, `elections`", inline=False)
            if discord.utils.get(ctx.author.roles, id=580403860724776980):
                embed.add_field(name="City Attorney Commands", value="`send`, `documents`", inline=False)
            if discord.utils.get(ctx.author.roles, id=583496754712805376) or discord.utils.get(ctx.author.roles, id=1087922383698014279):
                embed.add_field(name="City Clerk Commands", value="`transcript`, `bulletin`", inline=False)
            guild_perms = None
            if ctx.author.guild_permissions.ban_members:
                guild_perms = "`ban` `unban` "
            if ctx.author.guild_permissions.kick_members:
                guild_perms += "`kick` "
            if guild_perms is not None:
                embed.add_field(name="Moderation", value=f"{guild_perms}", inline=False)
            embed.add_field(name="Commands", value="`help` `ping` `serverinfo` `userinfo` `avatar`", inline=False)
            embed.set_footer(text=f"Arborfield Automation | Developed by {self.bot.owner}", icon_url=str(self.bot.user.avatar))
            await ctx.send(embed=embed)
        else:
            await ctx.send("Help regarding a specific command is not yet implemented.")
        pass

        @commands.command(name="beta-help", description="Shows help about a command or the bot (Beta version)", aliases=["help-beta"], hidden=True)
        @commands.is_owner()
        async def beta_help(self, ctx, *, command: str = None):
            embed = discord.Embed(
            title="Help",
            description="Here is a list of commands you can use with arborfield Automation.",
            color=discord.Color.dark_blue
            )
            embed.set_footer(text=f"Arborfield Automation | Developed by {self.bot.owner}", icon_url=str(self.bot.user.avatar))
            await ctx.send(embed=embed)
            if command is None:
                embed = discord.Embed(title="Help", description="Here's a list of all my commands:", color=0x00ff00)
                for cog in self.bot.cogs:
                    cog = self.bot.get_cog(cog)
                    if cog.qualified_name == "Owner Cog":
                        continue
                    if cog.qualified_name == "Help Cog":
                        continue
                    if cog.qualified_name == "Error Cog":
                        continue
                    if cog.qualified_name == "Admin Cog":
                        continue
                    if cog.qualified_name == "Commands Cog":
                        continue
                    embed.add_field(name=cog.qualified_name, value="`" + "`, `".join([c.name for c in cog.get_commands()]) + "`", inline=False)
                embed.set_footer(text="Use !beta-help <command> for more info on a command.")
                await ctx.send(embed=embed)
            else:
                if (cmd := self.bot.get_command(command)) is not None:
                    embed = discord.Embed(title=f"Help for {cmd.name}", description=cmd.help, color=0x00ff00)
                    embed.add_field(name="Usage", value=f"`{cmd.signature}`", inline=False)
                    if cmd.aliases:
                        embed.add_field(name="Aliases", value="`" + "`, `".join(cmd.aliases) + "`" or None, inline=False)
                    if isinstance(cmd, commands.Command):
                        embed.add_field(name="Cooldown", value=cmd._buckets._cooldown.per or None, inline=False)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("That command doesn't exist.")
                    pass
                pass
            pass

    pass

async def setup(bot):
    await bot.add_cog(HelpCog(bot))