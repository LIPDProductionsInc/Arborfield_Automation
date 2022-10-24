import discord
import random

from discord.ext import commands

class RedwoodAutomationFun(commands.Cog, name="Fun Commands"):
    def __init__(self, bot) -> None:
       self.bot = bot
    
    @commands.hybrid_command(name="flip", description="Flips a coin.")
    @commands.guild_only()
    async def flip(self, ctx):
        if ctx.channel.category_id == 578722368625836043:
            if random.randint(0, 1) == 0:
                await ctx.send("Heads")
            else:
                await ctx.send("Tails")
        else:
            raise commands.UserInputError("This command cannot be used in this channel.")
        pass

    @commands.hybrid_command(name="roll", description="Rolls a die.")
    @commands.guild_only()
    async def roll(self, ctx, sides:int=6):
        if ctx.channel.category_id == 578722368625836043:
            await ctx.send(f"You rolled a {random.randint(1, sides)}")
        else:
            raise commands.UserInputError("This command cannot be used in this channel.")
        pass

    @commands.hybrid_command(name="choose", description="Chooses between multiple options.")
    @commands.guild_only()
    async def choose(self, ctx, *, choices):
        if ctx.channel.category_id == 578722368625836043:
            await ctx.send(f' Chose {random.choice(choices)}')
        else:
            raise commands.UserInputError("This command cannot be used in this channel.")
        pass

    @commands.hybrid_command(name="8ball", description="Answers a yes/no question.")
    @commands.guild_only()
    async def eightball(self, ctx, *, question):
        if ctx.channel.category_id == 578722368625836043:
            responses = ["It is certain.",
                         "It is decidedly so.",
                         "Without a doubt.",
                         "Yes - definitely.",
                         "You may rely on it.",
                         "As I see it, yes.",
                         "Most likely.",
                         "Outlook good.",
                         "Yes.",
                         "Signs point to yes.",
                         "Reply hazy, try again.",
                         "Ask again later.",
                         "Better not tell you now.",
                         "Cannot predict now.",
                         "Concentrate and ask again.",
                         "Don't count on it.",
                         "My reply is no.",
                         "My sources say no.",
                         "Outlook not so good.",
                         "Very doubtful."]
            await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
        else:
            raise commands.UserInputError("This command cannot be used in this channel.")
        pass

    @commands.hybrid_command(name="rps", description="Play rock, paper, scissors.")
    @commands.guild_only()
    async def rps(self, ctx, choice):
        if ctx.channel.category_id == 578722368625836043:
            choices = ["rock", "paper", "scissors"]
            if choice.lower() not in choices:
                raise commands.UserInputError("Invalid choice.")
            else:
                await ctx.send(f"You chose {choice.lower()}")
                await ctx.send(f"I chose {random.choice(choices)}")
        else:
            raise commands.UserInputError("This command cannot be used in this channel.")
        pass

    @commands.hybrid_command(name="rpsls", description="Play rock, paper, scissors, lizard, spock.")
    @commands.guild_only()
    async def rpsls(self, ctx, choice):
        if ctx.channel.category_id == 578722368625836043:
            choices = ["rock", "paper", "scissors", "lizard", "spock"]
            if choice.lower() not in choices:
                raise commands.UserInputError("Invalid choice.")
            else:
                await ctx.send(f"You chose {choice.lower()}")
                await ctx.send(f"I chose {random.choice(choices)}")
        else:
            raise commands.UserInputError("This command cannot be used in this channel.")
        pass

    pass

async def setup(bot):
    await bot.add_cog(RedwoodAutomationFun(bot))