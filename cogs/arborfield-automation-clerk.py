import discord
import chat_exporter
import io

from discord import app_commands
from discord.ext import commands

class ClerkCog(commands.Cog, name="Clerk Commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name='transcript', description='Get a transcript of the session')
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), commands.has_any_role(583496754712805376, 1087922383698014279))
    #@commands.has_role(763471193524535336)
    async def transcript(self, ctx: commands.Context) -> None:
        channel = ctx.bot.get_channel(1129577057697943682)
        if ctx.channel.name.startswith("council-session"):
            await ctx.send("`Saving...`")
            try:
                transcript = await chat_exporter.export(ctx.channel, tz_info='EST', fancy_times=True)
                transcript_file = discord.File(io.BytesIO(transcript.encode()),filename=f"{ctx.channel.name}.html")
                await channel.send(f"{ctx.channel.name}", file=transcript_file)
                transcript_file = discord.File(io.BytesIO(transcript.encode()),filename=f"{ctx.channel.name}.html")
                await ctx.send(file=transcript_file)
            except Exception as e:
                await ctx.send(f"`{e}`", ephemeral=True)
                print("Ignoring exception in command transcript: {}".format(e))
        else:
            raise commands.UserInputError("This command can only be used in a council session channel.")
        pass

    @commands.hybrid_command(name='bulletin', description='Post a bulletin of a council session')
    @commands.guild_only()
    @commands.has_any_role(583496754712805376, 1087922383698014279)
    @app_commands.describe(bulletin_number="The number of the session (1st, 2nd, 3rd, etc.)", bulletin_link="The link to the bulletin")
    async def bulletin(self, ctx: commands.Context, bulletin_number, bulletin_link) -> None:
        channel = ctx.bot.get_channel(625302673796890624)
        if ctx.channel.id == 1129573856609304606:
            message = await channel.send(f'## <:Arborfield:1054103937239756800> | {bulletin_number} SESSION BULLETIN \n\n{bulletin_link} \n\n@here')
            await ctx.send('Bulletin posted!', ephemeral=True)
            await message.publish()
        else:
            raise commands.UserInputError("This command can only be used in the clerk channel.")
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ClerkCog(bot))
