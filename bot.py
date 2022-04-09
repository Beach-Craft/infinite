import discord, os
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)
bot.remove_command('help')


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'commands.{extension}')

    em = discord.Embed(
        description=
        f"<:check:954442477362872370>  `{extension.capitalize()}` Command Loaded Successfully!",
        colour=discord.Colour.green())

    await ctx.reply(embed=em, mention_author=False)


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'commands.{extension}')

    em = discord.Embed(
        description=
        f"<:check:954442477362872370>  `{extension.capitalize()}` Command Unloaded Successfully!",
        colour=discord.Colour.green())

    await ctx.reply(embed=em, mention_author=False)


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f'commands.{extension}')
    bot.load_extension(f'commands.{extension}')

    em = discord.Embed(
        description=
        f"<:check:954442477362872370>  `{extension.capitalize()}` Command Reloaded Successfully!",
        colour=discord.Colour.green())

    await ctx.reply(embed=em, mention_author=False)


for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')


@bot.event
async def on_ready():
    '''Bot Activity'''

    activity = discord.Game(name="spreading love", type=2)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Logged in as {bot.user} ID: {bot.user.id}")
  

bot.run("OTU5NzkyMjkwNTIyNjExNzQz.YkhCOg.BJmd7vYfyW5hj293hQr11MSdJ2c")