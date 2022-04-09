import discord
from discord.ext import commands

def make_list_embed(fields):
    embed = discord.Embed()
    for key, value in fields.items():
        embed.add_field(name=key, value=value, inline=True)
    return embed

class Information(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Command = Avatar
    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, *, user: discord.User=None):
        """Gets your avatar url or the avatar url of the specified user"""
        if user is None:
            user = ctx.author
        em = discord.Embed(title=f"{user}'s Avatar'")
        em.set_image(url=user.avatar_url)
        await ctx.send(embed = em, mention_author = False)

    # Command = Roleinfo
    @commands.command()
    @commands.guild_only()
    async def roleinfo(self, ctx, *, role: discord.Role):
        """Gets information on a role"""
        if role is None:
            await ctx.send("`{}` is not a valid role".format(role))
            return
        color = role.color
        if color == discord.Color(value=0x000000):
            color = None
        count = len([member for member in ctx.guild.members if discord.utils.get(member.roles, name=role.name)])
        fields = {
            "ID":role.id,
            "Members":count,
            "Creation Date":role.created_at,
            "Hierarchy Position":role.position,
            "Managed by Integration":role.managed,
            "Mentionable":role.mentionable,
            "Displayed Separately":role.hoist,
        }
        embed = make_list_embed(fields)
        embed.title = role.name
        await ctx.send(embed=embed)
    

    #  Command = MemberCount
    @commands.command()
    @commands.guild_only()
    async def membercount(self, ctx):

        member_count = len(ctx.guild.members) # includes bots
        true_member_count = len([m for m in ctx.guild.members if not m.bot]) # doesn't include bots
        em = discord.Embed(title=f"{ctx.guild.name}'s Members Count")
        em.add_field(name="Members:", value=f"All: `{member_count}`\nMembers: `{true_member_count}`")

        await ctx.reply(embed = em, mention_author = False)

def setup(bot):
    bot.add_cog(Information(bot))