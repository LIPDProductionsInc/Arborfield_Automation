import discord
import aiohttp
import asyncio
import datetime
import json
import psutil
import sys
import traceback

from discord.ext import commands

class OwnerCog(commands.Cog, name="Owner Commands"):

    def __init__(self, bot):
        self.bot = bot
    
    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, *, cog: str):
        await ctx.send(f'**`Loading Cog: {cog}...`**')
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            print('Loading cog...')
            await asyncio.sleep(0.1)
            print('Cog name:')
            await asyncio.sleep(0.1)
            print(cog)
            await asyncio.sleep(2)
            await self.bot.load_extension(f'cogs.arborfield-automation-{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            print('Ignoring exception in loading cog {}:'.format(cog), file=sys.stderr)
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
        else:
            await ctx.send(f'**`Cog: {cog} has loaded successfully`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def _unload(self, ctx, *, cog: str):
        await ctx.send(f'**`Unloading Cog: {cog}...`**')
        await asyncio.sleep(2)
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            print('Unloading cog...')
            await asyncio.sleep(0.1)
            print('Cog name:')
            await asyncio.sleep(0.1)
            print(cog)
            await self.bot.unload_extension(f'cogs.arborfield-automation-{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            print('Ignoring exception in unloading cog {}:'.format(cog), file=sys.stderr)
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
        else:
            print(f'{cog} has unloaded successfully!')
            await ctx.send(f'**`Successfuly unloaded Cog: {cog}`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        print('Reloading cog...')
        await asyncio.sleep(0.1)
        print('Cog Name:')
        await asyncio.sleep(0.1)
        print(cog)
        try:
            await ctx.send(f'**`Unloading Cog: {cog}...`**')
            await self.bot.unload_extension(f'cogs.arborfield-automation-{cog}')
            await asyncio.sleep(2)
            await ctx.send(f'**`Loading Cog: {cog}...`**')
            await self.bot.load_extension(f'cogs.arborfield-automation-{cog}')
            await asyncio.sleep(1)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            print('Ignoring exception in reloading cog {}:'.format(cog), file=sys.stderr)
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
        else:
            await ctx.send(f'**`Successfully loaded {cog}`**')
            print(f'Cog: {cog} has loaded sucessfuly!')
            pass
        pass

    @commands.command(name='sync', hidden=True)
    @commands.is_owner()
    async def _sync(self, ctx) -> None:
        await ctx.send('`Syncing Slash commands...`')
        print('Syncing slash commands')
        synced = await ctx.bot.tree.sync()
        await ctx.send(f"`Synced {len(synced)} commands`")
        print(f"Synced {len(synced)} commands")
        return

    
    @commands.command(name='eval', hidden=True)
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')
                pass
            pass
        pass
    
    @commands.command(name='rules', hidden=True)
    @commands.is_owner()
    async def _rules(self, ctx):
        channel = self.bot.get_channel(625292260228988928)
        await ctx.message.delete()
        embed = discord.Embed(
            colour=discord.Colour.dark_red(),
            description='Welcome to the City of Arborfield discord server. Please read & abide by our server rules at all times.'
            )
        embed.set_author(name='City of Arborfield Rules')
        embed.add_field(name='Rule 1', value='Your server nickname should be set to your full Roblox username. Department affiliates may utilise a callsign in their nickname.', inline=False)
        embed.add_field(name='Rule 2', value='Be respectful to everyone. Usage of homophobic, transphobic, racist or generally offensive remarks are strictly prohibited.', inline=False)
        embed.add_field(name='Rule 3', value='Spam, via text or via voice, is strictly prohibited.', inline=False)
        embed.add_field(name='Rule 4', value='NSFW or inappropriate content is strictly prohibited. No exemptions.', inline=False)
        embed.add_field(name='Rule 5', value='Any type of malicious content, files or links are strictly prohibited.', inline=False)
        embed.add_field(name='Rule 6', value='Debates are allowed, however, must remain peaceful.', inline=False)
        embed.add_field(name='Rule 7', value='If you\'re not sure if what you\'re doing may be a violation of the rules, it\'s best to not do it. Use common sense when using this Discord.', inline=False)
        embed.set_image(url='https://media.discordapp.net/attachments/1031690226013319178/1033874598351097876/IMG_7066.png')
        embed.set_footer(text='Rules last updated on:')
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)
        pass

    @commands.command(name='info', hidden=True)
    @commands.is_owner()
    async def _info(self, ctx):
        channel = self.bot.get_channel(625292260228988928)
        await ctx.message.delete()
        embed = discord.Embed(
            colour=discord.Color.dark_red(),
            description='Welcome to the City of Arborfield official Discord server. Here, you can see what the city is up to and chat with other residents of the city. Announcements and events are regularly posted, so keep your eyes out!\n\nInterested in residency? Head to the <#579054644337180693> channel and follow the instructions there.\n\n[Server Invite](https://discord.gg/BbUmrpU969) \n[ROBLOX Group](https://www.roblox.com/groups/4441445/City-of-Arborfield)'
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/625302673796890624/1033876953972871178/unknown.png")
        embed.set_author(name='Arborfield Information')
        embed.add_field(name='Council Boards', value='[City Council](https://trello.com/b/gcBwNq7w) \n[City Records](https://trello.com/b/nOwFvREq/)', inline=False)
        #embed.add_field(name='Administration Boards', value='[Office of the Mayor](https://trello.com/b/pK66sdV7)', inline=False)
        embed.add_field(name='Other Links', value='[City Charter](https://trello.com/c/SAswB9G6)\n[Floor Rules](https://trello.com/c/EQRshcxM)\n[Twitter](http://twitter.com/CityofArborFS)', inline=False)
        embed.set_footer(text='Information last updated on:')
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)
        pass
    
    @commands.command(name='edit', hidden=True)
    @commands.is_owner()
    async def _edit(self, ctx, id, content):
        message = await channel.fetch_message(id)
        await message.edit(content=content)
        pass
    
    @commands.command(name='stats', hidden=True)
    @commands.is_owner()
    async def _stats(self, ctx):
        embed = discord.Embed(
            title='Arborfield Automation',
            type='rich',
            colour=discord.Color(0xFF9E00),
            description=f'''
Python Version: **{sys.version}**

Discord.py Version: **{discord.__version__}**

Current CPU Usage: **{psutil.cpu_percent()}**

Current RAM Usage: **{psutil.virtual_memory().percent}**

Average System Load: **{[x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]}%**

Latency: **{round(self.bot.latency * 1000)}**ms
'''
            )
        embed.set_footer(text=f"Developed by {self.bot.owner}")
        embed.set_thumbnail(url=str(self.bot.user.avatar))
        await ctx.send(embed=embed)
        pass

    @commands.command(name='restart', hidden=True)
    @commands.is_owner()
    async def _restart(self, ctx):
        await ctx.send('Restarting...')
        await self.bot.logout()
        pass

    @commands.hybrid_command(name='test', hidden=True)
    @commands.is_owner()
    async def _test(self, ctx):
        print(discord.InteractionType.application_command)
        await ctx.send('Sent')
        pass

    @commands.command(name='role-request', hidden=True)
    @commands.is_owner()
    async def _rolerequest(self, ctx):
        request_role = """
The following roles can be requested from <@155149108183695360> using `?rank` followed by the name of the role:
- <@&1000334009651429467>
- <@&1001014065822453800>
- <@&1001013976840294450>
        """
        notice = """
- Your up-to-date callsign or rank **MUST** be a part of your nickname
- Applicants, Candidates, Probationary Officers, etc., do **NOT** get department roles
        """
        embed = discord.Embed(
            title="**ROLE REQUEST**",
            colour=discord.Color.blue(),
            description="""
To be able to view all the necessary channels in this server, you must have the appropriate role(s).

If you have verified with <@426537812993638400> before, check your DM's, because most likely your roles have already been given to you.
If you have not verified with <@426537812993638400> before, run `/verify` and make sure to select the command from <@426537812993638400> to get yourself verified.
If you still have not gotten all the roles you need, open a <#999293384504119326> to request the roles you need. **ANY REQUESTS MADE IN THIS CHANNEL WILL NOT BE SEEN!!!**

If you need new roles, first run `/update` from <@426537812993638400> to get your roles updated, if that fails, open a <#999293384504119326>."""
        )
        embed.add_field(name='**Requestable Roles**', value=request_role, inline=True)
        embed.add_field(name='**Notice to Department Employees:**', value=notice, inline=True)
        embed.set_footer(text=f"Developed by {self.bot.owner}", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url=str(self.bot.user.avatar))
        await ctx.send(embed=embed)
        pass

    pass

async def setup(bot):
    await bot.add_cog(OwnerCog(bot))
