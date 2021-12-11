import asyncio

from commands.sar import getSessionTicket, SAR_Player

from util.embed_utils import createWaitEmbed
from util.json_utils import readJsonFile
from util.msg_utils import getAuthorID, tagAuthor, getAuthor
from util.sar_utils import createSAR_Embed, hideSAR_EmbedInfo

from config import PLAYFAB_AC, PLAYFAB_PW
from commands.sar.sar_config import JSON_PATH, STEAM_ID_INDEX, PLAYFAB_ID_INDEX, TIMEOUT_SEC, DONE_EMOJI

async def search_bonded(ctx, bot):
    tag = tagAuthor(ctx)

    localRecords = readJsonFile(JSON_PATH)
    if (localRecords == None):
        await ctx.send(tag + "\n" + "Service is temporary unavailable, please try again later.")
        print('sar: Unable to load localRecords')
        print(f"Json file path: {JSON_PATH}")
        return

    authorID = str(getAuthorID(ctx))
    if (authorID not in localRecords):
        await ctx.send(tag + "\n" + "Please bond your Steam account first! (See help)")
        return
    
    embed = createWaitEmbed()
    msg = await ctx.send(tag, embed = embed)

    # Exit / Return if unable to get Session Ticket
    sessionTicket = getSessionTicket(PLAYFAB_AC, PLAYFAB_PW)
    if (sessionTicket == None):
        await ctx.send(tag + "\n" + "Service is temporary unavailable, please try again later.")
        print('sar: Unable to get session ticket')
        return
    
    # Init some variables...
    record = localRecords[authorID]
    steamID = record[STEAM_ID_INDEX]
    playFabID = record[PLAYFAB_ID_INDEX]

    # Bonded account never launched SAR
    # This if statement can be commented out since this checking is already dont when bonding the account
    if (playFabID == None):
        await ctx.send(tag + "\n" + "Bonded account does not have a Super Animal Royale profile.")
        return
    
    # Unable to get player data
    player = SAR_Player(sessionTicket, playFabID)
    if not (player.success()):
        embed.title = "Something went wrong..."
        embed.description = "Please try again later :<"
        await msg.edit(embed = embed)
        return
    
    embed = createSAR_Embed(ctx, steamID, player)
    await msg.edit(embed = embed)

    # --- Wait for reaction
    await msg.add_reaction(DONE_EMOJI)

    author = getAuthor(ctx)
    def check(reaction, user):
        return user == author and str(reaction.emoji) == DONE_EMOJI

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=TIMEOUT_SEC, check=check)
    except asyncio.TimeoutError:
        return
    # --- End of wait for reaction
    
    embed = hideSAR_EmbedInfo(embed)
    await msg.edit(embed = embed)