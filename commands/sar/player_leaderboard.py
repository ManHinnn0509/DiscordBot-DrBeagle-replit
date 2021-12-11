import concurrent
import concurrent.futures

import requests as req

class PlayerLeaderboard:
    """
        All rank's position of a player.
    """

    def __init__(self, sessionTicket: str, playFabID: str, template: dict) -> None:
        self.sessionTicket = sessionTicket
        self.playFabID = playFabID
        self.template = template

        self.leaderboardPositions = self.__getPlayerLeaderboardsPosition()
    
    def __getPlayerLeaderboardsPosition(self):
        d = {}

        for category, statDict in self.template.items():
            statKeys = statDict.keys()

            results = None
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = [executor.submit(getLeaderboardAroundPlayer, self.sessionTicket, name, self.playFabID) for name in statKeys]
                concurrent.futures.wait(results)

            # A single r.result() is actually a dict (API call result)
            # Abandon the whole result if one of these data is unablt to format
            datas = []
            try:
                for r in results:
                    data = r.result()["data"]["Leaderboard"][0]

                    # Add 1 in Position part is because the value of "Position" is index
                    datas.append([data["StatValue"], 1 + data["Position"]])
            except Exception as e:
                # print(e)
                return None
            
            d[category] = dict(zip(statKeys, datas))
        
        return d
    
    def update(self, replaceOldData=True):
        """
            Returns the comparing result with old stat data & new stat data

            Format is the same as the template but the list that contains the data is a bit different

            [template]: [STAT_VALUE, POSITION]
            [update]: [STAT VALUE, NEW_POS, POS_DIFF]
        """
        old = self.leaderboardPositions
        new = self.__getPlayerLeaderboardsPosition()

        updateResult = {}
        for (k1, v1), (k2, v2) in zip(old.items(), new.items()):
            # k1 == k2. Picked k1 in here
            category = k1
            statKeys = v1.keys()

            # List. Contains [stat value, position]
            # Reason of not using set... Because it will mess up the order?
            # Not sure but I will keep it as list()
            oldData = list(v1.values())
            newData = list(v2.values())

            dataDiff = []
            for oldL, newL in zip(oldData, newData):
                newStatValue = newL[0]
                newPos = newL[1]
                posDiff = oldL[1] - newPos

                dataDiff.append([newStatValue, newPos, posDiff])

            updateResult[category] = dict(zip(statKeys, dataDiff))
        
        # Replacing... or aka updating lol
        if (replaceOldData):
            self.leaderboardPositions = new

        return updateResult

def getLeaderboardAroundPlayer(sessionTicket, statName, playFabID, maxResultCount=1):
    """
        https://docs.microsoft.com/en-us/rest/api/playfab/client/player-data-management/get-leaderboard-around-player?view=playfab-rest
    """

    url = 'https://titleId.playfabapi.com/Client/GetLeaderboardAroundPlayer'
    h = {
        "X-Authorization": sessionTicket
    }

    b = {
        "StatisticName": statName,
        "PlayFabId": playFabID,
        "MaxResultsCount": maxResultCount,
    }

    r = req.post(url=url, headers=h, json=b)
    if (r.status_code != 200):
        return None
    
    return r.json()