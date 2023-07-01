import discord
import datetime

from discord import app_commands
from discord.ext import commands
from datetime import timedelta
from typing import Literal

class CouncilCog(commands.Cog, name="Council Commands Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="council", description="Shows the current city council members.")
    @commands.guild_only()
    async def council(self, ctx):
        embed = discord.Embed(
            title="Arborfield City Council",
            description="Here is a list of the current city council members:",
            color=discord.Color.dark_blue()
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
    @app_commands.check_any(app_commands.is_owner(), app_commands.has_any_role(578723625390309390, 806150833842421760, 581574602212507648))
    @app_commands.describe(first="True of False: This is the first item on the docket for the session.", docket_item = "The name of the item on the docket.", docket_link = "The Trello link to the item on the docket.")
    async def docket(self, interaction:discord.Interaction, first:Literal["True", "False"], docket_item:str, docket_link:str):
        if interaction.channel.id == 854761365150629898:
            if first == "True":
                await interaction.response.send_message(f"The first item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\nPlease react with <:aye:897181715141898240> one you have read the item. (<@&581574409832366086>)")
                react = await interaction.original_response()
                await react.add_reaction("aye:897181715141898240")
                print(f"{interaction.user} has announced the first item on the docket. Item: {docket_item.title()}")
            else:
                await interaction.response.send_message(f"The next item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\nPlease react with <:aye:897181715141898240> one you have read the item. (<@&581574409832366086>)")
                react = await interaction.original_response()
                await react.add_reaction("aye:897181715141898240")
                print(f"{interaction.user} has announced the next item on the docket. Item: {docket_item.title()}")
        elif interaction.channel.id == 1124569802950840442:
            if first == "True":
                await interaction.response.send_message(f"The first item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\nPlease react with <:aye:897181715141898240> one you have read the item.")
                react = await interaction.original_response()
                await react.add_reaction("aye:897181715141898240")
            else:
                await interaction.response.send_message(f"The next item on the docket is *\"{docket_item.title()}\"*. \n\n{docket_link} \n\nPlease react with <:aye:897181715141898240> one you have read the item.")
                react = await interaction.original_response()
                await react.add_reaction("aye:897181715141898240")
                pass
            pass
        pass

    @commands.hybrid_command(name="session", description="Starts a city council session, either in-game or on Discord.")
    @commands.guild_only()
    @commands.has_any_role(578723625390309390, 806150833842421760, 581574602212507648)
    @app_commands.describe(session_type="The type of session to start. Either \"in-game\" or \"discord\".")
    async def session(self, ctx, session_type:Literal["In-Game", "Discord"]):
        if session_type == "In-Game":
            channel = ctx.bot.get_channel(646541531523710996)
            await channel.send(f"**An in-game City Council Session is starting.**\n\nPlease join at the following link: <https://www.roblox.com/games/579211007/Stapleton-County-Firestone> \n\n@here")
            print(f"{ctx.author} has started an in-game city council session.")
        elif session_type == "Discord":
            channel = ctx.bot.get_channel(854761365150629898)
            channel2 = ctx.bot.get_channel(625302673796890624)
            await channel.send(f"{ctx.author.mention} has called this council into order at {datetime.datetime.now().strftime('%I:%M %p')} EST. on this {datetime.datetime.now().strftime('%A, %B %d, %Y')}. If in attendance, make yourself present by stating \"I\". Once we reach a quorum, we will proceed.\n\nRefrain from deleting or editing your messages after they've been sent as this may interfere with the record of fact.\n\n<@&581574409832366086>")
            await channel2.send(f"**A Discord City Council Session is starting.**\n\n<#854761365150629898> \n\n@here")
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
            if ctx.channel.id == 854761365150629898:
                await ctx.send("The session has been adjourned.")
                print(f"{ctx.author} has ended a Discord city council session.")
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
                await channel.send(f"{trello_link} \n\n <@&940169028683563039>")
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
    async def send(self, ctx, location: Literal["Mayor", "Docket"], trello_link):
        if location == "Mayor":
            channel = self.bot.get_channel(762320251441774632)
            if ctx.channel.name.startswith("council-session"):
                if trello_link.startswith("https://trello.com/c/"):
                    await channel.send(f"{trello_link} \n\n <@&578723625390309390>")
                    await ctx.send("The bill has been sent to the mayor for signature.")
                    print(f"{ctx.author} has sent a bill to the mayor for signature.")
                else:
                    raise commands.BadArgument("The link provided needs to be a Trello card.")
            elif ctx.channel.id == 625322290774671365:
                if ctx.interaction == None:
                    await ctx.message.delete()
                if trello_link.startswith("https://trello.com/c/"):
                    await channel.send(f"{trello_link} \n\n <@&578723625390309390>")
                    await ctx.send("Proposal sent to the mayor for signature.", ephemeral=True)
                    print(f"{ctx.author} has sent a proposal to the mayor for signature.")
                else:
                    raise commands.BadArgument("The link provided needs to be a Trello card.")
            else:
                raise commands.UserInputError("This command can only be used in <#625322290774671365> or a council session channel.")
                pass
        elif location == "Docket":
            if discord.utils.get(ctx.author.roles, id=940169028683563039):
                if ctx.channel.id == 625322290774671365:
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
                    raise commands.UserInputError("This command can only be used in <#625322290774671365>.")
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
        if ctx.channel.id == 854761365150629898:
            if ctx.interaction == None:
                await ctx.message.delete()
            await ctx.send(f"The floor is now {status.lower()} for debate. {f'<@&581574409832366086>' if status == 'Open' else ''}")
            print(f"{ctx.author} has {status.lower()}ed the floor for debate.")
        else:
            raise commands.UserInputError("This command can only be used in <#625322290774671365>.")
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

    pass

async def setup(bot):
    await bot.add_cog(CouncilCog(bot))
