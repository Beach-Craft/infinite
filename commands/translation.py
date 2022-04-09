import discord
from discord.ext import commands
from googletrans import Translator

translator = Translator()

class Translation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #  Command = Detect
    @commands.command()
    async def detect(self, ctx, text):

        detect = translator.detect(text).lang
        em = discord.Embed(
            title=f"Langauge detected!"
        )
        em.add_field(name="Your input", value=f"```{text}```", inline=False)
        em.add_field(name="Language", value=f"```{detect}```", inline=False)

        await ctx.reply(embed = em, mention_author = False)
    
    #  Command = Translate
    @commands.command(aliases=['tr'])
    async def translate(self, ctx, text_language, sec_lang, *, text):

        if text_language == None:
            await ctx.reply("Please provide text language!", mention_author = False)
        
        if sec_lang == None:
            await ctx.reply("Please provide a language to translate to!", mention_author = False)

        if sec_lang == None:
            await ctx.reply("I cant translate an empty message!", mention_author = False)

        translation = translator.translate(text, src=text_language, dest=sec_lang).text
        em = discord.Embed(
            title=f"Translated",
        )
        em.add_field(name="Text", value=f"```{text}```", inline=False)
        em.add_field(name="Text Language", value=f"```{text_language}```", inline=True)
        em.add_field(name="Translation Language", value=f"```{sec_lang}```", inline=True)
        em.add_field(name="Translation", value=f"```{translation}```", inline=False)

        await ctx.reply(embed = em, mention_author = False)

def setup(bot):
    bot.add_cog(Translation(bot))