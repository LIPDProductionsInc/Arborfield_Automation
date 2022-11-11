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
                channel = self.bot.get_channel(1040322534454861904)
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
            channel = self.bot.get_channel(1040322534454861904)
            link = "https://discordapp.com/channels/{}/{}/{}".format(message.guild.id, message.channel.id, message.id)
            embed = discord.Embed(
                colour = discord.Color.red(),
                description = f'**Message deleted in** {message.channel.mention} [Jump to Message]({link})'
                )
            embed.add_field(name='Message:', value=f'{message.content}', inline=False)
            '''Get the person who deleted the message from the audit log and add it as an embed field'''
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

    pass

async def setup(bot):
    await bot.add_cog(EventsCog(bot))