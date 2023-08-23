import discord
import datetime
import sys
import traceback

from discord import app_commands
from discord.ext import commands
from datetime import timedelta
from typing import Literal

class LeaveofAbsenceModal(discord.ui.Modal, title="Leave of Absence Form"):

    startdate = discord.ui.TextInput(
        label="What is the start of your leave of absence?",
        style=discord.TextStyle.short,
        placeholder="Enter the start date here...",
        required=True
    )

    enddate = discord.ui.TextInput(
        label="What is the end of your leave of absence?",
        style=discord.TextStyle.short,
        placeholder="Enter the estimated end date here...",
        required=True
    )

    reason = discord.ui.TextInput(
        label="What is the reason for your leave of absence?",
        style=discord.TextStyle.long,
        placeholder="Enter the reason here...",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.client.get_channel(947186552839237674)
        embed = discord.Embed(
            title="Leave of Absence Request",
            colour=discord.Color.dark_blue()
        )
        embed.add_field(name="Start Date", value=self.startdate.value, inline=True)
        embed.add_field(name="Estimated End Date", value=self.enddate.value, inline=True)
        embed.add_field(name="Reason", value=self.reason.value, inline=False)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
        embed.set_footer(text=f"ID: {interaction.user.id}")
        embed.timestamp = datetime.datetime.now()
        message = await channel.send("<@&581574602212507648>", embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        await interaction.response.send_message(f"Your leave of absence has been submitted. You will be notified when it has been approved or denied.", ephemeral=True)
        pass

    async def on_error(self, error, interaction: discord.Interaction):
        await interaction.response.send_message(f"An error occurred while processing your leave of absence request. Please try again later.", ephemeral=True)
        print("Ignoring exception in modal {}:".format(self), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        pass

    pass

class CouncilCog(commands.Cog, name="Council Commands Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="council", description="Shows the current city council members.")
    @commands.guild_only()
    async def council(self, ctx):
        embed = discord.Embed(
            title="Arborfield City Council",
            description="Here is a list of the current city council members:",
            color=discord.Color.dark_red()
            )
        embed.add_field(name="Mayor", value=ctx.guild.get_role(578723625390309390).members[0].mention if len(ctx.guild.get_role(578723625390309390).members) > 0 else "VACANT", inline=False)
        embed.add_field(name="Deputy Mayor", value=ctx.guild.get_role(806150833842421760).members[0].mention if len(ctx.guild.get_role(806150833842421760).members) > 0 else "VACANT", inline=True)
        embed.add_field(name="Council Chairperson", value=ctx.guild.get_role(581574602212507648).members[0].mention if len(ctx.guild.get_role(581574602212507648).members) > 0 else "VACANT", inline=False)
        embed.add_field(name="City Council Members", value="\n".join([member.mention for member in ctx.guild.members if discord.utils.get(member.roles, id=581574409832366086) and not discord.utils.get(member.roles, id=578723625390309390) and not discord.utils.get(member.roles, id=806150833842421760) and not discord.utils.get(member.roles, id=581574602212507648)]), inline=True)
        embed.set_footer(text=f"Arborfield Automation | Developed by {self.bot.owner} | Information Accurate As Of:", icon_url=str(self.bot.user.avatar))
        embed.timestamp = datetime.datetime.now()
        await ctx.send(embed=embed)
        pass

    @app_commands.command(name="docket", description="Has the bot announce the next item on the city council docket.")
    @app_commands.guild_only()
    @commands.check_any(commands.is_owner(), commands.has_any_role(578723625390309390, 806150833842421760, 581574602212507648))
    @app_commands.describe(first="True of False: This is the first item on the docket for the session.", docket_item="The name of the item on the docket.", docket_link="The Trello link to the item on the docket.")
    async def docket(self, interaction:discord.Interaction, first:Literal["True", "False"], docket_item:str, docket_link:str):
        if interaction.channel.name.startswith("council-session"):
            if docket_link.startswith("https://trello.com/c/") or docket_link.startswith("http://trello.com/c/"):
                if first == "True":
                    await interaction.response.send_message(f"The first item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\nReply to this message with \"Read\" once you have read the docket item. (<@&581574409832366086>)")
                    print(f"{interaction.user} has announced the first item on the docket. Item: {docket_item.title()}")
                else:
                    await interaction.response.send_message(f"The next item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\nReply to this message with \"Read\" once you have read the docket item. (<@&581574409832366086>)")
                    print(f"{interaction.user} has announced the next item on the docket. Item: {docket_item.title()}")
            else:
                raise commands.UserInputError("The link provided is not a valid Trello link.")
        elif interaction.channel.id == 1124569802950840442:
            if first == "True":
                await interaction.response.send_message(f"The first item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\nReply to this message with \"Read\" once you have read the docket item.")
            else:
                await interaction.response.send_message(f"The next item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\nReply to this message with \"Read\" once you have read the docket item.")
                pass
            pass
        pass

    @commands.hybrid_command(name="session", description="Starts a city council session, either in-game or on Discord.")
    @commands.guild_only()
    @commands.has_any_role(578723625390309390, 806150833842421760, 581574602212507648)
    @app_commands.describe(session_type="The type of session to start. Either \"in-game\" or \"discord\".", session_number="The number of the Discord session.")
    async def session(self, ctx:commands.Context, session_type:Literal["In-Game", "Discord"], session_number:int = None) -> None:
        if session_type == "In-Game":
            channel = ctx.bot.get_channel(625302673796890624)
            message = await channel.send(f"**An in-game City Council Session is starting.**\n\nPlease join at the following link: <https://www.roblox.com/games/3965549333> \n\n@here")
            await message.publish()
            print(f"{ctx.author} has started an in-game city council session.")
        elif session_type == "Discord":
            channel = ctx.bot.get_channel(625302673796890624)
            overwrites = {
                ctx.guild.get_role(578723625390309390): discord.PermissionOverwrite(send_messages=True),
                ctx.guild.get_role(806150833842421760): discord.PermissionOverwrite(send_messages=True),
                ctx.guild.get_role(581574602212507648): discord.PermissionOverwrite(send_messages=True),
                ctx.guild.get_role(581574409832366086): discord.PermissionOverwrite(send_messages=True),
                ctx.guild.get_role(941904710955327508): discord.PermissionOverwrite(view_channel=True, send_messages=False),
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)
            }
            if session_number is None:
                session_number = "new"
            channel2 = await ctx.guild.create_text_channel(f"council-session-{session_number}", category=ctx.guild.get_channel(940191124037976064), overwrites=overwrites, reason="City Council Session Started")
            await channel.send(f"**A Discord City Council Session is starting.**\n\n{channel2.mention} \n\n@here")
            await channel2.send(f"<:Arborfield:1054103937239756800> {ctx.author.mention} has called the council into order on this {datetime.datetime.now().strftime('%A, %B %d, %Y')} at {datetime.datetime.now().strftime('%I:%M %p')}.If in attendance, make yourself present by stating \"I\". Once we reach a quorum, we will proceed.\n\nRefrain from deleting or editing your messages after they've been sent as this may interfere with the record of fact.\n\n(<@&581574409832366086>)")
            print(f"{ctx.author} has started a Discord city council session.")
        else:
            raise commands.BadArgument
        pass

    @commands.hybrid_command(name="end-session", description="Ends a city council session, either in-game or on Discord.")
    @commands.guild_only()
    @commands.has_any_role(578723625390309390, 806150833842421760, 581574602212507648)
    @app_commands.describe(session_type="The type of session to end. Either \"in-game\" or \"discord\".")
    async def end_session(self, ctx, session_type:Literal["In-Game", "Discord"]):
        if session_type == "Discord":
            if ctx.channel.name.startswith("council-session"):
                channel = ctx.bot.get_channel(1129573856609304606)
                await ctx.send("The session has been adjourned.")
                print(f"{ctx.author} has ended a Discord city council session.")
                overwrites = {
                    ctx.guild.get_role(583496754712805376): discord.PermissionOverwrite(send_messages=True),
                    ctx.guild.get_role(1087922383698014279): discord.PermissionOverwrite(send_messages=True),
                    ctx.guild.get_role(941904710955327508): discord.PermissionOverwrite(view_channel=True, send_messages=False),
                    ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)
                }
                await ctx.channel.edit(category=ctx.guild.get_channel(761730715024097311), reason="Session Ended", overwrites=overwrites, position=0)
                await channel.send(f"<@&583496754712805376> <@&1087922383698014279>\n\nHi, the session in {ctx.channel.mention} has been adjourned and is awaiting transcribing!")
            else:
                if ctx.interaction == None:
                    await ctx.message.delete()
                raise commands.UserInputError("This command can only be used in a council session channel.")
        elif session_type == "In-Game":
            channel = ctx.bot.get_channel(646541531523710996)
            await channel.send("The session has been adjourned.")
            print(f"{ctx.author} has ended an in-game city council session.")
            pass
        else:
            raise commands.BadArgument
        pass

    @commands.hybrid_command(name="floor", description="Gives a non-council member the floor to speak.")
    @commands.guild_only()
    @commands.has_any_role(578723625390309390, 806150833842421760, 581574602212507648)
    @app_commands.describe(member="The non-council member to give the floor to.")
    async def floor(self, ctx, member:discord.Member):
        if ctx.channel.name.startswith("council-session"):
            if discord.utils.get(member.roles, id=578723625390309390) or discord.utils.get(member.roles, id=806150833842421760) or discord.utils.get(member.roles, id=581574602212507648) or discord.utils.get(member.roles, id=581574409832366086):
                raise commands.BadArgument("This person can already speak in the session.")
            else:
                overwrite = discord.PermissionOverwrite(send_messages=True, embed_links=True)
                await ctx.channel.set_permissions(member, overwrite=overwrite)
                channel = ctx.bot.get_channel(1040629489803202560)
                embed = discord.Embed(
                    title="Floor Given",
                    colour=discord.Color.dark_red()
                )
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                embed.add_field(name="Floor Given To:", value=member.mention, inline=False)
                embed.add_field(name="Given By:", value=ctx.author.mention, inline=False)
                embed.set_footer(text=f"ID: {ctx.author.id}")
                embed.timestamp = datetime.datetime.now()
                await channel.send(embed=embed)
                await ctx.send(f"{member.mention}: you have the floor.")
                print(f"{ctx.author} has given {member} the floor.")
        else:
            if ctx.interaction == None:
                await ctx.message.delete()
            raise commands.UserInputError("The floor can only be given in a city council session channel.")
            pass
        pass

    @commands.hybrid_command(name="dismiss", description="Dismisses a non-council member from the floor.")
    @commands.guild_only()
    @commands.has_any_role(578723625390309390, 806150833842421760, 581574602212507648)
    @app_commands.describe(member="The non-council member to dismiss from the floor.")
    async def dismiss(self, ctx, member:discord.Member):
        if ctx.channel.name.startswith("council-session"):
            if discord.utils.get(member.roles, id=578723625390309390) or discord.utils.get(member.roles, id=806150833842421760) or discord.utils.get(member.roles, id=581574602212507648) or discord.utils.get(member.roles, id=581574409832366086):
                raise commands.BadArgument("This person cannot be dismissed like this in the session.")
            else:
                await ctx.channel.set_permissions(member, overwrite=None)
                channel = ctx.bot.get_channel(1040629489803202560)
                embed = discord.Embed(
                    title="Dismissed From Floor",
                    colour=discord.Color.dark_red()
                )
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                embed.add_field(name="User Dismissed:", value=member.mention, inline=False)
                embed.add_field(name="Dismissed By:", value=ctx.author.mention, inline=False)
                embed.set_footer(text=f"ID: {ctx.author.id}")
                embed.timestamp = datetime.datetime.now()
                await channel.send(embed=embed)
                await ctx.send(f"{member.mention} has been dismissed from the floor.", ephemeral=True)
                print(f"{ctx.author} has dismissed {member} from the floor.")
        else:
            if ctx.interaction == None:
                await ctx.message.delete()
            raise commands.UserInputError("This command can only be used in a council session channel.")
            pass
        pass

    @commands.hybrid_command(name="propose", description="Proposes a bill to the rest of city council.")
    @commands.guild_only()
    @commands.has_any_role(578723625390309390, 806150833842421760, 581574602212507648, 581574409832366086)
    @app_commands.describe(bill_name="The name of the bill bring proposed.", bill_link="The link to the bill being proposed.")
    async def propose(self, ctx, *, bill_name, bill_link):
        if ctx.channel.id == 1004455652623646880:
            if bill_link.startswith("https://docs.google.com/document/d/"):
                if ctx.interaction == None:
                    await ctx.message.delete()
                await ctx.send(f"**{ctx.author.mention}** has proposed a bill and is looking for co-sponsors. \n\n**Bill Name:** \"{bill_name}\" \n\n**Bill Link:** {bill_link} \n\nIf you would like to co-sponsor this bill, please respond with \"Support\" or \"Sponsor\" @here.")
                print(f"{ctx.author} has proposed a bill. Bill: {bill_name} | Link: {bill_link}")
            else:
                if ctx.interaction == None:
                    await ctx.message.delete()
                raise commands.UserInputError("The bill link must be a Google Docs link.")
        else:
            raise commands.UserInputError("This command can only be used in <#1004455652623646880>.")
            pass
    
    @commands.hybrid_command(name="legal-review", description="Send a proposal to the City Attorney's Office for review.")
    @commands.guild_only()
    @commands.has_any_role(578723625390309390, 806150833842421760, 581574602212507648, 581574409832366086)
    @app_commands.describe(trello_link="The link to the Trello card for the proposal.")
    async def legal_review(self, ctx, trello_link):
        if ctx.interaction == None:
            await ctx.message.delete()
        if ctx.channel.id == 1004455652623646880:
            if trello_link.startswith("https://trello.com/c/"):
                channel = ctx.bot.get_channel(940193302777565224)
                await channel.send(f"{trello_link} \n\n<@&940169028683563039> \n\nSent by: {ctx.author.mention}")
                await ctx.send("The proposal has been sent to the City Attorney's Office for review.", ephemeral=True)
                print(f"{ctx.author} has sent a proposal to the City Attorney's Office for review.")
            else:
                raise commands.BadArgument("The link provided needs to be a Trello card.")
        else:
            raise commands.UserInputError("This command can only be used in <#1004455652623646880>.")
            pass
        pass

    @commands.hybrid_command(name="send", description="Send a proposal to either the mayor for signature or the persiding officer for notification.")
    @commands.guild_only()
    @commands.has_any_role(578723625390309390, 806150833842421760, 581574602212507648, 940169028683563039)
    @app_commands.describe(trello_link="The link to the Trello card for the proposal.", location="The location to send the proposal to.")
    async def send(self, ctx, location: Literal["Mayor", "Docket"], trello_link:str):
        if location == "Mayor":
            if ctx.interaction == None:
                await ctx.message.delete()
            channel = self.bot.get_channel(940193511272251403)
            if ctx.channel.name.startswith("council-session"):
                if trello_link.startswith("https://trello.com/c/"):
                    if len(ctx.guild.get_role(987153251889721435).members) > 0:
                        ping = "<@987153251889721435>"
                    else:
                        ping = "<@&578723625390309390>"
                    await channel.send(f"{trello_link} \n\n{ping}")
                    await ctx.send("The bill has been sent to the mayor's office for signature.")
                    print(f"{ctx.author} has sent a bill to the mayor's office for signature.")
                else:
                    raise commands.BadArgument("The link provided needs to be a Trello card.")
            elif ctx.channel.id == 947186552839237674:
                if trello_link.startswith("https://trello.com/c/"):
                    if len(ctx.guild.get_role(987153251889721435).members) > 0:
                        ping = "<@987153251889721435>"
                    else:
                        ping = "<@&578723625390309390>"
                    await channel.send(f"{trello_link} \n\n{ping}")
                    await ctx.send("Proposal sent to the mayor's office for signature.", ephemeral=True)
                    print(f"{ctx.author} has sent a proposal to the mayor's office for signature.")
                else:
                    raise commands.BadArgument("The link provided needs to be a Trello card.")
            else:
                raise commands.UserInputError("This command can only be used in a council session")
                pass
        elif location == "Docket":
            if discord.utils.get(ctx.author.roles, id=940169028683563039):
                if ctx.channel.id == 940193302777565224:
                    if ctx.interaction == None:
                        await ctx.message.delete()
                    channel = ctx.bot.get_channel(947186552839237674)
                    if trello_link.startswith("https://trello.com/c/"):
                        await channel.send(f"{trello_link} \n\n <@&581574602212507648> Approved and added to the docket.")
                        await ctx.send("Presiding officer notified.", ephemeral=True)
                        print(f"{ctx.author} has sent a proposal to the presiding officer.")
                    else:
                        raise commands.BadArgument("The link provided needs to be a Trello card.")
                else:
                    raise commands.UserInputError("This command can only be used in <#940193302777565224>.")
                    pass
            else:
                raise commands.MissingRole(missing_role=940169028683563039)
                pass
        else:
            raise commands.BadArgument("The location provided needs to be either Mayor or Docket.")
            pass
        pass

    @commands.hybrid_command(name="debate", description="Opens or closes the floor for debate on a proposal.")
    @commands.guild_only()
    @commands.has_any_role(578723625390309390, 806150833842421760, 581574602212507648)
    @app_commands.describe(status="The status of the debate.")
    async def debate(self, ctx, status: Literal["Open", "Close"]):
        if ctx.channel.name.startswith("council-session"):
            if ctx.interaction == None:
                await ctx.message.delete()
            await ctx.send(f"The floor is now {status.lower()} for debate. {f'<@&581574409832366086>' if status == 'Open' else ''}")
            print(f"{ctx.author} has {status.lower()}ed the floor for debate.")
        else:
            raise commands.UserInputError("This command can only be used in a council session.")
            pass

    @commands.hybrid_command(name="charter", description="Sends a link to the City Charter.")
    @commands.guild_only()
    async def charter(self, ctx):
        await ctx.send("Current City Charter: \n <https://trello.com/c/SAswB9G6/>")
        pass

    @commands.hybrid_command(name="template", description="Sends a link to the Trello card proposal template.")
    @commands.guild_only()
    @commands.has_any_role(578723625390309390, 806150833842421760, 581574602212507648, 581574409832366086)
    async def template(self, ctx):
        await ctx.send("Here is the link to the Bill Templates: \n <https://trello.com/c/qTPWo19z/>")
        pass

    @app_commands.command(name="loa", description="Submit a leave of absence request.")
    @app_commands.guild_only()
    @app_commands.check_any(app_commands.is_owner(), app_commands.has_any_role(581574409832366086))
    async def loa(self, interaction: discord.Interaction):
        await interaction.send_modal(LeaveofAbsenceModal())
        pass

    pass

async def setup(bot):
    await bot.add_cog(CouncilCog(bot))
