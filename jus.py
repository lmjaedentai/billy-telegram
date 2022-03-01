print('==========start==========')
import random
import urllib.request
from pyrogram import Client,filters,emoji
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


#QQ slash commands
app = Client("pokokpisangbot",api_id="17817209",api_hash="1317fd0bcc2b193c3dbd04defc748358",bot_token="5104353128:AAHgalcIDT_Q7MWcAfwmXqvak8rCYD-PPQ4")
with app:
    app.send_message("lmjaedentai", "login")
    print('==========login==========')

@app.on_message(filters.command("banana"))
def start_command(client, message):
    print("This is the /start command")
    message.reply('hi i m back')



app.run()