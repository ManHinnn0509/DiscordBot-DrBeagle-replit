def readFile(p):
    try:
        f = open(p, "r", encoding='utf-8')
        data = f.read()
        f.close()
        return data
    except Exception as e:
        print(e)
        return None

def writeFile(p, data):
    try:
        f = open(p, "w+", encoding='utf-8')
        f.write(data)
        f.close()
        return True
    except:
        return False