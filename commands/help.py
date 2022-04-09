import discord
import datetime
from discord.ext import commands

PREFIX = "$"

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #  Command = Help
    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def help(self, ctx):
        em = discord.Embed(
            title="Help menu",
            description=f"Hi there! my prefix is `{PREFIX}`.",
            color=0x11998e
            )

        em.add_field(name="Useful help commands", value=f"`{PREFIX}help <command>` Shows some help about a specific command.")
        em.add_field(name="📝 General [2]:", value="> `help`, `ping`", inline=False)
        em.add_field(name="🗂 Api [2]:", value="> `advice`, `fact`", inline=False)
        em.add_field(name="🎈 Fun [4]:", value="> `8ball`, `say`, `spellout`, `rolldice`", inline=False)
        em.add_field(name="🔧 Moderation [7]:", value="> `clear`, `mute`, `warn`, `warnings`,`clearwarns`, `points`, `leaderboard`", inline=False)
        em.add_field(name="🔩 Information [5]:", value="> `id`, `roleid`, `avatar`,`roleinfo`, `membercount`", inline=False)
        em.add_field(name="🛠 Owners [3]:", value="> `load`, `unload`, `reload`", inline=False)
        em.timestamp = datetime.datetime.utcnow()
        em.set_image(url="https://cdn.discordapp.com/attachments/938886261010206820/957147578040983582/infinite_ads.png")
        em.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed = em, mention_author = False)
    
    @help.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.is_owner()
    async def owner(self, ctx):
        em = discord.Embed(
            title="Help owner menu",
            color=0x11998e
            )
        em.add_field(name="Load", value="<:list_3:956607358912585789> Loads a command", inline=False)
        em.add_field(name="Unoad", value="<:list_3:956607358912585789> Unloads a command", inline=False)
        em.add_field(name="Reload", value="<:list_3:956607358912585789> reloads a command", inline=False)
        em.set_image(url="https://cdn.discordapp.com/attachments/938886261010206820/957147578040983582/infinite_ads.png")
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed = em, mention_author = False)

    @help.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.is_owner()
    async def moderation(self, ctx):
        em = discord.Embed(
            title="Moderation team help menu",
            color=0x11998e
            )
        em.add_field(name="Warn", value="<:list_3:956607358912585789> Warns a member",inline=False)
        em.add_field(name="Warnings", value="<:list_3:956607358912585789> Shows member warnings", inline=False)
        em.add_field(name="clearnwarns", value="<:list_3:956607358912585789> Removes all member warns", inline=False)
        em.set_image(url="https://cdn.discordapp.com/attachments/938886261010206820/957147578040983582/infinite_ads.png")
        em.add_field(name="mute", value="<:list_3:956607358912585789> Mutes a member", inline=False)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed = em, mention_author = False)

def setup(bot):
    bot.add_cog(Help(bot))