import calendar
import time
from datetime import datetime
from dateutil import tz

def convertTime(timeToConv: str, toZone='Asia/Taipei', returnString=False):
    """
        Converts UTC time to GMT+8 (Default) time.
        Returning date time format of this function: %Y-%m-%d %H:%M:%S
    """
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(toZone)

    # Splitted for debugging
    # timeToConv = str(timeToConv)
    t = timeToConv.replace("T", " ")
    t = t.replace("Z", "")
    t = t.split(".")[0]

    utc = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')

    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)

    return str(central) if (returnString) else central

def getDateTimeNow(taipeiTime=True):
    """
        Format example: "2021-05-28 23:45:15"
    """

    # Have to add this parameter and set it to true
    #  for repl.it hosting
    # Otherwise there will be a lot of changes to be done
    if (taipeiTime):
        return getTaipeiTimeNow()

    else:
        now = str(datetime.now())
        now = now.split(".")[0]
        return now

def getTaipeiTimeNow():
    t = str(datetime.now().astimezone(tz.gettz('Asia/Taipei')))
    return t.split('.')[0]

def getTimestampNow():
    return calendar.timegm(time.gmtime())

def getTimestampDetailed():
    return datetime.datetime.now().timestamp()