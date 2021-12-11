import asyncio

from commands.sar import getPlayFabID, getSessionTicket, SAR_Player
from commands.steam import getSteamID

from util.msg_utils import tagAuthor, getAuthor
from util.embed_utils import createWaitEmbed
from util.sar_utils import createSAR_Embed, hideSAR_EmbedInfo
from util.json_utils import readJsonFile, updateJsonFile

from commands.sar.sar_config import SEARCH_JSON_PATH, DONE_EMOJI, TIMEOUT_SEC
from config import PLAYFAB_AC, PLAYFAB_PW, STEAM_WEB_API_KEY

async def search(ctx, bot, url):
    tag = tagAuthor(ctx)

    # Didn't provite URL
    if (url == None):
        await ctx.send(tag + "\n" + "Please provide a Steam profile URL!")
        return
    
    # Invalid profile URL
    steamID = getSteamID(url, STEAM_WEB_API_KEY)
    if (steamID == None):
        await ctx.send(tag + "\n" + "Invalid profile URL!")
        return
    
    # Creates an Embed
    embed = createWaitEmbed()
    embed.description = 'You can use "$sar bond" to bond this account. See "$sar help"'
    embed.description += "\n"
    embed.description += '你可以用 "$sar bond" 去綁定這個帳號，詳情請看 "$sar help"'

    # Send the msg with tag & embed
    msg = await ctx.send(tag, embed = embed)

    # Unable to get session ticket / local json records, then edit the embed and return
    sessionTicket = getSessionTicket(PLAYFAB_AC, PLAYFAB_PW)
    localRecords = readJsonFile(SEARCH_JSON_PATH)
    if ((sessionTicket == None) or (localRecords == None)):
        embed.title = "Something went wrong..."
        embed.description = "Please try again later :<"
        await msg.edit(embed = embed)
        return
    
    playFabID = localRecords.get(steamID, None)
    hasLocalRecord = True
    if (playFabID == None):
        # This record not found in local json file.
        hasLocalRecord = False
        
        # Get the PlayFabID via function / API call
        playFabID = getPlayFabID(sessionTicket, steamID)
        
        # If the function / API call above has failed...
        if (playFabID == None):
            embed.title = ""
            embed.description = "This user does not have a Super Animal Royale profile."
            await msg.edit(embed = embed)
            return
    
    player = SAR_Player(sessionTicket, playFabID)
    if not (player.success()):
        embed.title = "Something went wrong..."
        embed.description = "Please try again later :<"
        await msg.edit(embed = embed)
        return
    
    embed = createSAR_Embed(ctx, steamID, player)
    await msg.edit(embed=embed)

    if not (hasLocalRecord):
        result = updateJsonFile(SEARCH_JSON_PATH, steamID, playFabID)

    # --- Wait for reaction
    await msg.add_reaction(DONE_EMOJI)

    author = getAuthor(ctx)
    def check(reaction, user):
        return (user == author) and str(reaction.emoji) == DONE_EMOJI and (reaction.message.id == msg.id)

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=TIMEOUT_SEC, check=check)
    except asyncio.TimeoutError:
        return
    # --- End of wait for reaction

    embed = hideSAR_EmbedInfo(embed)
    await msg.edit(embed = embed)