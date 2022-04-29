print('==========start==========')
import re
import os
import sys
import csv
import json
import random
import urllib
import asyncio
import requests
import traceback
import mediawiki
import lyricsgenius as lg
from mediawiki import MediaWiki
from pytube import YouTube, exceptions
from PyMultiDictionary import MultiDictionary, DICT_WORDNET
from pyromod import listen
from pyrogram import Client,filters,emoji, errors
from pyrogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineQuery, InlineQueryResultArticle,InlineQueryResultPhoto, InputTextMessageContent


#QQ before we start
genius = lg.Genius("zdhRYLihRzp3sUoJRFBcEOuMp_Z3eHTIGDbDzbMPqs_PmyPOSMGgYm2YxhpYRjte", skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
app = Client("BillyKaiChengBot",api_id="17817209",api_hash="1317fd0bcc2b193c3dbd04defc748358",bot_token="5277492303:AAFoaZvrUicVyIIjgwG2HyrliGuht4Bda6Q")
with app:
    app.send_message(-1001518766606, "login\ndevice: vscode")
    # app.send_message(-1001518766606, "login\ndevice: [repl.it](https://replit.com/@lmjaedentai/Billy-Telegram#main.py)", disable_web_page_preview=True,disable_notification=True)
    print('==========login==========')


def error_handling(func):
    async def inner(app,message: Message,**kwargs): #kwargs mean any other args avai
        try:
            if func.__name__ != 'on_message':
                await app.send_message(-1001518766606,'👤 /'+func.__name__)
            await func(app,message,**kwargs)
        except Exception as error:
            fullerror = "".join(traceback.TracebackException.from_exception(error).format())
            printerror = await app.send_message(-1001518766606,f'❌ **{error}**\n```\n{fullerror}\n```\n', disable_web_page_preview=True)
            await app.send_message(message.chat.id,f"❌ **An unexpected error has occur** \n```\n{error}\n```\nWe are sorry for that. [Fullerror]({printerror.link})")
            traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)
    return inner

def shau():
    emoji = ['🖕', '🖕🏻', '🖕🏼','🖕🏽','🖕🏾','🖕🏿']
    content = emoji[random.randint(0,5)]
    for a in range(100):
        content = content + emoji[random.randint(0,5)]
    return content

async def shutdown(app,message):
    if message.from_user.id in [986857222,1499315224]:
        await message.reply('shutting down...')
        await app.send_message(-1001518766606,f'😴  shut down by **{message.from_user.username}**')
        sys.exit(f'shut down by **[{message.from_user.username}]**')
    else:
        await message.reply('❌ No admin rights')

def getsticker():
    with open('sticker.csv') as csv_file:
        urllist = list()
        final = list()
        final.append(InlineQueryResultArticle(title='晨曦云',thumb_url='https://i.imgur.com/ZqGgNt5.jpg', input_message_content=InputTextMessageContent(shau())))
        for i in csv.reader(csv_file, delimiter=','):
            urllist.append(i[0])
        
    for sticker in urllist:
        final.append(InlineQueryResultPhoto(photo_url=sticker))
    return final
        
def checkvalid(url):
    try:
        title = YouTube(url).title 
    except exceptions.RegexMatchError:
        return False
    else:
        return True





#QQ slash cmd
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

@app.on_message(filters.command("chenxiyun"))
async def sendshau(client, message):
    await message.reply('Try @billy',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Try now.",switch_inline_query_current_chat='chenxiyun')]]))

@app.on_message(filters.command("dict"))
@error_handling
async def dictionary(client, message):
    dictionary = MultiDictionary()
    query = await app.ask(message.chat.id, "🔎 Which word you want to define?")
    rawresult = dictionary.meaning('en',query.text, dictionary=DICT_WORDNET)
    try:
        zh = dictionary.translate('en', query.text, to='zh')[-1][1]
    except IndexError:
        zh = '[无法查询相关词汇]'
    if not rawresult:
        await message.reply(f'❌ **No search result**',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f'https://www.google.com/search?q={query.text.replace(" ","%20")}')]]))
    else:
        result='Noun\n'
        i = 0
        for meanings in rawresult['Noun']:
            i+=1
            result += f'{i}. {meanings}\n'
        if 'Verb' in rawresult:
            result += '\nVerb\n'
            for meanings in rawresult['Verb']:
                i+=1
                result += f'{i}. {meanings}\n'
        await app.send_message(message.chat.id,f'📘 **{query.text}** \n\n{result}\n👲🏻 {zh}',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📘 Oxford",url=f'https://www.oxfordlearnersdictionaries.com/definition/english/{query.text.lower().replace(" ","%20")}'),InlineKeyboardButton("🔎 Google",url=f'https://www.google.com/search?q=define%20{query.text.replace(" ","%20")}')]]))
 

@app.on_message(filters.command("kamus"))
@error_handling
async def kamus(client, message):
    dictionary = MultiDictionary()
    query = await app.ask(message.chat.id, "🔎 Apakah perkataan kamu ingin cari?")
    rawresult = dictionary.meaning('ms', query.text)
    try:
        zh = dictionary.translate('ms', query.text, to='zh')[-1][1]
    except IndexError:
        zh = '[无法查询相关词汇]'
    if rawresult[1] != '':
        await app.send_message(message.chat.id,f'📕 **{query.text}** \n\n{rawresult[1][0:4000]}\n\n👲 {zh}', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📕 Kamus Dewan",url=f'https://prpm.dbp.gov.my/cari1?keyword={query.text.replace(" ","%20")}'),InlineKeyboardButton("🔎 ekamus (bc)",url=f'https://www.ekamus.info/index.php/?a=srch&d=1&q={query.text.replace(" ","%20")}')]]))
    else:
        await message.reply(f'❌ **Carian kata tiada di dalam kamus terkini**',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Cari Google.",url=f'https://www.google.com/search?q={query.text.replace(" ","%20")}')]]))

@app.on_message(filters.command("wiki"))
@error_handling
async def wiki(client, message):
    wiki = MediaWiki()
    search = await app.ask(message.chat.id, "🔎 Which article you want to search ?")
    try:
        content = wiki.summary(search.text, sentences=5)
    except mediawiki.DisambiguationError as error:
        await message.reply(f'**🤔 Please specify your search query** \n\n{error} \nYour search query matched mutliple pages.')
    except mediawiki.PageError:
        await message.reply(f'❌ **No search result** \n\nTry Google.',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Google",url=f"https://www.google.com/search?q={search.text.replace(' ','%20')}")]]))
    except Exception as error:
        raise Exception(error)
    else:
        result = wiki.page(search.text)
        await app.send_message(message.chat.id,f'📖 **{result.title}**\n\n{content}',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📖 Wikipedia",url=result.url.replace(' ','%20'))]]))

@app.on_message(filters.command("lyrics"))
@error_handling
async def findlyrics(client, message):
    query = await app.ask(message.chat.id, "🎸 Which song lyrics you want?",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💫 Powered by GeniusApi",url=f'https://genius.com/')]]))
    lyrics = genius.search_song(query.text, get_full_info=True)

    if lyrics is None or len(lyrics.lyrics) > 2045:
        await message.reply(f'❌ **No search result**',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f'https://www.google.com/search?q={query.text}%20lyrics')]]))
    else:
        formatlyrics = '**🎸 '+lyrics.lyrics.replace("Embed", "").replace('Lyrics',f'Lyrics**\n🎤 [{lyrics.primary_artist.name}]({lyrics.primary_artist.url})\n')
        url = f"\n[🎧](https://www.youtube.com/results?search_query={query.text})".replace(' ','%20')
        await message.reply(formatlyrics+url, disable_web_page_preview=True)

@app.on_message(filters.command("meet"))
@error_handling
async def createmeet(client, message):
    await message.reply_photo("https://piunikaweb.com/wp-content/uploads/2020/11/google-meet.png",caption='support MOE only.'
    ,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🐢 click to join",url=f'https://accounts.google.com/AccountChooser/signinchooser?continue=https://g.co/meet/pythongroup')]]))

@app.on_message(filters.command("music"))
@error_handling
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

@app.on_message(filters.command("calc"))
@error_handling
async def calc(client, message):
    query = await app.ask(message.chat.id, "🔢 Type your formula here. ",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❓ How to use",url=f'https://gist.github.com/lmjaedentai/7a45c849deecf3412f2f30c6ea2ad562#calc-in-billy-kaicheng')]]))
    try:
        answer = eval(query.text)
    except (ValueError, SyntaxError, NameError) as error:
        await app.send_message(message.chat.id,"❌ Invalid input. \n\n[📗 Cymath Algerbra Solver](https://cymath.com)\n[📱 Android Scienctific Calculator](http://play.google.com/store/apps/details?id=advanced.scientific.calculator.calc991.plus)",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❓ How to use",url=f'https://gist.github.com/lmjaedentai/7a45c849deecf3412f2f30c6ea2ad562#calc-in-billy-kaicheng')]]), disable_web_page_preview=True)
    else:
        await message.reply(answer)




#QQ other cmd
@app.on_message(filters.chat([-1001197820173]) & filters.new_chat_members)
async def welcome(client, message):
    MENTION = "[{}](tg://user?id={})"  # User mention markup
    new_members = [u.mention for u in message.new_chat_members]
    await message.reply(f'🥳 ✨ Welcome to the shittest place in telegram {new_members} ! 🚀  💩', disable_web_page_preview=True)

@app.on_message(filters.text & ~filters.edited)
@error_handling
async def on_message(client, message):
    async def minicmd(argument):
        switcher = {
            '.id': lambda: message.reply(message.chat.id),
            '.err': lambda: this_is_an_error(),
            '.shutdown': lambda: shutdown(client,message),
        }
        try:
            await switcher[argument]()
        except KeyError:
            pass
    await minicmd(message.text)

@app.on_inline_query()
# @error_handling
def sticker(client, inline_query):
    # print(inline_query.query)
    if inline_query.query == 'chenxiyun':
        result = [InlineQueryResultArticle(title='晨曦云',thumb_url='https://i.imgur.com/ZqGgNt5.jpg', input_message_content=InputTextMessageContent(shau()))]
    else:
        result = stickerlist
    inline_query.answer(is_gallery=True,results=result,cache_time=1)






# from online import keep_alive 
# keep_alive()
stickerlist = getsticker()
app.run()