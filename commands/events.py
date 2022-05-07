import discord
import json
import datetime
from discord.ext import commands

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #  Event = On Member Join
    @commands.Cog.listener()
    async def on_member_join(self, member):

        guild = self.bot.get_guild(830011771880210434)
        memberList = len(guild.members)

        if member.guild.id == 830011771880210434:
            embed = discord.Embed(title="Welcome to Infinite Advertising", description="Let's get you started!\n\n<:dot:935419801193562192> <#898230437032394803>\n<:dot:935419801193562192> <#887208116767297546>\n<:dot:935419801193562192> <#944588247009464340>")
            embed.set_author(name=member.display_name, icon_url=member.avatar_url)
            embed.set_image(url="https://imgur.com/1x9l4Vm.png")
            embed.set_footer(text=f"You're our {memberList}th member \u200b")
            embed.set_thumbnail(url=member.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()

            channel = self.bot.get_channel(944976665040285777)
            await channel.send(member.mention, embed = embed)

def setup(bot):
    bot.add_cog(Events(bot))