print('==========start==========')
import os 
import sys
sys.path.append('./module') 
import csv
import pytz
import random
import urllib
import asyncio
import datetime
import traceback
import mediawiki
import lyricsgenius as lg
from telegraph import Telegraph
from mediawiki import MediaWiki
from word_forms.lemmatizer import lemmatize
from PyMultiDictionary import MultiDictionary, DICT_WORDNET
from pyromod import listen
from pyrogram import Client,filters,emoji, errors
from pyrogram.types import Message, InlineKeyboardButton, KeyboardButton,ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineQuery, InlineQueryResultArticle,InlineQueryResultPhoto, InputTextMessageContent, ForceReply, ReplyKeyboardRemove
from module.pytube import YouTube, exceptions
from module.google_trans_new import google_translator  
# from google_trans_new import google_translator  

#LINK https://www.youtube.com/watch?v=qeBjVJkOAGc oracle

#QQ before we start
telegraph = Telegraph()
telegraph.create_account(short_name='billy')
genius = lg.Genius("zdhRYLihRzp3sUoJRFBcEOuMp_Z3eHTIGDbDzbMPqs_PmyPOSMGgYm2YxhpYRjte", skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
translator = google_translator(url_suffix="my") 
app = Client("BillyKaiChengBot",api_id="17817209",api_hash=os.environ['API'],bot_token=os.environ['TOKEN'])
# app = Client("billybetabot",api_id="17817209",api_hash=os.environ['API'],bot_token='5456415338:AAGyHTNPA2Bi1CHV0ERseo13XVU_WYP5SiY')

#for repl
import nltk
nltk.download('omw-1.4')

with app:
    # app.send_message(-1001518766606, "#login\ndevice: vscode")
    app.send_message(-1001518766606, "#login\ndevice: [repl.it](https://replit.com/@lmjaedentai/billy-telegram#main.py)", disable_web_page_preview=True,disable_notification=True)
    print('==========login==========')


def error_handling(func):
    async def inner(app,message: Message,**kwargs): #kwargs mean any other args avai
        try:
            if func.__name__ != 'on_message':
                # await app.send_message(-1001518766606,'👤 /'+func.__name__)
                pass
            await func(app,message,**kwargs)
        except errors as error:
            fullerror = "".join(traceback.TracebackException.from_exception(error).format())
            printerror = await app.send_message(-1001518766606,f'❌ **{error}**\n```\n{fullerror}\n```#error', disable_web_page_preview=True)
            await app.send_message(message.chat.id,f"⁉️ **[Telegram API error]({printerror.link})**\n\nWe are sorry for that   /help", disable_web_page_preview=True)
            traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)
        except Exception as error:
            fullerror = "".join(traceback.TracebackException.from_exception(error).format())
            printerror = await app.send_message(-1001518766606,f'❌ **{error}**\n```\n{fullerror}\n```#error', disable_web_page_preview=True)
            await app.send_message(message.chat.id,f"❌ **[An unexpected error has occur]({printerror.link})** \n```\n{error}\n```\nWe are sorry for that   /help", disable_web_page_preview=True)
            traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)
    return inner

def shau():
    emoji = ['🖕', '🖕🏻', '🖕🏼','🖕🏽','🖕🏾','🖕🏿']
    content = emoji[random.randint(0,5)]
    for a in range(59):
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
        


#QQ slash cmd
@app.on_message(filters.command("shau"))
@error_handling
async def sendshau(client, message):
    instructiion = await message.reply("GO",reply_markup=ReplyKeyboardMarkup([[shau(),shau()],[shau(),shau()]]))
    await asyncio.sleep(2)
    await instructiion.delete()
    await asyncio.sleep(20)
    remove = await message.reply("times up",reply_markup=ReplyKeyboardRemove())
    await remove.delete()

@app.on_message(filters.command(["dict","d","dictionary"]))
@error_handling
async def dictionary(client, message):
    targetlist = ['n.','adv.','adj.','v.','prep.','int.','conj.','art.','1.','2.','3.','4.','5.','6.','7.','8.','9.','10.','[','|| ','] ','/']
    replacelist = ['\n\nNoun: ','\n\nAdverb: ','\n\nAdjective: ','\n\nVerb: ','\n\nPreposition: ','\n\nInterjection: ','\n\nConjunction: ','\n\nArticles:','\n1.','\n2.','\n3.','\n4.','\n5.','\n6.','\n7.','\n8.','\n9.','\n10.','\n • ','\n\nExample:\n • ','\n • ','/ ']
    dictionary = MultiDictionary()
    def cndict(search):
        text = ''
        success = False
        with open('dict pro.csv', 'r', encoding='utf-8') as f:
            for row in csv.reader(f, delimiter=","):
                if search == row[0]:
                    success = True
                    for i in row:
                        text += i  
                    text = text.replace(search,'',1).replace(row[1],f'')
                    break
                elif f'{search} 1'== row[0]:
                    success = True
                    for i in row:
                        text += i  
                    text = text.replace(f'{search} 1','',1).replace(row[1],f'')
                    search = f'{search} 2'
        if success:
            for i in range(len(targetlist)):
                text = text.replace(targetlist[i],replacelist[i])
            return text
        else:
            return False

    query = await app.ask(message.chat.id, "🔎 Enter a word to define",filters=filters.user(message.from_user.id) ,reply_markup = ForceReply(placeholder="exp: Daydreamer"),)
    typing = await app.send_message(message.chat.id,'searching...')
    search = query.text.lower()
    #english dict
    try:
        rawresult = dictionary.meaning('en',search, dictionary=DICT_WORDNET)
    except IndexError: #no result
        pass
    else:
        i = 0
        result = ''
        for types in ['Noun','Verb','Adjective','Adverb']:
            if types in rawresult:
                result+=f'\n{types}\n'
                for meanings in rawresult[types]:
                    i+=1
                    result += f'{i}. {meanings}\n'
        await app.send_message(message.chat.id,f'📘 **[{search}](https://www.oxfordlearnersdictionaries.com/definition/english/{search.replace(" ","%20")})** \n{result}‎ ')
    #cn dict
    zh = cndict(search)
    if zh == False or zh == '': #no result
        try:
            search = lemmatize(search)
            zh = cndict(search) #try base form / lemma word
        except ValueError: #word_form module: no word in this world
            return await message.reply(f'❌ **No search result**   /help',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f'https://www.google.com/search?q={search.replace(" ","%20")}')]]))
        else:
            if zh == False: #dict.pro do not hav
                zh = f"\n{translator.translate(search,lang_tgt='zh')}"
                if zh.lower().strip() == search.strip() or zh=='':  #google trans do not hav
                    return await message.reply(f'❌ **No search result**   /help',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f'https://www.google.com/search?q={search.replace(" ","%20")}')]]))
    await app.send_message(message.chat.id,f'👲🏻**中文注释**\n{zh}',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙏 Credits",url=f'https://github.com/mahavivo/english-wordlists')]]))
    await typing.delete()

@app.on_message(filters.command(["kamus","k"]))
@error_handling
async def kamus(client, message):
    query = await app.ask(message.chat.id, "🔎 Masukkan perkataan yang anda ingin cari",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder="contoh: Almari"))
    typing = await app.send_message(message.chat.id,'searching...')
    zh = translator.translate(query.text,lang_tgt='zh') 
    if zh.lower().strip() == query.text.lower().strip() or zh=='': 
        await app.send_message(message.chat.id,f'❌ **Carian kata tiada di dalam kamus terkini**   /help',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Cari Google.",url=f'https://www.google.com/search?q={query.text.replace(" ","%20")}')]]))
    else: 
        await app.send_message(message.chat.id,f'📕 **{query.text}** \n\n👲 {zh}\n\n**[➡️ lihat selanjutnya](https://www.ekamus.info/index.php/term/%E9%A9%AC%E6%9D%A5%E6%96%87-%E5%8D%8E%E6%96%87%E5%AD%97%E5%85%B8,{query.text.replace(" ","%20").lower()}.xhtml)**')#, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📕 Kamus Dewan",url=f'https://prpm.dbp.gov.my/cari1?keyword={query.text.replace(" ","%20")}'),InlineKeyboardButton("🔎 ekamus (bc)",url=f'https://www.ekamus.info/index.php/?a=srch&d=1&q={query.text.replace(" ","%20")}')]]))
    await typing.delete()

@app.on_message(filters.command("lyrics"))
@error_handling
async def findlyrics(client, message):
    query = await app.ask(message.chat.id, "🎸 Tell me the **song title** __follow by the name of artist (optional)__",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder="Perfect Ed Sheeran"))
    typing = await app.send_message(message.chat.id,'searching...')
    try:
        lyrics = genius.search_song(query.text, get_full_info=True)
    except:
        await app.send_message(message.chat.id,f"☹️ No search result\n\n **or**\n\n**[😀 Try Mojim.com](https://mojim.com/{query.text.replace(' ','%20')}.html?g3)**")#,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f"https://www.google.com/search?q={query.text.replace(' ','%20')}%20lyrics")]]))
    if lyrics is None:
        await app.send_message(message.chat.id,f"☹️ No search result\n\n **or**\n\n**[😀 Mojim.com](https://mojim.com/{query.text.replace(' ','%20')}.html?g3)**")#,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f"https://www.google.com/search?q={query.text.replace(' ','%20')}%20lyrics")]]))
    else:
        response = telegraph.create_page(query.text, html_content='🎸'+lyrics.lyrics.replace("\n", "<br>").replace("Lyrics", "<br>").replace("You might also like", "<br>").replace("Embed", "<br>") , author_name=lyrics.primary_artist.name, author_url=lyrics.primary_artist.url.replace(' ','%20'))
        await app.send_message(message.chat.id,response['url'],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎧 listen",url=f"https://www.youtube.com/results?search_query={query.text}".replace(' ','%20'))],[InlineKeyboardButton("not this one ☹️",url=f"https://mojim.com/{query.text.replace(' ','%20')}.html?g3")]]))
    await typing.delete()

@app.on_message(filters.command("youtube")) #https://www.youtube.com/watch?v=wiHYx9NX4DM
@error_handling
async def music(client, message):
    def checkvalid(url):
        try:
            YouTube(url).title 
        except exceptions.RegexMatchError:
            return message.reply("❌ **Invalid query.** \nWe only support videos from Youtube.   /music")
        else:
            return url
    #download
    query = await app.ask(message.chat.id, "🎺 Enter **link** from Youtube",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder="paste link here"))
    url = checkvalid(query.text)
    status = await query.reply("⬇️  downloading media...")
    music = YouTube(url).streams.filter(file_extension='mp4').order_by('resolution').desc().first().download()
    # await status.delete()
    #convert
    status = await status.edit_text("➡️  sending media...")
    # base, ext = os.path.splitext(music)
    # new_file = base + '.mp3'
    # os.rename(music, new_file)
    #send
    await query.reply_document(music,caption=YouTube(query.text).title,force_document=False)
    await status.delete()
    os.remove(music)



@app.on_message(filters.command(["other","more"]))
@error_handling
async def others(client, message):
    i = await message.reply('Select the feature you want',reply_markup=ReplyKeyboardMarkup([['/help'],['/calc'],['/kamus'],['/translate'],['/covid'],['/wiki'],['/peribahasa']],resize_keyboard=True))
    await asyncio.sleep(2)
    await i.delete()

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

@app.on_message(filters.command("wiki"))
@error_handling
async def wiki(client, message):
    search = await app.ask(message.chat.id, "🔎 Enter name of article to search ",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder="exp: Tiananmen square"))
    try:
        result = MediaWiki().page(search.text)
    except mediawiki.DisambiguationError as suggestion:
        await search.reply(f'**🤔 Please specify your search query** \n{suggestion} \n\n**Your search query matched mutliple pages.**\n\n/wiki')
    except mediawiki.PageError:
        await search.reply(f'❌ **No search result** Try Google.',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Google",url=f"https://www.google.com/search?q={search.text.replace(' ','%20')}")]]))
    else:
        await app.send_message(message.chat.id,f"📖 **{result.title}**\n\n{result.url.replace(' ','%20')}\n‎")

@app.on_message(filters.command("calc"))
@error_handling
async def calc(client, message):
    query = await app.ask(message.chat.id, "🔢 Type your formula here.\nSupport basic math only. ",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder='send "how" for instruction '))
    if "how" in query.text.lower():
        return await app.send_message(message.chat.id, "https://telegra.ph/Calc-in-Billy-KaiCheng-07-10")
    try:
        formula = query.text.replace("^","**")
        formula = formula.replace("x","*")
        answer = eval()
    except (ValueError, SyntaxError, NameError, TypeError) as error:
        await app.send_message(message.chat.id,"❌ Invalid input. \n\n[📗 Cymath Algerbra Solver](https://cymath.com)\n[📱 Android Scienctific Calculator](http://play.google.com/store/apps/details?id=advanced.scientific.calculator.calc991.plus)",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❓ How to use",url=f'https://telegra.ph/Calc-in-Billy-KaiCheng-07-10')]]), disable_web_page_preview=True)
    else:
        await message.reply(answer)

@app.on_message(filters.command("translate"))
@error_handling
async def translate(client, message):
    async def asklang():
        global code
        choice = await app.ask(message.chat.id,'Select the language you want translate **to**',filters=filters.user(message.from_user.id),reply_markup=ReplyKeyboardMarkup([['🇬🇧 English','🇲🇾 Bahasa Melayu','🇹🇼 正体中文']],resize_keyboard=True))
        if choice.text == '🇬🇧 English':
            return 'en'
        elif choice.text == '🇲🇾 Bahasa Melayu':
            return 'ms'
        elif choice.text == '🇹🇼 正体中文':
            return 'zh-tw'
        else:
            await asklang()
    code = await asklang()
    query = await app.ask(message.chat.id, f"🔣 Enter the word translate to {code}",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder="I love carrot"))
    await app.send_message(message.chat.id,f'{query.text}\n⇓\n{translator.translate(query.text,lang_tgt=code)}')

@app.on_message(filters.command("remind"))
@error_handling
async def remind(client, message):
    reminder = await app.ask(message.chat.id, f"🔔 What should I remind you?",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder="this feature is unstable"))
    rawtime = await app.ask(message.chat.id, f"🕒 Pick a time to remind",filters=filters.user(message.from_user.id),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("How? 🤔",callback_data="data")]]))
    time = rawtime.text
    time_convert = {"s":1, "m":60, "h":3600,"d":86400}
    try:
        seconds = int(time[:-1]) * time_convert[time[-1]]
    except (ValueError, KeyError,TypeError):
        return await app.send_message(message.chat.id,f"**❌ Invalid input**\nClick this to see instructions 👇🏻 then try again /remind",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("instructions",callback_data="data")]]))
    rawdate = pytz.timezone('Asia/Kuala_Lumpur').localize(datetime.datetime.now()) + datetime.timedelta(seconds = seconds) # UTC8 + delaytime
    if seconds <= 0:
        await app.send_message(message.chat.id,f'❌ No zero or negative value')
    elif seconds > 7776000:
        await app.send_message(message.chat.id,f'❌ Maximum duration is 90 days.')
    else: 
        await app.send_message(message.chat.id,f"🔔 Alright, I will remind you **{reminder.text}** in **{time}** at **{datetime.datetime.fromtimestamp(round(rawdate.timestamp()))}**")
        await asyncio.sleep(seconds)
    await reminder.reply(f'🔔 Reminder for [{reminder.text}]({reminder.link})\n🕒 set **{time}** ago\n\n`dont forget lol`',disable_web_page_preview=True)

@app.on_callback_query()
async def reminder_instructions(client, callback_query):
    await callback_query.answer(f"You can enter any time value you like\nby following format below.\n\nFor example:\n\n10 second  : 10s\n10 minutes : 10m\n10 hours     : 10h\n10 days       : 10d\n\nThis beta feature currently is unstable.",show_alert=True)

@app.on_message(filters.command(["start","help"]))
@error_handling
async def test(client, message):
    await app.send_message(message.chat.id,'2022 coded in Python\n[source](https://github.com/lmjaedentai/billy-telegram#readme) • [about](https://telegra.ph/Billy-KaiCheng-09-04) • [feedback](https://github.com/lmjaedentai/billy-telegram/issues/new/choose)\n\n**Main Command**\n• dont touch /shau\n• cn to en /dictionary\n• download /youtube\n• search song /lyrics\n\n**/more Subcommand**\n• google /translate\n• simple math /calc\n• malay /kamus\n• real time statistics /covid\n• search for /wiki\n• cari /peribahasa',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("go touch grass 🍃",url=f'https://en.wikipedia.org/wiki/Poaceae')]]), disable_web_page_preview=True)

@app.on_message(filters.command("peribahasa"))
@error_handling
async def peribahasa(client, message):
    query = await app.ask(message.chat.id, "🔎 Masukkan peribahasa yg anda ingin cari",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder="by maksudperibahasa.com"))
    await app.send_message(message.chat.id,f"📕 **{query.text}** \n\nhttps://maksudperibahasa.com/?s={query.text.replace(' ','-')}/")
    await app.send_message(message.chat.id,f"👲 **中文注释** \n\nhttps://www.ekamus.info/index.php/term/Simpulan+Bahasa+%26amp%3B+Peribahasa,{query.text.replace(' ','+')}.xhtml")





#QQ other cmd
@app.on_message(filters.text)
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


#QQ tracking
import time
def foo():
  print("foo", time.time())
  app.send_message(-1001518766606, f"#online {pytz.timezone('Asia/Kuala_Lumpur').localize(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}", disable_web_page_preview=True,disable_notification=True)

def every(delay, task):
  next_time = time.time() + delay
  while True:
    time.sleep(max(0, next_time - time.time()))
    try:
      task()
    except Exception:
      traceback.print_exc()
    next_time += (time.time() - next_time) // delay * delay + delay

import threading
threading.Thread(target=lambda: every(60, foo)).start()




from online import keep_alive 
keep_alive()
stickerlist = getsticker()
app.run()