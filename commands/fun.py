import discord
import re
import random
from discord.ext import commands

def strip_global_mentions(message, ctx=None):
    if ctx:
        perms = ctx.message.channel.permissions_for(ctx.message.author)
        if perms.mention_everyone:
            return message
    remove_everyone = re.compile(re.escape("@everyone"), re.IGNORECASE)
    remove_here = re.compile(re.escape("@here"), re.IGNORECASE)
    message = remove_everyone.sub("everyone", message)
    message = remove_here.sub("here", message)
    return message

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Help is ready!')

    #  Command = 8ball
    @commands.command(aliases=['8ball'])
    @commands.guild_only()
    async def _8ball(self, ctx, question):

        responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
             "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
             "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
             "Yes.", "Yes – definitely.", "You may rely on it."]
                
        response = random.choice(responses)
        embed=discord.Embed(title="The Magic 8 Ball has Spoken!")
        embed.add_field(name='Question: ', value=f'{question}', inline=True)
        embed.add_field(name='Answer: ', value=f'{response}', inline=False)

        await ctx.reply(embed=embed, mention_author = False)

    #  Command = Say
    @commands.command()
    @commands.guild_only()
    async def say(self, ctx, *, message:str):
        """Make the bot say whatever you want it to say"""
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(strip_global_mentions(message, ctx))

    #  Command = Spellout
    @commands.command()
    @commands.guild_only()
    async def spellout(self, ctx, *, msg:str):
        """S P E L L O U T"""
        await ctx.reply(" ".join(list(msg.upper())), mention_author = False)

    #  Command = Roll
    @commands.command()
    @commands.guild_only()
    async def roll(self, ctx):
        """Roll some die"""
        await ctx.reply("You rolled a {}!".format(random.randint(1, 6)), mention_author = False)
      
def setup(bot):
    bot.add_cog(Fun(bot))