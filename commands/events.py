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
    
    @commands.Cog.listener()
    async def on_message(self, message):

        notification_channel = self.bot.get_channel(935101741274378250)

        with open("data/channels.json", "r") as file:
            load_channels = json.load(file)

        try:
            get = load_channels[f"{message.channel.id}"]
        except:
            get = "hh"
        if get != "hh":
            note = 0
            if message.author.id == self.bot.user.id:
                note =0
            else:

                if len(message.content) <= 50:
                    await message.delete()

                    embed = discord.Embed(
                        title="Advertisement Deleted",
                        description=f"Message deleted in {message.channel.mention}"
                    )
                    embed.add_field(name="Rules", value="Make sure to read advertising rules from <#887208116767297546>")
                    embed.add_field(name="Reason", value="Your ad didn't include 5+ words in your ad describing your server")
                    embed.set_image(url="https://cdn.discordapp.com/attachments/938886261010206820/957147578040983582/infinite_ads.png")
                    await notification_channel.send(message.author.mention, embed = embed)

def setup(bot):
    bot.add_cog(Events(bot))