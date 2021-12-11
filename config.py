from os import getenv

from discord import Activity, ActivityType

from dotenv import load_dotenv
load_dotenv()

BOT_PREFIX = "$"
BOT_NAME = "Dr. Beagle 🎓"
BOT_COLOR = 0xBD743F

BOT_ACTIVITY = Activity(
    type = ActivityType.streaming,
    name = "Super Animal Royale",
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"     # Rick roll
)

BOT_ICON_URL = "https://i.imgur.com/uhVEecY.png"
BOT_FULL_URL = "https://i.imgur.com/ySbmenX.png"
BOT_INVITE_URL = "https://discord.com/api/oauth2/authorize?client_id=888383011400339496&permissions=8&scope=bot"

# From .env
OWNER_ID = getenv("OWNER_ID")
OWNER_STEAM_ID = getenv("OWNER_STEAM_ID")
OWNER_PLAYFAB_ID = getenv("OWNER_PLAYFAB_ID")

BOT_TOKEN = getenv('BOT_TOKEN')
STEAM_WEB_API_KEY = getenv("STEAM_API_KEY")

PLAYFAB_EMAIL = getenv("PLAYFAB_EMAIL")
PLAYFAB_AC = getenv("PLAYFAB_AC")
PLAYFAB_PW = getenv("PLAYFAB_PW")

BDOM_COOKIE_KEY = getenv("COOKIE_KEY")
BDOM_FORM_DATA_KEY = getenv("FORM_DATA_KEY")
BDOM_USER_AGENT = getenv("BDOM_USER_AGENT")

"""
# Settings from Mongy.py
MONGY_COLOR = 0xE800FF

MONGY_ICON_URL = "https://i.imgur.com/fShZYcc.jpg"
MONGY_JPG = "https://i.imgur.com/zgnWdG2.jpg"
BOT_INVITE_URL = "https://discord.com/api/oauth2/authorize?client_id=836216444051914774&permissions=8&scope=bot"
"""