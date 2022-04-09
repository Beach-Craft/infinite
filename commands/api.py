import discord
import requests
from discord.ext import commands

class Api(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.facts_url = "https://uselessfacts.jsph.pl/random.json?language=en"
        self.advice_url = "https://api.adviceslip.com/advice"

    #  Command = Fact
    @commands.command()
    @commands.guild_only()
    async def fact(self, ctx):
        """Gets a random fact  using an api"""
        response = requests.get(self.facts_url)
        fact = response.json()['text']

        em = discord.Embed(
            description=f" {fact}"
        )

        await ctx.reply(embed = em, mention_author = False)
    
    #  Command = Advice
    @commands.command()
    @commands.guild_only()
    async def advice(self, ctx):
        """Gets a random advice using an api"""

        response = requests.get(self.advice_url)
        advice = response.json()["slip"]['advice']

        em = discord.Embed(
            description=f" {advice}"
        )

        await ctx.reply(embed = em, mention_author = False)


def setup(bot):
    bot.add_cog(Api(bot))