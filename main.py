print('==========start==========')
import os
import json
import random
import asyncio
import requests
import urllib.request
import mediawiki
import lyricsgenius as lg
from mediawiki import MediaWiki
from pytube import YouTube
from PyMultiDictionary import MultiDictionary
from pyromod import listen
from pyrogram import Client,filters,emoji, errors
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackGame


#QQ slash commands
dictionary = MultiDictionary()
wiki = MediaWiki()
genius = lg.Genius("zdhRYLihRzp3sUoJRFBcEOuMp_Z3eHTIGDbDzbMPqs_PmyPOSMGgYm2YxhpYRjte", skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
app = Client("BillyKaiChengBot",api_id="17817209",api_hash="1317fd0bcc2b193c3dbd04defc748358",bot_token="5277492303:AAFoaZvrUicVyIIjgwG2HyrliGuht4Bda6Q")
with app:
    app.send_message("lmjaedentai", "login\ndevice: vscode")
    # app.send_message("lmjaedentai", "login\ndevice: [repl.it](https://replit.com/@lmjaedentai/Billy-Telegram#main.py)", disable_web_page_preview=True,disable_notification=True)
    print('==========login==========')


@app.on_message(filters.command("covid"))
async def covid(client, message):
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
async def sticker(client, message):
    try:
        await message.delete()
    except errors.exceptions.forbidden_403.MessageDeleteForbidden:
        pass
    choose = await message.reply('choose the sticker you want',reply_markup=ReplyKeyboardMarkup([['.xi','.fbi','.rick','.nono'],['.jeng','.abucom','.rainbow'],['.triggered','.SystemError']],resize_keyboard=True))
    await asyncio.sleep(10)
    await choose.delete()

@app.on_message(filters.command("dictionary"))
async def dictionary(client, message):
    query = await app.ask(message.chat.id, "🔎 Which word you want to define?")
    rawresult = dictionary.meaning('en', query.text)
    if rawresult[1] != '':
        await message.reply(f'📘 **{query.text}** \n\n{rawresult[1]}',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📘 Oxford",url=f'https://www.oxfordlearnersdictionaries.com/definition/english/{query.text}'),InlineKeyboardButton("🔎 Google",url=f'https://www.google.com/search?q=define%20{query.text}')]]))
    else:
        await message.reply(f'❌ **No search result**',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f'https://www.google.com/search?q={query.text}')]]))

@app.on_message(filters.command("kamus"))
async def kamus(client, message):
    query = await app.ask(message.chat.id, "🔎 Apakah perkataan kamu ingin cari?")
    rawresult = dictionary.meaning('ms', query.text)
    if rawresult[1] != '':
        if len(rawresult[1]) > 4095:
            await message.reply(f'📕 **{query.text}** \n\nDefinisi terlalu panjang. Anda boleh cari melalui kamus online.', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📕 Kamus Dewan",url=f'https://prpm.dbp.gov.my/cari1?keyword={query.text}'),InlineKeyboardButton("🔎 ekamus (bc)",url=f'https://www.ekamus.info/index.php/?a=srch&d=1&q={query.text}')]]))
            return
        await message.reply(f'📕 **{query.text}** \n\n{rawresult[1]}', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📕 Kamus Dewan",url=f'https://prpm.dbp.gov.my/cari1?keyword={query.text}'),InlineKeyboardButton("🔎 ekamus (bc)",url=f'https://www.ekamus.info/index.php/?a=srch&d=1&q={query.text}')]]))
    else:
        await message.reply(f'❌ **Carian kata tiada di dalam kamus terkini**',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Cari Google.",url=f'https://www.google.com/search?q={query.text}')]]))

@app.on_message(filters.command("wiki"))
async def wiki(client, message):
    search = await app.ask(message.chat.id, "🔎 Which article you want to search ?")
    try:
        content = wiki.summary(search.text, sentences=5)
    except mediawiki.DisambiguationError as error:
        await message.reply(f'**🤔 Please specify your search query** \n\n{error} \nYour search query matched mutliple pages.')
    except mediawiki.PageError:
        await message.reply(f'❌ **No search result** \n\nTry Google.',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Google",url=f'https://www.google.com/search?q={search.text}')]]))
    except Exception as error:
        raise Exception(error)
    else:
        result = wiki.page(search.text)
        await message.reply(f'📖 **{result.title}**\n\n{content}',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📖 Wikipedia",url=result.url)]]))

@app.on_message(filters.command("lyrics"))
async def findlyrics(client, message):
    query = await app.ask(message.chat.id, "🎸 Which song lyrics you want?",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💫 Powered by GeniusApi",url=f'https://genius.com/')]]))
    lyrics = genius.search_song(query.text, get_full_info=True)
    if lyrics is None:
        await message.reply(f'❌ **No search result**',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f'https://www.google.com/search?q={query.text}%20lyrics')]]))
    else:
        await message.reply('**🎸 '+lyrics.lyrics.replace("Embed", "").replace('Lyrics','Lyrics**\n\n'))

@app.on_message(filters.command("meet"))
async def createmeet(client, message):
    await message.reply_photo("https://i.imgur.com/9k81Efw.png",caption='support MOE only.'
    ,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🐢 click to join",url=f'https://accounts.google.com/AccountChooser/signinchooser?continue=https://g.co/meet/pythongroup')]]))

@app.on_message(filters.command("music"))
async def music(client, message):
    #download
    query = await app.ask(message.chat.id, "🎺 What is the **url** of youtube mp3 you want to download?")
    if checkvalid(query.text) == False:
        return await message.reply("❌ **Invalid url.** We only support videos from Youtube. ")
    await app.send_chat_action(message.chat.id, "typing")
    status = await message.reply("⬇️  downloading media...")
    music = YouTube(query.text).streams.filter(file_extension='mp4',only_audio=True).order_by('resolution').desc().first().download()
    await status.delete()
    #convert
    await app.send_chat_action(message.chat.id, "upload_video")
    status = await message.reply("➡️  sending media...")
    base, ext = os.path.splitext(music)
    new_file = base + '.mp3'
    os.rename(music, new_file)
    #send
    await message.reply_document(new_file,caption=YouTube(query.text).title,force_document=True)
    await app.send_chat_action(message.chat.id, "cancel")
    await status.delete()
    os.remove(new_file)

@app.on_callback_query()
async def openquery(client, callback_query): #show text "hello" and open my html 5 game through `url` para
    await callback_query.answer(url='https://lmjaedentai.github.io/popspike')

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
            '.abucom': lambda: message.reply_photo('https://lmjaedentai.github.io/abu/asset/news.jpg',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌸 Start",url=f'https://lmjaedentai.github.io/abu')]])),
            '.triggered': lambda: message.reply_animation('https://c.tenor.com/xVLmXq1yLzQAAAAC/triggered.gif'),
            '.SystemError': lambda: message.reply_photo('https://cdn.vox-cdn.com/thumbor/acSRiL1daqU6Ck5ogaUzuQXMPxU=/0x0:1320x880/1200x800/filters:focal(555x335:765x545)/cdn.vox-cdn.com/uploads/chorus_image/image/69531789/windows11bsod.0.jpg'),
            '.meet': lambda: message.reply('https://meet.google.com/new')
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