import json
import requests as req

from util.file_utils import readFile

def getJsonFromURL(url) -> dict:
    try:
        r = req.get(url)
        t = r.text

        data = json.loads(t)
        return data
    except:
        return None

def updateJsonFile(p, key, value) -> bool:
    encoding = "utf-8"
    try:

        # Avoid dupelicate entry
        if not (isinstance(key, str)):
            key = str(key)

        f = open(p, 'r', encoding=encoding)
        data = f.read()
        f.close()

        data = json.loads(data)
        data[key] = value

        s = json.dumps(data, indent=4)
        # print(s)
        
        f = open(p, 'w+', encoding=encoding)
        f.write(s)
        f.close()

        return True
    except:
        return False

def readJsonFile(p):
    """
        Reads a json file as dict() and return it \n
        None will be returned if any Exception is raised
    """
    try:
        return json.loads(readFile(p))
    except Exception as e:
        print(e)
        return None

def writeJSON_File(p, data):
    try:
        with open(p, 'w+', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except:
        return False

# This should be useful as a script
# But I'm just gonna put this here first
def beautifyJSON_File(p) -> bool:
    try:
        s = None

        # Read content to str from file
        with open(p, "r", encoding="utf-8") as f:
            s = f.read()
        
        # str -> dict
        data = json.loads(s)

        # dict -> str (beautified str dict)
        s = json.dumps(data, indent=4)

        # Output...
        with open(p, "w+", encoding="utf-8") as f:
            f.write(s)
        
        return True
    except:
        return False