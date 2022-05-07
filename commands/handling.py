import discord
from discord.ext import commands

class ErrorHandling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply("You dont have the permissions to do that!", mention_author = False)
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply("Member was not found")
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.reply(f"You dont have the permissions to do that!")
        else:
            raise error
        

def setup(bot):
    bot.add_cog(ErrorHandling(bot))