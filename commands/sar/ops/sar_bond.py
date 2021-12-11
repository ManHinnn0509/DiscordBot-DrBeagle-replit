from commands.steam import getSteamID
from commands.sar import getPlayFabID, getSessionTicket

from util.msg_utils import tagAuthor, getAuthorID
from util.json_utils import updateJsonFile


from config import PLAYFAB_AC, PLAYFAB_PW, STEAM_WEB_API_KEY
from commands.sar.sar_config import JSON_PATH, SEARCH_JSON_PATH

async def bond(ctx, url):
    tag = tagAuthor(ctx)
    msg = await ctx.send(content=tag + "\n" + "Please wait...")

    if (url == None):
        await msg.edit(content=tag + "\n" + "Please provide a Steam profile URL.")
        return
    
    steamID = getSteamID(url, STEAM_WEB_API_KEY)
    if (steamID == None):
        await msg.edit(content=tag + "\n" + "Invalid Steam profile!")
        return
    
    sessionTicket = getSessionTicket(PLAYFAB_AC, PLAYFAB_PW)
    playFabID = getPlayFabID(sessionTicket, steamID)
    if (playFabID == None):
        await msg.edit(content=tag + "\n" + "This user does not have a Super Animal Royale profile.")
        return
    
    authorID = str(getAuthorID(ctx))

    # Format for saving these data into local .json file
    result = updateJsonFile(JSON_PATH, authorID, [steamID, playFabID])
    resultMsg = tag + "\n" + ("Account bonded!" if (result) else "Unable to bond account. Please try again later.")

    await msg.edit(content=resultMsg)

    # Add record to search.json
    ignored = updateJsonFile(SEARCH_JSON_PATH, steamID, playFabID)