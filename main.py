print('==========start==========')
import os
import sys
sys.path.append('./module') 
import csv
import nltk
import time
import random
import urllib
import requests
import asyncio
import datetime
import threading
import traceback
import mediawiki
import pastebinpy as pbp
from telegraph import Telegraph
from mediawiki import MediaWiki
from imgur_python import Imgur
from word_forms.lemmatizer import lemmatize
from PyMultiDictionary import MultiDictionary, DICT_WORDNET
from pyromod import listen
from pyrogram import Client,filters, errors
from pyrogram.types import Message, InlineKeyboardButton,ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineQueryResultArticle, InputTextMessageContent, ForceReply, ReplyKeyboardRemove, ChatPermissions
from module.google_trans_new import google_translator  
from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL, utils
import lyricsgenius as lg

#LINK https://www.youtube.com/watch?v=qeBjVJkOAGc oracle

#QQ before we start
nltk.download('omw-1.4')#for repl
ytmusic = YTMusic()
telegraph = Telegraph()
telegraph.create_account(short_name='billy')
imgur_client = Imgur({'client_id': 'cf8cccd3042fc58d1f4'})
translator = google_translator(url_suffix="tw") 
memelist = [[row['name']] for row in csv.DictReader(open('memes.csv', 'r', encoding='utf-8'), delimiter='|',fieldnames=['name','type','action'])]
genius = lg.Genius("zdhRYLihRzp3sUoJRFBcEOuMp_Z3eHTIGDbDzbMPqs_PmyPOSMGgYm2YxhpYRjte", skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
# app = Client("BillyKaiChengBot",api_id="17817209",api_hash=os.environ['API'],bot_token=os.environ['TOKEN'])
app = Client("billybetabot",api_id="17817209",api_hash=os.environ['API'],bot_token='5456415338:AAGyHTNPA2Bi1CHV0ERseo13XVU_WYP5SiY')

try:
    with app:
        app.send_message(-1001518766606, "#login\ndevice: [server](https://replit.com/@lmjaedentai/billy-telegram#main.py)", disable_web_page_preview=True,disable_notification=True,reply_markup=ReplyKeyboardRemove())
        print('==========login==========')
        track = app.send_message(-1001518766606, f"#online {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} for **0**", disable_web_page_preview=True,disable_notification=True)
        #app.send_message(-1001733031563, f"**Billy Dictionary 📘**\n\nYou can search any definition for English word here. Simple and Fast. We support translation to Chinese in high accuracy. Just send me a word here now.\n\n[source](https://lmjaedentai.github.io/billy-telegram/) • [about](https://telegra.ph/Billy-KaiCheng-09-04) • [feedback](https://github.com/lmjaedentai/billy-telegram/issues/new/choose)", disable_web_page_preview=True,disable_notification=True)
except errors.exceptions.not_acceptable_406.AuthKeyDuplicated:
    os.remove("BillyKaiChengBot.session")
    sys.exit('[shutdown] session file error')


def error_handling(func):
    async def err_inner(app,message: Message,**kwargs): #kwargs mean any other args avai
        try:
            if func.__name__ != 'on_message':
                # await app.send_message(-1001518766606,'👤 /'+func.__name__)
                pass
            await func(app,message,**kwargs)
        except Exception as error:
            fullerror = "".join(traceback.TracebackException.from_exception(error).format())
            if len(fullerror) > 4094:
                printerror = await app.send_message(-1001518766606,f'❌ **{error}**\n\n{pbp.paste("i70OGnD-bRkSea_HhN_pILGRcWNQ80hb",fullerror,error, format="python")}\n#error', disable_web_page_preview=False)
            else:
                printerror = await app.send_message(-1001518766606,f'❌ **{error}**\n```\n{fullerror}\n```#error', disable_web_page_preview=True)
            #error mseg for user
            
            if isinstance(error, errors.RPCError): #telegram own error
                await app.send_photo(message.chat.id,'https://http.cat/500',f"[Telegram API error]({printerror.link})   /help",reply_markup=ReplyKeyboardRemove())
            elif isinstance(error,asyncio.exceptions.TimeoutError):
                await app.send_photo(message.chat.id,'https://http.cat/204',f"[No response]({printerror.link})   /help",reply_markup=ReplyKeyboardRemove())
            elif isinstance(error,requests.exceptions.JSONDecodeError) or isinstance(error,requests.exceptions.Timeout) or isinstance(error,KeyError):
                await app.send_photo(message.chat.id,'https://http.cat/424',f"[fail to request]({printerror.link})   /help",reply_markup=ReplyKeyboardRemove())
            elif isinstance(error,RuntimeError):
                await app.send_photo(message.chat.id,'https://http.cat/444',reply_markup=ReplyKeyboardRemove())
            elif isinstance(error,TypeError) or isinstance(error,NameError) or isinstance(error,SyntaxError) or isinstance(error,AttributeError):
                await app.send_photo(message.chat.id,'https://http.cat/525',f"Jden makes some basic mistake in code.\n[Noob.]({printerror.link})   /help",reply_markup=ReplyKeyboardRemove())
            else:
                await app.send_photo(message.chat.id,'https://http.cat/417',f"❌ **[An unexpected error has occur]({printerror.link})** \n```\n{error}\n```\nWe are sorry for that   /help")
            traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)
    return err_inner

def tracking():
    def every(delay, task):
        global ii
        ii = 1
        next_time = time.time() + delay
        while True:
            time.sleep(max(0, next_time - time.time()))
            try:
                task()
                ii += 1
            except Exception:
                traceback.print_exc()
            next_time += (time.time() - next_time) // delay * delay + delay
            
    def foo():
        global track
        track.delete()
        track = app.send_message(-1001518766606,f"#online {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} for **{ii}**",disable_notification=True)
    
    threading.Thread(target=lambda: every(60, foo)).start()

def shau():
    emoji = ['🖕', '🖕🏻', '🖕🏼','🖕🏽','🖕🏾','🖕🏿']
    content = emoji[random.randint(0,5)]
    for i in range(59):
        content = content + emoji[random.randint(0,5)]
    return content

async def shutdown(app,message):
    if message.from_user.id in [986857222,1499315224]:
        await message.reply('shutting down...')
        await app.send_message(-1001518766606,f'😴  shut down by **{message.from_user.mention()}**')
        sys.exit(f'shut down by **[{message.from_user.mention()}]**')
    else:
        await message.reply('https://http.cat/450')

async def check_definition(search,message):
    def cndict(search):
        targetlist = ['noun','adverb','adjective','verb','preposition','conjunction','article','pronoun']#,'1.','2.','3.','4.','5.','6.','7.','8.','9.','0.','[','|| ','] ','/',')','①','③']
        replacelist = ['\n\nNoun: ','\n\nAdverb: ','\n\nAdjective: ','\n\nVerb: ','\n\nPreposition: ','\n\nConjunction: ','\n\nArticles:','\n\nPronouns:']#,'\n1.','\n2.','\n3.','\n4.','\n5.','\n6.','\n7.','\n8.','\n9.','\n10.','\n • ','\n\nExample:\n • ','\n • ','/ ',') ','\n① ','\n③ ']
        meaning = ''
        with open('dict max.csv', 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f, delimiter='*',fieldnames=['name','pronouciation','meaning']):
                if search == row['name']:
                    meaning += row['meaning']     #if the phrases got 2 meaning, += wont sacrify the first meaning
                    break                         #everythings ends here, stop searching
            if meaning != '':
                for i in range(len(targetlist)):  #format definition
                    meaning = meaning.replace(targetlist[i],replacelist[i])
                for n in range(43,0,-1):
                    if f'{n}. ' in meaning:
                        meaning = meaning.replace(f'{n}. ',f'\n{n}.')
                meaning = meaning.replace(f'.',f'. ')
                return meaning
            else:
                return False
    
    async def endict(search):
        try:
            rawresult = MultiDictionary().meaning('en',search, dictionary=DICT_WORDNET)
        except IndexError: #no result
            pass
        except KeyError:
            await endict(search)
        else:
            i = 0
            result = ''
            for types in ['Noun','Verb','Adjective','Adverb']: #format definition
                if types in rawresult:
                    result+=f'\n{types}\n'
                    for meanings in rawresult[types]:
                        i+=1
                        result += f'{i}. {meanings}\n'
            await app.send_message(message.chat.id,f'📘 **[{search}](https://www.oxfordlearnersdictionaries.com/definition/english/{search.replace(" ","%20")})** \n{result}‎ ')

    typing = await app.send_message(message.chat.id,'searching...')
    await endict(search)
    zh = cndict(search)
    if zh == False or zh == '': #no result
        try:
            searchpure = lemmatize(search)
            zh = cndict(searchpure) #try base form / lemma word
        except ValueError:      #word_form module: no word in this world
            return await app.send_photo(message.chat.id,'https://http.cat/404',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f'https://www.google.com/search?q=define%20{search}')]]))
        else:
            if zh == False:     #dict.pro do not hav
                zh = f"\n\n{translator.translate(search,lang_src='en',lang_tgt='zh-tw')}  `(google translate)`"
                if zh.lower().strip() == search.strip() or zh=='':  #google trans do not hav
                    return await message.reply(f'https://http.cat/404   /help',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f'https://www.google.com/search?q=define%20{search}')]]))
        finally:
            await typing.delete()
    await app.send_message(message.chat.id,f'👲🏻**中文注释**{zh}',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙏 Credits",url=f'https://github.com/mahavivo/english-wordlists')]]))
    await typing.delete()

@app.on_message(filters.chat(-1001733031563))
@error_handling
async def on_message(client, message): #billy dict
    me = await app.get_me()
    search = message.text
    if search is None: #non text
        return await message.delete()
    elif "/" in search or " " in search or search.isalpha() == False:
        if message.from_user.id != me.id:
            return await message.delete()
    else:
        search = search.lower().strip()
        await check_definition(search,message)
    
#QQ main cmd
@app.on_message(filters.command("shau"))
@error_handling
async def sendshau(client, message):
    instructiion = await message.reply("GO",reply_markup=ReplyKeyboardMarkup([[shau(),shau()],[shau(),shau()]]))
    await asyncio.sleep(2)
    await instructiion.delete()
    await asyncio.sleep(20)
    remove = await message.reply("times up",reply_markup=ReplyKeyboardRemove())
    await remove.delete()

@app.on_message(filters.command(["dict","d","dictionary","q"]))
@error_handling
async def dictionary(client, message):
    #asking for query
    if message.text.lower().strip() in ["/dict","/d","/dictionary","/q"] or message.text.strip().__contains__('@BillyKaiChengBot'): #NOTE input == ONLY command
        query = await app.ask(message.chat.id, "🔎 Enter a word to define",reply_to_message_id=message.id,filters=filters.user(message.from_user.id) ,reply_markup = ForceReply(placeholder="exp: Daydreamer",selective=True),timeout=30)
        search = query.text.lower().strip()
    else: #args is given together with cmd
        search = message.text.replace(f'/{message.command[0]} ','').lower().strip()
    await check_definition(search,message)

@app.on_message(filters.command(["kamus","k"]))
@error_handling
async def kamus(client, message):
    #asking for query
    if message.text.lower().strip() in ["/kamus","/k"] or message.text.strip().__contains__('@BillyKaiChengBot'): #input == ONLY command
        query = await app.ask(message.chat.id, "🔎 Masukkan perkataan yang anda ingin cari",reply_to_message_id=message.id,filters=filters.user(message.from_user.id),reply_markup = ForceReply(selective=True,placeholder="contoh: Almari"))
        search = query.text.lower().strip()
    else: #args is given together with cmd
        search = message.text.replace(f'/{message.command[0]} ','').lower().strip()
    typing = await app.send_message(message.chat.id,'searching...')

    zh = translator.translate(search,lang_tgt='zh-tw',lang_src='ms') 
    if zh.lower().strip() == search or zh=='': 
        await app.send_message(message.chat.id,f'https://http.cat/404   /help',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Cari Google.",url=f'https://www.google.com/search?q={search.replace(" ","%20")}')]]))
    else: 
        # await app.send_message(message.chat.id,f'📕 **{search}** \n\n👲 {zh}\n\n**➡️ [lihat selanjutnya](https://www.ekamus.info/index.php/term/%E9%A9%AC%E6%9D%A5%E6%96%87-%E5%8D%8E%E6%96%87%E5%AD%97%E5%85%B8,{search.replace(" ","%20").lower()}.xhtml)**')#, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📕 Kamus Dewan",url=f'https://prpm.dbp.gov.my/cari1?keyword={query.text.replace(" ","%20")}'),InlineKeyboardButton("🔎 ekamus (bc)",url=f'https://www.ekamus.info/index.php/?a=srch&d=1&q={query.text.replace(" ","%20")}')]]))
        await app.send_message(message.chat.id,f'📕 **{search}** \n\n👲 {zh}\n\n**➡️ [lihat selanjutnya](https://www.ekamus.info/index.php/?a=srch&d=1&q={search.replace(" ","%20").lower()})**')
    await typing.delete()

@app.on_message(filters.command(["lyrics","l"]))
@error_handling
async def findlyrics(client, message):
    #asking for query
    if message.text.lower().strip() in ["/lyrics","/l"] or message.text.strip().__contains__('@BillyKaiChengBot'): #input == ONLY command
        query = await app.ask(message.chat.id, "🎸 Tell me the **song title** __follow by the name of artist (optional)__",reply_to_message_id=message.id,filters=filters.user(message.from_user.id),reply_markup = ForceReply(selective=True,placeholder="Perfect Ed Sheeran"))
        search = query.text.lower().strip()
    else: #args is given together with cmd
        search = message.text.replace(f'/{message.command[0]} ','').lower().strip()
    typing = await app.send_message(message.chat.id,'searching...')

    async def searchlyrics(search):
        try:
            # lyrics = genius.search_song(search, get_full_info=True)
            searchresult = ytmusic.search(query=search,filter='songs',limit=1)
            rawsong = ytmusic.get_watch_playlist(searchresult[0]["videoId"])
            l = ytmusic.get_lyrics(browseId =rawsong["lyrics"])
        except (requests.exceptions.ConnectionError):
            print('[lyrics err]')
            await searchlyrics(search)
        except:
            await app.send_message(message.chat.id,f"☹️ No search result\n\n **or**\n\n**😀 [Try Google instant search](https://www.google.com/search?q={search.replace(' ','%20')}%20lyrics)**")#,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f"https://www.google.com/search?q={query.text.replace(' ','%20')}%20lyrics")]]))
        else:
            if l['lyrics'] is None:
                return await app.send_message(message.chat.id,f"☹️ No search result\n\n **or**\n\n**😀 [Try Google](https://www.google.com/search?q={search.replace(' ','%20')}%20lyrics)**")#,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f"https://www.google.com/search?q={query.text.replace(' ','%20')}%20lyrics")]]))
            response = telegraph.create_page(search, author_name=searchresult[0]['artists'][0]['name'], author_url=f"https://music.youtube.com/channel/{searchresult[0]['artists'][0]['id']}", html_content=l['lyrics'].replace("\n", "<br>"))
            # response = telegraph.create_page(search, html_content='🎸'+lyrics.lyrics.replace("\n", "<br>").replace("Lyrics", "<br>").replace("You might also like", "<br>").replace("Embed", "<br>") , author_name=lyrics.primary_artist.name, author_url=lyrics.primary_artist.url.replace(' ','%20'))
            await app.send_message(message.chat.id,response['url'],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎧 listen",url=f"https://www.youtube.com/watch?v={searchresult[0]['videoId']}")],[InlineKeyboardButton("not this one ☹️",url=f"https://www.google.com/search?q={search.replace(' ','%20')}%20lyrics")]]))
        await typing.delete()
    
    await searchlyrics(search)


@app.on_message(filters.command(["youtube","y"])) #https://www.youtube.com/watch?v=wiHYx9NX4DM
@error_handling
async def downloadyt(client, message):
    async def askformat():
        global choice
        choice = await app.ask(message.chat.id,'Choose download format',reply_to_message_id=message.id,filters=filters.user(message.from_user.id),reply_markup=ReplyKeyboardMarkup([['mp3','mp4']],resize_keyboard=True, one_time_keyboard=True)) 
        if choice.text not in ['mp3','mp4']:
            await askformat()

    vidopt = {'format': 'best','outtmpl': 'vid.%(ext)s','restrictfilenames': True,'noplaylist': True,'nocheckcertificate': True,'ignoreerrors': False,'logtostderr': False,'default_search': 'auto','source_address': '0.0.0.0'} #LINK https://github.com/yt-dlp/yt-dlp#output-template
    audioopt = {'format': 'bestaudio','outtmpl': '%(title)s.mp3','noplaylist': True,'nocheckcertificate': True,'ignoreerrors': False,'logtostderr': False,'default_search': 'auto','source_address': '0.0.0.0'}
    query = await app.ask(message.chat.id, "📽  Enter Youtube url /video name",reply_to_message_id=message.id,filters=filters.user(message.from_user.id),reply_markup = ForceReply(selective=True,placeholder="paste link here"))
    await askformat()

    def search(arg):
        global status
        if choice.text == 'mp4': 
            opt = vidopt
            download = False
        else:
            opt = audioopt
            download = True
        with YoutubeDL(opt) as ydl:
            try:
                requests.get(arg) 
            except:
                return ydl.extract_info(f"ytsearch:{arg}", download=download)['entries'][0:1][0]
            else:
                return ydl.extract_info(arg, download=download)

    result = search(query.text)
    if choice.text == 'mp4':
        print('[fulltitle]  ',result['fulltitle'])
        await app.send_message(message.chat.id,f"**{result['fulltitle']}** \n\n⬇️  [Download link]({result['url']})  •  [more info](https://telegra.ph/Youtube-in-Billy-KaiCheng-12-09)",disable_web_page_preview=False,reply_markup=ReplyKeyboardRemove())
    else:
        await query.reply_document(f"./{result['fulltitle']}.mp3",force_document=False,reply_markup=ReplyKeyboardRemove())
        os.remove(f"./{result['fulltitle']}.mp3")

#QQ sub cmd
@app.on_message(filters.command(["covid","c"]))
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

@app.on_message(filters.command(["wiki","wk"]))
@error_handling
async def wiki(client, message):
    search = await app.ask(message.chat.id, "🔎 Enter name of article to search ",reply_to_message_id=message.id,filters=filters.user(message.from_user.id),reply_markup = ForceReply(selective=True,placeholder="exp: Tiananmen square"))
    try:
        result = MediaWiki().page(search.text)
    except mediawiki.DisambiguationError as suggestion:
        await app.send_photo(message.chat.id,"https://http.cat/300")
        await search.reply(f'**🤔 Please specify your search query** \n{suggestion} \n\n**Your search query matched mutliple pages.**\n\n/wiki')
    except mediawiki.PageError:
        await search.reply(f'https://http.cat/404   /help',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Google",url=f"https://www.google.com/search?q={search.text.replace(' ','%20')}")]]))
    else:
        await app.send_message(message.chat.id,f"📖 **{result.title}**\n\n{result.url.replace(' ','%20')}\n‎")

@app.on_message(filters.command(["translate","t","trans"]))
@error_handling
async def translate(client, message):
    langcode = [['🇬🇧 English'],['🇲🇾 Bahasa Melayu'],['🇹🇼 正体中文'],['instruction ℹ️'],['am'],['ar'],['eu'],['bn'],['bg'],['ca'],['cs'],['da'],['nl'],['et'],['fil'],['fi'],['fr'],['de'],['el'],['gu'],['iw'],['hi'],['hu'],['is'],['id'],['it'],['ja'],['kn'],['ko'],['lv'],['lt'],['no'],['pl'],['pt-PT'],['ro'],['ru'],['sr'],['sk'],['sl'],['es'],['sw'],['sv'],['ta'],['th'],['tr'],['uk'],['vi']]
    query = await app.ask(message.chat.id, f"💬 Enter the word to **translate**",reply_to_message_id=message.id,filters=filters.user(message.from_user.id),reply_markup = ForceReply(selective=True,placeholder="How are you?"))
    async def asklang():
        global code, choice
        choice = await app.ask(message.chat.id,'🌏 Select the language',reply_to_message_id=message.id,filters=filters.user(message.from_user.id),reply_markup=ReplyKeyboardMarkup(langcode,resize_keyboard=True, one_time_keyboard=True))
        if choice.text == '🇬🇧 English':
            return 'en'
        elif choice.text == '🇲🇾 Bahasa Melayu':
            return 'ms'
        elif choice.text == '🇹🇼 正体中文':
            return 'zh-tw'
        elif choice.text == 'instruction ℹ️':
            return None 
        elif any(choice.text in x for x in langcode):
            return choice.text
        else:
            await asklang()
    code = await asklang()
    if code is None:
        return await app.send_message(message.chat.id,f'click to see [instruction](https://telegra.ph/Language-code-in-translate-12-09)',reply_markup=ReplyKeyboardRemove())
    await choice.reply(f'{query.text}\n⇓\n{translator.translate(query.text,lang_tgt=code)}\n\n',reply_markup=ReplyKeyboardRemove())

@app.on_message(filters.command(["peribahasa","p"]))
@error_handling
async def peribahasa(client, message):
    query = await app.ask(message.chat.id, "🔎 Masukkan peribahasa yg anda ingin cari",reply_to_message_id=message.id,filters=filters.user(message.from_user.id),reply_markup = ForceReply(selective=True,placeholder="by maksudperibahasa.com"))
    await app.send_message(message.chat.id,f"📕 **{query.text}** \n\nhttps://maksudperibahasa.com/?s={query.text.replace(' ','-')}/")
    await app.send_message(message.chat.id,f"👲 **中文注释** \n\nhttps://www.ekamus.info/index.php/?a=srch&q={query.text.replace(' ','+')}")

@app.on_message(filters.command(["mute"]))
@error_handling
async def muteppl(client, message):
    me = await app.get_me()
    if not message.reply_to_message:
        return await app.send_message(message.chat.id,f'https://http.cat/412')
    if message.reply_to_message.from_user.id == me.id:
        return await app.send_message(message.chat.id,f"[Billy cant mute itself](https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/Trollface_non-free.png/220px-Trollface_non-free.png)")
    if message.reply_to_message.from_user.id == message.from_user.id:
        return await app.send_message(message.chat.id,f"Are you trying to /mute yourself")
    time = message.text.replace(f'/{message.command[0]} ','').lower().strip()

    # rawtime = await app.ask(message.chat.id, f"🕒 Pick a Duration",reply_to_message_id=message.id,filters=filters.user(message.from_user.id),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("How? 🤔",callback_data="data")]]))
    # time = rawtime.text
    time_convert = {"s":1, "m":60, "h":3600,"d":86400}
    
    try:
        seconds = int(time[:-1]) * time_convert[time[-1]]
    except (ValueError, KeyError,TypeError):
        return await app.send_message(message.chat.id,f"https://http.cat/418")#,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("instructions",callback_data="data")]]))
    if seconds <= 30 or seconds >= 31622400:
        return await app.send_message(message.chat.id,f"https://http.cat/416")
    
    try:
        await app.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, ChatPermissions(),datetime.datetime.now() + datetime.timedelta(seconds=seconds))
    except errors.ChatAdminRequired: #bot not admin
        await app.send_message(message.chat.id,f'https://http.cat/401')
    except errors.UserAdminInvalid: #target is admin
        await app.send_message(message.chat.id,f'https://http.cat/405')
    else:
        await app.send_message(message.chat.id,f'✅  **{message.reply_to_message.from_user.mention()}** is muted by {message.from_user.mention()} for **{time}**')

@app.on_message(filters.command(["unmute"]))
@error_handling
async def unmuteppl(client, message):
    try:
        await app.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, ChatPermissions(can_send_messages = True, can_send_media_messages = True, can_send_other_messages = True, can_send_polls = True, can_add_web_page_previews = True))
    except errors.ChatAdminRequired: #bot not admin
        await app.send_message(message.chat.id,f'https://http.cat/401')
    except errors.UserAdminInvalid: #target is admin
        await app.send_message(message.chat.id,f'https://http.cat/405')
    else:
        await app.send_message(message.chat.id,f'✅  **{message.reply_to_message.from_user.mention()}** is unmuted by {message.from_user.mention()} for **{time}**')

@app.on_message(filters.command(["weather","temp","w"]))
@error_handling
async def sendweather(client, message):
    choice = await app.ask(message.chat.id,'🌏 Choose your region',filters=filters.user(message.from_user.id),reply_markup=ReplyKeyboardMarkup([['Malacca'],['Other']],resize_keyboard=True, one_time_keyboard=True))
    if choice.text == 'Malacca':
        city = 'Malacca'
    else:
        query = await app.ask(message.chat.id,'🌏 Enter your region',reply_to_message_id=message.id,filters=filters.user(message.from_user.id),reply_markup = ForceReply(selective=True,placeholder="by MSN weather"))
        city = query.text
    typing =  await app.send_message(message.chat.id,'searching',reply_markup=ReplyKeyboardRemove())
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?appid=c19ed679efd0dd0f4afdaa12325d2f17&q={city.replace(' ','%20')}&units=metric")
        raw = response.json()
        response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution?appid=c19ed679efd0dd0f4afdaa12325d2f17&lat={raw['coord']['lat']}&lon={raw['coord']['lon']}")
        raw2 = response.json()
    except IndexError:
        return await message.reply(f'https://http.cat/404   /help',reply_markup=ReplyKeyboardRemove())
    else:
        weathercode = {"01d":"☀️","02d":"⛅","03d":"☁️☁️","04d":"☁️","09d":"🌦️","10d":"🌧️","11d":"⛈️","13d":"❄️","50d":"🌫️","01n":"☀️","02n":"⛅","03n":"☁️☁️","04n":"☁️","09n":"🌦️","10n":"🌧️","11n":"⛈️","13n":"❄️","50n":"🌫️"}
        aircode={1:"Good",2:"Fair",3:"Moderate",4:"Poor",5:"Very poor"}
        await typing.delete()
        await app.send_message(message.chat.id,f"**[{raw['name']}](https://www.google.com/search?q={city.replace(' ','%20')}%20weather)**\n{weathercode[raw['weather'][0]['icon']]} {raw['weather'][0]['description']}\n\n🌡 temp: **{raw['main']['temp']}°C**\n🥵 highest: **{raw['main']['temp_max']}°C**\n🥶 lowest: **{raw['main']['temp_min']}°C**\n\n😑 feels like: **{raw['main']['feels_like']}°C**\n💧 humidity: **{raw['main']['humidity']}**\n🍃 wind: **{raw['wind']['speed']}km/h  {raw['wind']['deg']}°**\n\n☁️ cloudiness: **{raw['clouds']['all']}%**\n👀 visibility: **{raw['visibility']}m**\n🌬️ air quality: **{aircode[raw2['list'][0]['main']['aqi']]}**",disable_web_page_preview=True,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("by OpenWeatherMap 🌞",url='https://openweathermap.org/api')]]))



#QQ under construction
@app.on_message(filters.command("remind"))
@error_handling
async def remind(client, message):
    reminder = await app.ask(message.chat.id, f"🔔 What should I remind you?",reply_to_message_id=message.id,filters=filters.user(message.from_user.id),reply_markup = ForceReply(selective=True,placeholder="this feature is unstable"))
    rawtime = await app.ask(message.chat.id, f"🕒 Pick a time to remind",reply_to_message_id=message.id,filters=filters.user(message.from_user.id),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("How? 🤔",callback_data="data")]]))
    time = rawtime.text
    time_convert = {"s":1, "m":60, "h":3600,"d":86400}
    try:
        seconds = int(time[:-1]) * time_convert[time[-1]]
    except (ValueError, KeyError,TypeError):
        return await app.send_message(message.chat.id,f"https://http.cat/304",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("instructions",callback_data="data")]]))
    rawdate = datetime.datetime.now() + datetime.timedelta(seconds = seconds) # UTC8 + delaytime
    if seconds <= 0:
        await app.send_message(message.chat.id,f'https://http.cat/411')
    elif seconds > 7776000:
        await app.send_message(message.chat.id,f'https://http.cat/414')
    else: 
        await app.send_message(message.chat.id,f"🔔 Alright, I will remind you **{reminder.text}** in **{time}** at **{datetime.datetime.fromtimestamp(round(rawdate.timestamp()))}**")
        await asyncio.sleep(seconds)
    await reminder.reply(f'🔔 Reminder for [{reminder.text}]({reminder.link})\n🕒 set **{time}** ago\n\n`dont forget lol`',disable_web_page_preview=True)

@app.on_callback_query()
async def reminder_instructions(client, callback_query):
    await callback_query.answer(f"You can enter any time value you like\nby following format below.\n\nFor example:\n\n10 second  : 10s\n10 minutes : 10m\n10 hours     : 10h\n10 days       : 10d\n\nThis beta feature currently is unstable.",show_alert=True)


@app.on_message(filters.command(["other","more"]))
@error_handling
async def other_cmdlist(client, message):
    i = await message.reply('Select the feature you want',reply_markup=ReplyKeyboardMarkup([['/help'],['/peribahasa'],['/wiki'],['/weather'],['/covid']],resize_keyboard=True, one_time_keyboard=True))
    await asyncio.sleep(2)
    await i.delete()
    await asyncio.sleep(20)
    remove = await message.reply("times up",reply_markup=ReplyKeyboardRemove())
    await remove.delete()

@app.on_message(filters.command(["start","help",'test']))
@error_handling
async def helpmenu(client, message):
    await app.send_photo(message.chat.id,'https://http.cat/100')
    await app.send_message(message.chat.id,'2022 coded in Python\n[source](https://lmjaedentai.github.io/billy-telegram/) • [privacy](https://telegra.ph/Privacy-Policy-02-19-26) • /feedback\n\n**Main Command**\n• dont touch /shau\n• cn to en /dictionary\n• download /youtube\n• search song /lyrics\n\n**/more Subcommand**\n• google /translate\n• malay /kamus\n• real time statistics /covid\n• search for /wiki\n• cari /peribahasa \n• find /memes\n• check /weather'
    ,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("about us 🍃",url='https://telegra.ph/Billy-KaiCheng-09-04')]]), disable_web_page_preview=True)

@app.on_message(filters.command(["feedback"]))
@error_handling
async def getfeedback(client, message):
    respond = await app.ask(message.chat.id,'Comment here...\n\n**It can be a**\n1. idea suggestion\n2. letter to developer\n3. enhancement\n4. feature request\n5. bug report\n\n[more](https://github.com/lmjaedentai/billy-telegram/issues/new/choose)', disable_web_page_preview=True,filters=filters.user(message.from_user.id),timeout=2)
    await app.send_message(message.chat.id,f'Thanks for your feeback 😁')
    feedback = await app.send_message(-1001518766606,f'**User #feedback from {message.from_user.mention()}\n\n**{respond.text}')
    await feedback.pin()


#QQ other cmd
@app.on_message(filters.text)
@error_handling
async def on_message(client, message):
    if message.text == ".err":
        this_is_an_error() #type: ignore
    elif message.text == ".id":
        await message.reply(message.chat.id)
    elif message.text == ".shutdown":
        await shutdown(client,message)


from online import keep_alive 
tracking()
keep_alive()
app.run()