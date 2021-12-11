from flask import Flask
from threading import Thread
import random
import time
import requests
import logging

app = Flask('')

@app.route('/')
def home():
    return "Discord Bot - Dr Beagle :P"

def run():
    # port = random.randint(2000,9000)
    port = 8080
    app.run(host='0.0.0.0',port=port)

def ping(target, debug):
    while(True):
        r = requests.get(target)
        if (debug == True):
            print(f"[KEEP ALIVE] Status code = {r.status_code}")
        time.sleep(random.randint(30, 60)) #alternate ping time between 3 and 5 minutes

def awake(target, debug=False):  
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.logger.disabled = True  
    t = Thread(target=run)
    r = Thread(target=ping, args=(target,debug,))
    t.start()
    r.start()

'''
# Old version that doesn't work (?)
# I think it requires uptimerobot.com
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Discord Bot - Dr Beagle :P"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
'''