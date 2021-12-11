import random

def randDouble():
    return random.random()

def randInt(start, end):
    """
    Range of result: start <= RESULT <= end
    """
    return int(random.randrange(start, end))

def hexToInt(hex: str):
    try:
        # Removes the #
        if (hex.startswith("#")):
            hex = hex[1::]
        return int(hex, 16)
    except:
        return None

def formatNumber(n):
    """
    1000 -> 1,000
    """
    return f"{n:,}"

def canConvertInt(s):
    try:
        temp = int(s)
        return True
    except ValueError:
        return False