import os
from util.json_utils import readJsonFile, updateJsonFile
from discord.ext import commands

from commands.sar import getPlayFabID, getSessionTicket, SAR_Player
from commands.steam import getSteamID

from classes import Cog_Extension
from config import PLAYFAB_AC, PLAYFAB_PW, STEAM_WEB_API_KEY
from util.msg_utils import isOwner, tagAuthor, getAuthorID

import commands.sar.ops as ops

class SuperAnimalRoyale(Cog_Extension):

    @commands.command()
    async def sar(self, ctx, option=None, url=None):
        tag = tagAuthor(ctx)

        # Search bonded account data
        if (option == None and url == None):
            await ops.search_bonded(ctx, self.bot)
        
        # Help
        elif (option == "help" or option == "-h"):
            await ctx.send(tag, embed=ops.createHelpEmbed(ctx))

        # Account bonding
        elif (option == "bond" or option == "-b"):
            await ops.bond(ctx, url)
        
        # Search player
        elif (option == "search" or option == "-s"):
            await ops.search(ctx, self.bot, url)

        # Generating a session ticket (Owner only)
        elif (option == "ticket" or option == "-t"):
            if (isOwner(ctx)):
                print(f">>> Session ticket: {getSessionTicket(PLAYFAB_AC, PLAYFAB_PW)}")
        
        else:
            await ctx.send(tag + "\n" + "Invalid input. See `help`")

# ---------- Setup

def setup(bot):
    bot.add_cog(SuperAnimalRoyale(bot))