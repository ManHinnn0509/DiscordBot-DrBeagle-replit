import discord

from os import getcwd
from discord.ext import commands

from classes import Cog_Extension
from util.json_utils import readJsonFile
from util.time_utils import getDateTimeNow
from util.embed_utils import setRequestFooter
from util.math_utils import randDouble, randInt
from util.msg_utils import tagAuthor, isOwner, getAuthorDisplayName, getAuthorAvatarURL

from config import BOT_COLOR, BOT_NAME, BOT_ICON_URL

# Constants
pokedex = None
# POKEDEX_JSON_PATH = str(getcwd()) + "\\" + "json" + "\\" + "pokedex.json"
POKEDEX_JSON_PATH = f"./json/pokedex.json"

SHINY_RATE = 1 / 8192
SHINY_RATE_STR = "1 / 8192"

class Pokemon(Cog_Extension):

    @commands.command(
        aliases = ["pkm", "寶可夢"],
        brief = "Get a random Pokemon... Just for fun"
    )
    async def pokemon(self, ctx, argIndex = None, argShiny = None):
        global pokedex
        await randomPokemon(ctx, pokedex, SHINY_RATE, SHINY_RATE_STR, argIndex, argShiny)

# ---------- Functions

async def randomPokemon(ctx, pokedex, shinyRate, rateStr, argIndex=None, argShiny=None):
    tag = tagAuthor(ctx)

    pokedexMin = 1
    pokedexMax = len(pokedex)

    index = randInt(pokedexMin, pokedexMax)
    shiny = (randDouble() <= shinyRate)

    # For owner only, command options
    if (isOwner(ctx)):
        if (argIndex != None):
            try:
                index = int(argIndex)
                if ((index > pokedexMax) or (index < pokedexMin)):
                    return
            except:
                pass
        if (argShiny == "shiny"):
            shiny = True
    
    pokemonData = pokedex[str(index)]
    embed = __buildPokemonEmbed(ctx, pokemonData, shiny, rateStr)
    await ctx.send(tag, embed = embed)

def __buildPokemonEmbed(ctx, pokemonData, shiny, rateStr):
    pkm = PokedexPokemon(pokemonData)

    index = pkm.getPokedexID()
    translatedName = pkm.getTranslatedName()
    
    dir = "xyani-shiny" if (shiny) else "xyani"

    # Use animated Pokemon images
    # artworkURL = pkm.getOfficialArtworkURL()
    gifName = pkm.getName().replace("-", "")
    artworkURL = "https://play.pokemonshowdown.com/sprites/{}/{}.gif".format(dir, gifName)

    # Build description
    desc = "圖鑑編號: {}".format(index)
    if (pkm.isLegendary()):
        desc += "\n\n" + "是**神獸**欸"
    elif (pkm.isMythical()):
        desc += "\n\n" + "是**幻之寶可夢**欸?"
    
    if (shiny):
        desc += "\n\n" + f"是**色違**的! ({rateStr} 的機率!)"

    # Build the Embed...
    embed = discord.Embed(
        title = "野生的 " + str(translatedName) + " 出現了！",
        description = desc,
        color = BOT_COLOR
    )

    embed.set_image(url = artworkURL)

    embed.set_author(
        name = BOT_NAME,
        icon_url = BOT_ICON_URL
    )

    # Sets the footer with function in utils.
    setRequestFooter(embed, getAuthorDisplayName(ctx), getAuthorAvatarURL(ctx))

    return embed

# ---------- Pokemon Class object from the Json data

class PokedexPokemon:
    def __init__(self, pokemonDataList):
        self.data = pokemonDataList
    
    def getPokedexID(self):
        return self.data[0]
    
    def getName(self):
        return self.data[1]
    
    def getTranslatedName(self):
        return self.data[2]
    
    def getOfficialArtworkURL(self):
        return self.data[3]
    
    def isLegendary(self):
        return self.data[4]
    
    def isMythical(self):
        # https://wiki.52poke.com/zh-hant/%E5%B9%BB%E4%B9%8B%E5%AE%9D%E5%8F%AF%E6%A2%A6
        return self.data[5]

# ---------- Setup

def setup(bot):
    bot.add_cog(Pokemon(bot))
    
    # Init the pokedex when this extension or "command" is being loaded
    global pokedex
    pokedex = readJsonFile(POKEDEX_JSON_PATH)