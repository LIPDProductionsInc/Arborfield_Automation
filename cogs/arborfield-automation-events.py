import discord
import datetime

from discord.ext import commands

class EventsCog(commands.Cog, name="Events Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            if before.channel.id == 854761365150629898:
                channel = self.bot.get_channel(1040629489803202560)
                link = "https://discordapp.com/channels/{}/{}/{}".format(before.guild.id, before.channel.id, before.id)
                embed = discord.Embed(
                    colour = discord.Color.blue(),
                    description = f'**Message edited in** {before.channel.mention} [Jump to Message]({link})'
                    )
                embed.add_field(name='Before:', value=f'{before.content}', inline=False)
                embed.add_field(name='After:', value=f'{after.content}', inline=False)
                embed.set_author(name=f'{before.author}', icon_url=before.author.avatar)
                embed.set_footer(text=f'ID: {before.author.id}')
                embed.timestamp = datetime.datetime.now()
                await channel.send(embed=embed)
                pass
            pass
        pass

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.channel.id == 854761365150629898:
            channel = self.bot.get_channel(1040629489803202560)
            link = "https://discordapp.com/channels/{}/{}/{}".format(message.guild.id, message.channel.id, message.id)
            embed = discord.Embed(
                colour = discord.Color.red(),
                description = f'**Message deleted in** {message.channel.mention} [Jump to Message]({link})'
                )
            embed.add_field(name='Message:', value=f'{message.content}', inline=False)
            async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
                if entry.target == message.author:
                    embed.add_field(name='Deleted By:', value=f'{entry.user.mention}', inline=False)
                    embed.add_field(name='ID:', value=f'{entry.user.id}', inline=True)
                    break
            embed.set_author(name=f'{message.author}', icon_url=message.author.avatar)
            embed.set_footer(text=f'ID: {message.author.id}')
            embed.timestamp = datetime.datetime.now()
            await channel.send(embed=embed)
            pass
        pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == 854761365150629898:
            for role in payload.member.roles:
                if role.id != 581574409832366086:
                    channel = self.bot.get_channel(payload.channel_id)
                    message = await channel.fetch_message(payload.message_id)
                    await message.remove_reaction(payload.emoji, payload.member)
        elif payload.channel_id == 947186552839237674:
            for role in payload.member.roles:
                if role.id == 581574602212507648:
                    guild = self.bot.get_guild(payload.guild_id)
                    message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                    if message.author.id == 1033859464488562788:
                        direct_message = "<:Arborfield:1054103937239756800> | **LEAVE OF ABSENCE REQUEST**\n\n"
                        embed = message.embeds[0]
                        footer = embed.footer.text
                        id = footer[4:]
                        member = guild.get_member(int(id))
                        if payload.emoji.name == '✅':
                            direct_message += f"The Arborfield {role.name.title()} has approved your leave of absence request.\n\n"
                            direct_message += "You cannot be in-game or active in other departments while on leave. You are **NOT** allowed to be in attendance of any council sessions while on your leave; however, once you return (if the session is still ongoing), you may \"enter\" the session (make sure you reply to the attendance message).\n\n"
                            direct_message += "If you are currently in attendance for a discord session upon this approval message, the current Presiding Officer will excuse you from the rest of the sessions and note it for the record.\n\n"
                            direct_message += f"Please contact {payload.member.mention} if you have any questions.\n\n*{payload.member.display_name}*\n*Arborfield {role.name.title()}*"
                            await member.send(direct_message)
                            print(f"{payload.member.display_name} approved {member.display_name}'s leave of absence request.")
                        elif payload.emoji.name == '❌':
                            direct_message += f"The Arborfield {role.name.title()} has **denied** your leave of absence request.\n\n"
                            direct_message += f"If you have any questions, please contact {payload.member.mention}.\n\n"
                            direct_message += f"*{payload.member.display_name}*\n*Arborfield {role.name.title()}*"
                            await member.send(direct_message)
                            print(f"{payload.member.display_name} denied {member.display_name}'s leave of absence request.")
                        else:
                            raise ValueError("Invalid emoji.")
                        pass
                    pass
                pass
            pass
        pass

    pass

async def setup(bot):
    await bot.add_cog(EventsCog(bot))