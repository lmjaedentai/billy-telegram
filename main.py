print('==========start==========')
import json
import random
import asyncio
import requests
import urllib.request
from ytmusicapi import YTMusic
from PyMultiDictionary import MultiDictionary
import mediawiki
from mediawiki import MediaWiki
from pyromod import listen
from pyrogram import Client,filters,emoji
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


#QQ slash commands
app = Client("BillyKaiChengBot",api_id="17817209",api_hash="1317fd0bcc2b193c3dbd04defc748358",bot_token="5277492303:AAFoaZvrUicVyIIjgwG2HyrliGuht4Bda6Q")
with app:
    # app.send_message("lmjaedentai", "login\ndevice: vscode")
    app.send_message("lmjaedentai", "login\ndevice: [heroku](https://replit.com/@lmjaedentai/Billy-Telegram#main.py)", disable_web_page_preview=True)
    print('==========login==========')


@app.on_message(filters.command(["start", "help"]))
async def start_command(client, message):
    await print("This is the /start command")

@app.on_message(filters.command("covid"))
async def start_command(client, message):
    def readcsv(url):
        with urllib.request.urlopen(url) as f:
            last = f.readlines()[-1]
            last2 = last.decode("utf-8") 
            data = last2.split(",")
            return data

    cases = readcsv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv')
    deaths = readcsv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_malaysia.csv')
    await message.reply(f'**🏥 <u>Active: {cases[4]}</u>** \n\n🔴 New cases: `{cases[1]}`\n🟢 Recovered: `{cases[3]}`\n⚫ Death: `{deaths[1]}`\n\nstay home to stay safe'
                    ,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ℹ more info",url="https://covidnow.moh.gov.my/")]]))

@app.on_message(filters.command("shau"))
async def start_command(client, message):
    emoji = ['🖕', '🖕🏻', '🖕🏼','🖕🏽','🖕🏾','🖕🏿']
    content = emoji[random.randint(0,5)]
    for a in range(100):
        content = content + emoji[random.randint(0,5)]
    await message.reply(content)   

@app.on_message(filters.command("sticker"))
async def start_command(client, message):
    await message.delete()
    choose = await message.reply('choose the sticker you want',reply_markup=ReplyKeyboardMarkup([['.xi','.fbi','.rick','.nono'],['.jeng','.abucom','.rainbow'],['.triggered','.SystemError']],resize_keyboard=True))
    await asyncio.sleep(10)
    await choose.delete()

@app.on_message(filters.command("dictionary"))
async def start_command(client, message):
    query = await app.ask(message.chat.id, "🔎 Which word you want to define?")
    dictionary = MultiDictionary()
    rawresult = dictionary.meaning('en', query.text)
    if rawresult[1] != '':
        await message.reply(f'📘 **{query.text}** \n\n{rawresult[1]}'
                            ,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📘 Oxford dictionary",url=f'https://www.oxfordlearnersdictionaries.com/definition/english/{query.text}')]]))
    else:
        await message.reply(f'❌ **No search result** \n\nTry Google.')

@app.on_message(filters.command("kamus"))
async def start_command(client, message):
    query = await app.ask(message.chat.id, "🔎 Apakah perkataan kamu ingin cari?")
    dictionary = MultiDictionary()
    rawresult = dictionary.meaning('ms', query.text)
    if rawresult[1] != '':
        if len(rawresult[1]) > 4095:
            await message.reply(f'📕 **{query.text}** \n\n Definisi terlalu panjang. Anda boleh cari dalam laman web kamus dewan di bawah.'
                            ,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📕 Kamus Dewan",url=f'https://prpm.dbp.gov.my/cari1?keyword={query.text}')]]))
        print(rawresult[1])
        await message.reply(f'📕 **{query.text}** \n\n{rawresult[1]}'
                            ,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📕 Kamus Dewan",url=f'https://prpm.dbp.gov.my/cari1?keyword={query.text}')]]))
    else:
        await message.reply(f'❌ **Carian kata tiada di dalam kamus terkini** \n\nCari Google.')

@app.on_message(filters.command("lyrics"))
async def start_command(client, message):
    return await message.reply('Still under construction 🏗️ 🚧')
    query = await app.ask(message.chat.id, "🔎 What song's lyrics you want?")
    ytmusic = YTMusic()
    rawdata = ytmusic.search(query.text,filter='songs',limit=1)
    print(json.dumps(rawdata, indent = 3))
    return
    browseid = ytmusic.get_watch_playlist(videoid)
    lyrics = ytmusic.get_lyrics(browseid)

@app.on_message(filters.command("wiki"))
async def start_command(client, message):
    wiki = MediaWiki()
    search = await app.ask(message.chat.id, "🔎 Which article you want to search ?")
    try:
        content = wiki.summary(search.text, sentences=5)
    except mediawiki.DisambiguationError as error:
        await message.reply(f'**🤔 Please specify your search query** \n\n{error} \nYour search query matched mutliple pages.')
    except mediawiki.PageError:
        await message.reply(f'❌ **No search result** \n\nTry Google.')
    except Exception as error:
        raise Exception(error)
    else:
        result = wiki.page(search.text)
        await message.reply(f'📖 **{result.title}**\n\n{content}'
                    ,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("wikipedia",url=result.url)]]))




@app.on_message(filters.text & ~filters.edited)
async def my_handler(client, message):
    async def sendwhat(argument):
        switcher = {
            '.rainbow': lambda: message.reply_photo("https://i.imgur.com/DuB3YyZ.png"),
            '.xi': lambda: message.reply_animation("https://c.tenor.com/zD4vOAi7MAoAAAAC/%E6%88%91%E4%BB%AC%E6%80%80%E5%BF%B5%E4%BB%96-%E6%88%91%E5%80%91%E6%87%B7%E5%BF%B5%E4%BB%96.gif"),
            '.fbi': lambda: message.reply_photo("https://scontent.fmkz1-1.fna.fbcdn.net/v/t1.6435-9/86183683_112926100282051_6753412159687884800_n.jpg?_nc_cat=100&ccb=1-5&_nc_sid=e3f864&_nc_eui2=AeFOkSVceEX4WQCb8BgGfJHjwVHujVRN-WnBUe6NVE35aWXNOGT1S2NLy8nSvkPvLp_nJa3Ljtx51EyUSUbDPNSA&_nc_ohc=2S6-BtPGpTQAX8ulcib&_nc_oc=AQmwcGnwDKEGz43j9RhQXgaa8CTYAIFmt1NtlXqNK_uor9AKWtUGgW5WtUBNvpTfhdRzhcR_DGXusoMNNZvm2hQt&_nc_ht=scontent.fmkz1-1.fna&oh=00_AT9qTweXc4ubuogkY1T1rJihqJ8DZ7mE0J-mACPL1SXUYg&oe=62341759"),
            '.rick': lambda: message.reply_animation("https://c.tenor.com/VFFJ8Ei3C2IAAAAM/rickroll-rick.gif"),
            '.nono':  lambda: message.reply_photo('https://www.aixiaola.com/wp-content/uploads/2021/10/c4d36f57bf4cc6e7d0c979398822a755.jpg'),
            '.jeng':lambda: message.reply_animation('https://c.tenor.com/oGICkKJ1Y8QAAAAd/jeng.gif'),
            '.abucom': lambda: message.reply_photo('https://lmjaedentai.github.io/abu/asset/news.jpg'),
            '.triggered': lambda: message.reply_animation('https://c.tenor.com/xVLmXq1yLzQAAAAC/triggered.gif'),
            '.SystemError': lambda: message.reply_photo('https://cdn.vox-cdn.com/thumbor/acSRiL1daqU6Ck5ogaUzuQXMPxU=/0x0:1320x880/1200x800/filters:focal(555x335:765x545)/cdn.vox-cdn.com/uploads/chorus_image/image/69531789/windows11bsod.0.jpg')
        }
        try:
            await switcher[argument]()
        except KeyError:
            pass
    await sendwhat(message.text)
    # print(f'\033[94m {message.text} \033[94m')

@app.on_message(filters.chat([-742050643,-657457191]) & filters.new_chat_members)
async def welcome(client, message):
    MENTION = "[{}](tg://user?id={})"  # User mention markup
    new_members = [u.mention for u in message.new_chat_members]
    await message.reply(f'🥳✨Welcome to the shittest place in telegram {new_members} ! 🚀💩', disable_web_page_preview=True)



# from online import keep_alive 
# keep_alive()
app.run()
