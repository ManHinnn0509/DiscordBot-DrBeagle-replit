from os import getcwd

# Constants
JSON_FILE_NAME = "bond.json"
# JSON_PATH = str(getcwd()) + "\\" + "json" + "\\" + "sar" + "\\" + JSON_FILE_NAME
JSON_PATH = f'./json/sar/{JSON_FILE_NAME}'

SEARCH_JSON_FILE_NAME = "search.json"
# SEARCH_JSON_PATH = str(getcwd()) + "\\" + "json" + "\\" + "sar" + "\\" + SEARCH_JSON_FILE_NAME
SEARCH_JSON_PATH = f'./json/sar/{SEARCH_JSON_FILE_NAME}'

TIMEOUT_SEC = 300.0
DONE_EMOJI = "✅"

STEAM_ID_INDEX = 0
PLAYFAB_ID_INDEX = 1

GAME_ICON_URL = "https://i.imgur.com/85CltDc.png"
MAP_URL = "https://i.imgur.com/G2GmjqB.png"

DEFAULT_FOX_COLOR = 0xde5f33