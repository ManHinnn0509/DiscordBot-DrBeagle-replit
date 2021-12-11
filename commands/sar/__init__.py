import json
import requests as req

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from commands.sar.sar_player import SAR_Player
from commands.sar.player_leaderboard import PlayerLeaderboard

def getSessionTicket(playFab_AC: str, playFab_PW: str):
    """
        Gets session ticket for SAR via LoginWithPlayFab() \n
        See https://docs.microsoft.com/en-us/rest/api/playfab/client/authentication/login-with-playfab?view=playfab-rest

        None will be returned if any Exception is raised or the player has no PlayFab ID
    """

    TITLE_ID = "D36D"
    apiURL = "https://d36d.playfabapi.com/Client/LoginWithPlayFab"

    body = {
        "Username": playFab_AC,
        "Password": playFab_PW,
        "TitleId": TITLE_ID
    }

    r = req.post(url=apiURL, verify=False, json=body)
    try:
        rJSON = r.json()
        return rJSON["data"]["SessionTicket"]
    except:
        return None

def getPlayFabID(sessionTicket, steamID):
    """
        Gets a player's PlayFab ID using his/her Steam ID \n
        See https://docs.microsoft.com/en-us/rest/api/playfab/server/account-management/get-playfab-ids-from-steam-ids?view=playfab-rest
    """

    url = "https://titleId.playfabapi.com/Client/GetPlayFabIDsFromSteamIDs"

    headers = {
        "Host": "d36d.playfabapi.com",
        "User-Agent": "UnityPlayer/2018.4.27f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)",
        "X-PlayFabSDK": "UnitySDK-2.84.200402",
        "X-Authorization": sessionTicket,
        "Content-Type": "application/json",
    }

    steamID = int(steamID)
    bodyDict = {
        "SteamStringIDs": [
            steamID
        ]
    }

    # Make it into String
    body = json.dumps(bodyDict)
    
    r = req.post(url=url, headers=headers, data=body, verify=False)
    try:
        data = r.json()
        return data["data"]["Data"][0]["PlayFabId"]
    except:
        return None