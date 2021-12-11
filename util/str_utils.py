import base64

def encodeBase64(s):
    return base64.b64encode(bytes(s, 'utf-8')).decode('ascii')

def decodeBase64(s):
    try:
        return base64.b64decode(s).decode('ascii')
    except:
        return None

def escapeMD_Text(text):
    for i in "*_|":
        text = text.replace(i, ("\\" + i))
    return text

def bytesToBase64(b):
    return base64.b64encode(b).decode('ascii')