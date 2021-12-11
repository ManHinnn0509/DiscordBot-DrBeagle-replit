from dateutil import tz
from datetime import datetime
from discord import Embed

from util.msg_utils import tagAuthor
from util.time_utils import getTaipeiTimeNow
from util.msg_utils import getAuthorDisplayName, getAuthorAvatarURL
from config import BOT_COLOR, BOT_NAME, BOT_ICON_URL

def createWaitEmbed(ctx=None):
    "Creates an Embed with text 'Please wait...' only"
    desc = "" if (ctx == None) else tagAuthor(ctx)

    embed = Embed(
        title = "Please wait...",
        description = desc,
        color = BOT_COLOR
    )

    setAuthorBot(embed)
    return embed

def createDefaultEmbed(ctx):
    """
        Creates an empty Embed with colo, author (bot) & request info
    """
    embed = Embed(
        color = BOT_COLOR
    )

    setAuthorBot(embed)
    setRequestFooter_ctx(ctx, embed)
    return embed

# --- Embed attributes setting etc...

def setAuthorBot(embed):
    "Sets the author of an Embed's author as the bot"
    embed.set_author(
        name = BOT_NAME,
        icon_url = BOT_ICON_URL
    )

def setRequestFooter_ctx(ctx, embed):
    "Sets the footer of an Embed with requester's info (By passing ctx in)"
    displayName = getAuthorDisplayName(ctx)
    avatarURL = getAuthorAvatarURL(ctx)
    setRequestFooter(embed, displayName, avatarURL)

def setRequestFooter(embed, displayName, avatarURL):
    "Sets the footer of an Embed with requester's info"
    
    t = getTaipeiTimeNow()
    
    embed.set_footer(
        text = f"Requested by {displayName} ({t})",
        icon_url = avatarURL
    )