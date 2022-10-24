#keep the server online by using uptimerobot.com
from threading import Thread
from flask import Flask

web = Flask('')

@web.route('/')
def home():
    return "Billy Kaicheng Control Centre"

def run():
  web.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()