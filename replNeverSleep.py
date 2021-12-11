from flask import Flask
from threading import Thread

import random
import time
import requests
import logging

app = Flask('')

@app.route('/')
def main():
    '''
    from variables import commandCallHistory
    s = ""

    if (len(commandCallHistory) != 0):
        s = '<br>'.join(list(reversed(commandCallHistory)))

    html = f"""
    <html style="background-color: #000000">
        <head>
            <h1 style="color: white;">
                Dr. Beagle is alive!
            </h1>
        </head>

        <body>
            <p style="color: aqua; font-size: 110%">
                Command call history:
            </p>

            <p style="color: #00FF00">
                {s}
            </p>
        </body>

    </html>
    """
    '''

    return 'Bot is alive!'

def run():
    app.run(host="0.0.0.0", port=8080)

def ping(target, debug):

    while (True):
        try:
            r = requests.get(target, verify=False)
            if (debug == True):
                print(f"status code = {r.status_code}")
        except Exception as e:
            print(f"Exception caught: {e}")

        # Alternate ping time between 3 and 5 minutes
        time.sleep(random.randint(30, 60)) 

def awake(target, debug=False):  
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.logger.disabled = True  
    t = Thread(target=run)
    r = Thread(target=ping, args=(target,debug,))
    t.start()
    r.start()