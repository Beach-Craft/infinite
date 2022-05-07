import discord
import datetime
import asyncio
import json
from time import time
from discord.ext import commands

from utils import moderation

class Mute(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #  Command = AddChannel
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def addchannel(self, ctx, channel : discord.TextChannel = None):

        embed = discord.Embed(
            description="Specify a channel!",
            color=discord.Color.red()
            )

        if channel == None:
            await ctx.reply(embed = embed, mention_author = False)
        else:

            embed = discord.Embed(
            description=f"{channel.mention} has been added!",
            color=discord.Color.green()
            )
            await moderation.add_channel_data(channel)
            await ctx.reply(embed = embed, mention_author = False)

    #  Command = RemoveChannel
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def removechannel(self, ctx, channel : discord.TextChannel = None):

        embed = discord.Embed(
            description="Specify a channel!",
            color=discord.Color.red()
            )

        if channel == None:
            await ctx.reply(embed = embed, mention_author = False)

        with open("data/channels.json","r") as file:
            load = json.load(file)
        try:
            del load[f"{channel.id}"]
        except:
            return await ctx.reply("Couldn't find the channel!", mention_author = False)

        with open("data/channels.json","w") as file:
            json.dump(load, file)
        await ctx.reply(f"Channel removed {channel.mention}!", mention_author = False)

    #  Command = Clear
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role("Founder", "Admins", "Moderation Team")
    async def clear(self, ctx, amount:int):
        """Prunes the specified amount of messages"""
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            await ctx.reply("I do not have the `Manage Messages` permission.", mention_author= False)
            return
        deleted = await ctx.channel.purge(limit=amount)
        deleted_message = await ctx.reply(f"`{len(deleted)}` messages have been deleted.", mention_author = False)
        await asyncio.sleep(5)
        # The try and except pass is so in the event a user prunes again or deletes the prune notification before the bot automatically does it, it will not raise an error
        try:
            await deleted_message.delete()
        except:
            pass
    
    #  Commands = Points
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role("Founder", "Admins", "Moderation Team")
    async def points(self, ctx, staff : discord.Member = None):
        if staff == None:
            staff = ctx.author

        staffs = await moderation.staff_data(staff)
        staffs = await moderation.get_staff_data()

        points = staffs[str(staff.id)]["points"]
        em = discord.Embed(title=f"{staff.name}'s Moderation Points", description=f"**Points:** `{points}`")
        await ctx.reply(embed = em, mention_author = False)

    #  Commands = Manage Points
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role("Founder", "Admins", "Moderation Team")
    async def manage_points(self, ctx, staff : discord.Member, stats, amount):

        staffs = await moderation.get_staff_data()

        if stats == "add":
            points = staffs[str(staff.id)]["points"] =+ amount
            em = discord.Embed(title=f"{staff.name}'s Moderation Points", description=f"**Points:** `{points}`")
            await ctx.reply(embed = em, mention_author = False)
        elif stats == "remove":
            points = staffs[str(staff.id)]["points"] =- amount
            em = discord.Embed(title=f"{staff.name}'s Moderation Points", description=f"**Points:** `{points}`")
            await ctx.reply(embed = em, mention_author = False)
    
    #  Commands = Leaderboard
    @commands.command()
    @commands.guild_only()
    async def leaderboard(self, ctx, x = 5):

        staffs = await moderation.get_staff_data()
        leader_board = {}
        total = []

        for staff in staffs:
            name = int(staff)
            total_amount = staffs[staff]["points"]
            leader_board[total_amount] = name 
            total.append(total_amount)
    

        total = sorted(total, reverse =True)

        em = discord.Embed(title = f"Top {x} Moderators Have Warning Points")
        em.set_footer(text="$points to get your points")
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = self.bot.get_user(id_)
            name = member.name 
            em.add_field(name=f"`{index}.` {name}", value = f"<:list_3:956607358912585789> {amt}", inline = False)
            if index == x:
                break
            else:
                index +=1

        await ctx.reply(embed = em, mention_author = False)

    #  Commands = Warn
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role("Founder", "Admins", "Moderation Team")
    async def warn(self, ctx, member : discord.Member = None):

        if member == None:
            em = discord.Embed(
                title="Warn Command",
                descrition="Warns a member"
            )
            em.add_field(name="Usage:", value="-warn [Member ID/Mention]")
            em.add_field(name="Example:", value=f"-warn {ctx.author.mention}", inline=False)

            await ctx.reply(embed = em, mention_author = False)

        else:

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            main_embed = discord.Embed(title="Warn Command")
            main_embed.add_field(name="<:red:956607358669291562> Reason(s)", value="<:list_3:956607358912585789> No Reason Provided", inline=False)
            main_embed.add_field(name="<:red:956607358669291562> Channel(s)", value="<:list_3:956607358912585789> Not Set", inline=False)
            main_embed.add_field(name="<:red:956607358669291562> Notification", value="<:list_3:956607358912585789> Not Sent", inline=False)
            main_embed.timestamp = datetime.datetime.utcnow()
            main_embed.set_footer(text=f"{member.display_name} \u200b", icon_url=member.avatar_url)

            set_reason_embed = discord.Embed(description="**Enter Warn Reason(s)**")
            set_channel_embed = discord.Embed(description="**Enter Channel(s)**")

            try:
                msg = await ctx.reply(embed = main_embed, mention_author = False)
                set_reason_msg = await ctx.send(embed = set_reason_embed)
                reason_reply = await self.bot.wait_for('message', timeout=60.0, check=check)
                await reason_reply.add_reaction("<:check:954442477362872370>")
                main_embed2 = discord.Embed(title="Warn Command")
                main_embed2.add_field(name="<:green:956607358895783996> Reason(s)", value=f"<:list_3:956607358912585789> {reason_reply.content}", inline=False)
                main_embed2.add_field(name="<:red:956607358669291562> Channel(s)", value="<:list_3:956607358912585789> Not Set", inline=False)
                main_embed2.add_field(name="<:red:956607358669291562> Notification", value="<:list_3:956607358912585789> Not Sent", inline=False)
                main_embed2.timestamp = datetime.datetime.utcnow()
                main_embed2.set_footer(text=f"{member.display_name} \u200b", icon_url=member.avatar_url)
                await msg.edit(embed = main_embed2)
                await set_reason_msg.delete()
                await reason_reply.delete()

            except asyncio.TimeoutError:
                await ctx.reply("Timeout!", mention_author = False)

            try:
                set_channel_msg = await ctx.send(embed = set_channel_embed)
                channel_reply = await self.bot.wait_for('message', timeout=60.0, check=check)
                channel = channel_reply.content
                if channel.startswith("<#") and channel.endswith(">"):

                    # Creats database if member dosn't have one
                    await moderation.create_data(member)
                    staff = ctx.author
                    user = member
                    staff1 = staff
                    await moderation.staff_data(staff)
                  
                    # Updates member data
                    await moderation.update_data(member, reason_reply.content, ctx.author)
                    await moderation.update_staff(staff)

                    users = await moderation.get_data()
                    staffs = await moderation.get_staff_data()

                    warncount = users[str(user.id)]["count"]
                    staff_points = staffs[str(staff1.id)]["points"]

                    await channel_reply.add_reaction("<:check:954442477362872370>")
                    main_embed3 = discord.Embed(title="Warn Command")
                    main_embed3.add_field(name="<:green:956607358895783996> Reason(s)", value=f"<:list_3:956607358912585789> {reason_reply.content}", inline=False)
                    main_embed3.add_field(name="<:green:956607358895783996> Channel(s)", value=f"<:list_3:956607358912585789> {channel_reply.content}", inline=False)
                    main_embed3.add_field(name="<:red:956607358669291562> Notification", value="<:list_3:956607358912585789> Not Sent", inline=False)
                    main_embed3.timestamp = datetime.datetime.utcnow()
                    main_embed3.set_footer(text=f"{member.display_name} \u200b", icon_url=member.avatar_url)
                    await msg.edit(embed = main_embed3)
                    await set_channel_msg.delete()
                    await channel_reply.delete()

                    # Warning channel
                    notification_channel = self.bot.get_channel(935101741274378250)
                    # Warning log channel
                    warning_channel = self.bot.get_channel(942113618563051560)

                    # Notification embed
                    embed=discord.Embed(title="Advertisement Deleted", description=f"**Moderated By:** {ctx.author.mention}\n**Case:** ({warncount})\n**Channel:** {channel_reply.content}\n**Reason:**\n{reason_reply.content}")
                    embed.set_image(url="https://cdn.discordapp.com/attachments/938886261010206820/957147578040983582/infinite_ads.png")
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(text=f"Infinite Moderation Team", icon_url=ctx.guild.icon_url)
                    embed.set_author(name=member.display_name, icon_url=member.avatar_url)
                    await notification_channel.send(f"{member.mention} you have been warned!", embed=embed)
                    main_embed3 = discord.Embed(title=f"{member.display_name}'s has been warned!")
                    main_embed3.add_field(name="<:green:956607358895783996> Reason(s)", value=f"<:list_3:956607358912585789> {reason_reply.content}", inline=False)
                    main_embed3.add_field(name="<:green:956607358895783996> Channel(s)", value=f"<:list_3:956607358912585789> {channel_reply.content}", inline=False)
                    main_embed3.add_field(name="<:green:956607358895783996> Notification", value="<:list_3:956607358912585789> Sent to <#935101741274378250>", inline=False)
                    main_embed3.timestamp = datetime.datetime.utcnow()
                    main_embed3.set_footer(text=f"{staff.display_name} has been given 1 point, you have {staff_points} points! \u200b", icon_url=member.avatar_url)
                    await msg.edit(embed = main_embed3)
                    # Warning logs embed
                    embed=discord.Embed()
                    embed.add_field(name="User:", value=f"{member.mention}", inline=False)
                    embed.add_field(name="<:id_:954442477316767794> UserID:", value=f"{member.id}", inline=False)
                    embed.add_field(name="<:channel:954442477325140028> Channel:", value=f"{channel_reply.content}", inline=False)
                    embed.add_field(name="<:play:954442477383864320> Case:", value=f"```fix\n {warncount}\n```", inline=False)
                    embed.add_field(name="<:info:954442477434187876> Reason:", value=f"```{reason_reply.content}```", inline=False)
                    embed.add_field(name="Moderator: ", value=f"{ctx.author.mention}", inline=False)
                    embed.add_field(name="Time:", value=f"<t:{int(time())}:D>", inline=False)
                    await warning_channel.send(embed=embed)
                    
                    hours = 3600

                    if warncount == 3:
                        mute = 3 * hours
                        roleobject = discord.utils.get(ctx.message.guild.roles, id=891991637184630794)

                        main_embed4 = discord.Embed(title=f"{member.display_name}'s has been warned!")
                        main_embed4.add_field(name="<:green:956607358895783996> Reason(s)", value=f"<:list_3:956607358912585789> {reason_reply.content}", inline=False)
                        main_embed4.add_field(name="<:green:956607358895783996> Channel(s)", value=f"<:list_3:956607358912585789> {channel_reply.content}", inline=False)
                        main_embed4.add_field(name="<:green:956607358895783996> Notification", value="<:list_3:956607358912585789> Sent to <#935101741274378250>", inline=False)
                        main_embed4.add_field(name="<:green:956607358895783996> Actions", value="<:list_3:956607358912585789> The member has been muted!", inline=False)
                        main_embed4.timestamp = datetime.datetime.utcnow()
                        main_embed4.set_footer(text=f"{staff.display_name} has been given 1 point, you have {staff_points} points! \u200b", icon_url=member.avatar_url)
                        await msg.edit(embed = main_embed4)

                        await user.add_roles(roleobject)
                        await asyncio.sleep(mute)
                        await user.remove_roles(roleobject)
                    if warncount == 5:
                        mute = 10 * hours
                        roleobject = discord.utils.get(ctx.message.guild.roles, id=891991637184630794)

                        main_embed5 = discord.Embed(title=f"{member.display_name}'s has been warned!")
                        main_embed5.add_field(name="<:green:956607358895783996> Reason(s)", value=f"<:list_3:956607358912585789> {reason_reply.content}", inline=False)
                        main_embed5.add_field(name="<:green:956607358895783996> Channel(s)", value=f"<:list_3:956607358912585789> {channel_reply.content}", inline=False)
                        main_embed5.add_field(name="<:green:956607358895783996> Notification", value="<:list_3:956607358912585789> Sent to <#935101741274378250>", inline=False)
                        main_embed5.add_field(name="<:green:956607358895783996> Actions", value="<:list_3:956607358912585789> The member has been muted!", inline=False)
                        main_embed5.timestamp = datetime.datetime.utcnow()
                        main_embed5.set_footer(text=f"{staff.display_name} has been given 1 point, you have {staff_points} points! \u200b", icon_url=member.avatar_url)
                        await msg.edit(embed = main_embed5)

                        await user.add_roles(roleobject)
                        await asyncio.sleep(mute)
                        await user.remove_roles(roleobject)


                else:
                    await ctx.reply("Thats not a channel!", mention_author = False)
                    await channel_reply.add_reaction("<:wrong:954604048458350592>")
            except asyncio.TimeoutError:
                await ctx.reply("Timeout!", mention_author = False)
    
    #  Commands = Warnings
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role("Founder", "Admins", "Moderation Team")
    async def warnings(self, ctx, member : discord.Member):
        users = await moderation.get_data()
        index = 1
        embed = discord.Embed(title=f"{member.name}'s Warnings")
        embed.set_author(name=member.name, icon_url=member.avatar_url)

        id = users[str(member.id)]["warnings"][str(index)]["id"]
        count = users[str(member.id)]["count"]
        reason = users[str(member.id)]["warnings"][str(index)]["reason"]
        time = users[str(member.id)]["warnings"][str(index)]["time"]
        moderator = users[str(member.id)]["warnings"][str(index)]["moderator"]
      
        for user in users:
            if str(member.id) == user:
                if count > 1 or count == 1:
                    
                    embed.add_field(name=f"<:clock_:956599472501182535> <t:{time}:f>",value=f"<:id_:954442477316767794> **Warn ID:** `{id}`\n<:discord_mod:956600652082073731> **Moderated By:** <@{moderator}>\n```diff\n- {reason}\n```")
                    
                    index +=1
                if count > 2 or count == 2:

                    id = users[str(member.id)]["warnings"][str(index)]["id"]
                    count = users[str(member.id)]["count"]
                    reason = users[str(member.id)]["warnings"][str(index)]["reason"]
                    time = users[str(member.id)]["warnings"][str(index)]["time"]
                    moderator = users[str(member.id)]["warnings"][str(index)]["moderator"]
                    
                    embed.add_field(name=f"<:clock_:956599472501182535> <t:{time}:f>",value=f"<:id_:954442477316767794> **Warn ID:** `{id}`\n<:discord_mod:956600652082073731> **Moderated By:** <@{moderator}>\n```diff\n- {reason}\n```", inline = False)

                    index +=1
                if count > 3 or count == 3:
                    
                    id = users[str(member.id)]["warnings"][str(index)]["id"]
                    count = users[str(member.id)]["count"]
                    reason = users[str(member.id)]["warnings"][str(index)]["reason"]
                    time = users[str(member.id)]["warnings"][str(index)]["time"]
                    moderator = users[str(member.id)]["warnings"][str(index)]["moderator"]

                    embed.add_field(name=f"<:clock_:956599472501182535> <t:{time}:f>",value=f"<:id_:954442477316767794> **Warn ID:** `{id}`\n<:discord_mod:956600652082073731> **Moderated By:** <@{moderator}>\n```diff\n- {reason}\n```", inline = False)

                    index +=1
                if count > 4 or count == 4:
                    
                    id = users[str(member.id)]["warnings"][str(index)]["id"]
                    count = users[str(member.id)]["count"]
                    reason = users[str(member.id)]["warnings"][str(index)]["reason"]
                    time = users[str(member.id)]["warnings"][str(index)]["time"]
                    moderator = users[str(member.id)]["warnings"][str(index)]["moderator"]

                    embed.add_field(name=f"<:clock_:956599472501182535> <t:{time}:f>",value=f"<:id_:954442477316767794> **Warn ID:** `{id}`\n<:discord_mod:956600652082073731> **Moderated By:** <@{moderator}>\n```diff\n- {reason}\n```", inline = False)

                    index +=1
                    
                if count > 5 or count == 5:
                    
                    id = users[str(member.id)]["warnings"][str(index)]["id"]
                    count = users[str(member.id)]["count"]
                    reason = users[str(member.id)]["warnings"][str(index)]["reason"]
                    time = users[str(member.id)]["warnings"][str(index)]["time"]
                    moderator = users[str(member.id)]["warnings"][str(index)]["moderator"]
                    
                    embed.add_field(name=f"<:clock_:956599472501182535> <t:{time}:f>",value=f"<:id_:954442477316767794> **Warn ID:** `{id}`\n<:discord_mod:956600652082073731> **Moderated By:** <@{moderator}>\n```diff\n- {reason}\n```", inline = False)

                    index +=1
                
                if index == 6:
                    break
                else:
                    index += 1
            
        await ctx.send(embed = embed)
        
    @commands.command()
    @commands.guild_only()
    @commands.has_any_role("Founder", "Admins", "Moderators")
    async def clearwarns(self, ctx, member: discord.Member = None):

        

        if member == None:
            em = discord.Embed(
                title="Clearnwarns Command",
                descrition="Clearnwarns member warn"
            )
            em.add_field(name="Usage:", value="-clearnwarns [Member ID/Mention]")
            em.add_field(name="Example:", value=f"-clearnwarns {ctx.author.mention}", inline=False)
        else:
            with open("data/warns.json","r") as file:
                load_warns = json.load(file)
    
        del load_warns[str(member.id)]
  
        with open("data/warns.json","w") as file:
            json.dump(load_warns,file)
  
        await ctx.reply(f"{member.display_name} warns removed!", mention_author = False)

def setup(bot):
    bot.add_cog(Mute(bot))