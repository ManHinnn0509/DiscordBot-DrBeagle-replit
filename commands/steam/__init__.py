import json
import requests as req

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SteamUser:
    def __init__(self, apiKey, steamID, index=0):
        url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}".format(apiKey, steamID)
        r = req.get(url, verify=False)

        reqData = r.json()["response"]["players"][int(index)]

        self.data = reqData
        self.steamID = reqData["steamid"]
        self.personaName = reqData["personaname"]
        self.profileURL = reqData["profileurl"]
        self.avatarFullURL = reqData["avatarfull"]
        self.realName = reqData.get("realname", "N/A")
        self.countryCode = reqData.get("loccountrycode", "N/A")
        self.timeCreated_Timestamp = reqData.get("timecreated", "UNKNOWN")
        self.lastLogOff_Timestamp = reqData.get("lastlogoff", "UNKNOWN")

def getSteamID(profileURL, apiKey):
    """
        Returns a Steam64ID from of account of profileURL \n
        None will be returned if the URL is invalid
    """
    reqURL = __genSteamReqURL(profileURL, apiKey)

    # No match found
    if (reqURL == None):
        return None
    
    try:
        r = req.get(reqURL, timeout=5, verify=False)
        data = r.json()

        if ("ResolveVanityURL" in reqURL):
            return data["response"]["steamid"]
        elif ("GetPlayerSummaries" in reqURL):
            return data["response"]["players"][0]["steamid"]
    except:
        pass
    
    return None

def __genSteamReqURL(profileURL, apiKey):
    if ("/id/" in profileURL):
        vID = profileURL.split("/id/")[-1].split("/")[0]
        return "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={}&vanityurl={}".format(apiKey, vID)
    elif ("/profiles/" in profileURL):
        steamID = profileURL.split("/profiles/")[-1].split("/")[0]
        return "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}".format(apiKey, steamID)

    # Invalid input URL
    return None