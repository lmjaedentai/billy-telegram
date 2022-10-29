print('==========start==========')
import os
import sys
sys.path.append('./module') 
import csv
import time
import nltk
import pytz
import random
import urllib
import asyncio
import datetime
import threading
import traceback
import mediawiki
import lyricsgenius as lg
from telegraph import Telegraph
from mediawiki import MediaWiki
from word_forms.lemmatizer import lemmatize
from PyMultiDictionary import MultiDictionary, DICT_WORDNET
from pyromod import listen
from pyrogram import Client,filters, errors
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message, InlineKeyboardButton, KeyboardButton,ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineQuery, InlineQueryResultArticle,InlineQueryResultPhoto, InputTextMessageContent, ForceReply, ReplyKeyboardRemove, ChatPermissions
from module.pytube import YouTube, exceptions
from module.google_trans_new import google_translator  
from ytmusicapi import YTMusic


#LINK https://www.youtube.com/watch?v=qeBjVJkOAGc oracle

#QQ before we start
telegraph = Telegraph()
ytmusic = YTMusic()
telegraph.create_account(short_name='billy')
translator = google_translator(url_suffix="my") 
# app = Client("BillyKaiChengBot",api_id="17817209",api_hash=os.environ['API'],bot_token=os.environ['TOKEN'])
app = Client("billybetabot",api_id="17817209",api_hash=os.environ['API'],bot_token='5456415338:AAGyHTNPA2Bi1CHV0ERseo13XVU_WYP5SiY')
# nltk.download('omw-1.4')#for repl

with app:
    # app.send_message(-1001518766606, "#login\ndevice: vscode")
    app.send_message(-1001518766606, "#login\ndevice: [repl.it](https://replit.com/@lmjaedentai/billy-telegram#main.py)", disable_web_page_preview=True,disable_notification=True)
    print('==========login==========')
    track = app.send_message(-1001518766606, f"#online {pytz.timezone('Asia/Kuala_Lumpur').localize(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} for **0**", disable_web_page_preview=True,disable_notification=True)


def error_handling(func):
    async def inner(app,message: Message,**kwargs): #kwargs mean any other args avai
        try:
            if func.__name__ != 'on_message':
                # await app.send_message(-1001518766606,'👤 /'+func.__name__)
                pass
            await func(app,message,**kwargs)
        except Exception as error:
            fullerror = "".join(traceback.TracebackException.from_exception(error).format())
            printerror = await app.send_message(-1001518766606,f'❌ **{error}**\n```\n{fullerror}\n```#error', disable_web_page_preview=True)
            if isinstance(error, errors.RPCError): #telegram own error
                await app.send_message(message.chat.id,f"⁉️ **[Telegram API error]({printerror.link})**\n\nWe are sorry for that   /help", disable_web_page_preview=True)
            else:
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
        await app.send_message(-1001518766606,f'😴  shut down by **{message.from_user.mention()}**')
        sys.exit(f'shut down by **[{message.from_user.mention()}]**')
    else:
        await message.reply('❌ No admin rights')


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
    targetlist = ['n.','adv.','adj.','v.','prep.','int.','conj.','art.','prop.','aux.','1.','2.','3.','4.','5.','6.','7.','8.','9.','10.','[','|| ','] ','/',')']
    replacelist = ['\n\nNoun: ','\n\nAdverb: ','\n\nAdjective: ','\n\nVerb: ','\n\nPreposition: ','\n\nInterjection: ','\n\nConjunction: ','\n\nArticles:','\n\nPronouns:','\n\nAuxiliary:','\n1.','\n2.','\n3.','\n4.','\n5.','\n6.','\n7.','\n8.','\n9.','\n10.','\n • ','\n\nExample:\n • ','\n • ','/ ',') ']
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
    
    #asking for query
    if message.text.lower().strip() in ["/dict","/d","/dictionary"] or message.text.strip().__contains__('@BillyKaiChengBot'): #input == ONLY command
        query = await app.ask(message.chat.id, "🔎 Enter a word to define",filters=filters.user(message.from_user.id) ,reply_markup = ForceReply(placeholder="exp: Daydreamer"),)
        search = query.text.lower().strip()
    else: #args is given together with cmd
        search = message.text.replace(f'/{message.command[0]} ','').lower().strip()
    typing = await app.send_message(message.chat.id,'searching...')

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
        finally:
            await typing.delete()
    await app.send_message(message.chat.id,f'👲🏻**中文注释**\n{zh}',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙏 Credits",url=f'https://github.com/mahavivo/english-wordlists')]]))
    await typing.delete()

@app.on_message(filters.command(["kamus","k"]))
@error_handling
async def kamus(client, message):
    #asking for query
    if message.text.lower().strip() in ["/kamus","/k"] or message.text.strip().__contains__('@BillyKaiChengBot'): #input == ONLY command
        query = await app.ask(message.chat.id, "🔎 Masukkan perkataan yang anda ingin cari",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder="contoh: Almari"))
        search = query.text.lower().strip()
    else: #args is given together with cmd
        search = message.text.replace(f'/{message.command[0]} ','').lower().strip()
    typing = await app.send_message(message.chat.id,'searching...')

    zh = translator.translate(search,lang_tgt='zh') 
    if zh.lower().strip() == search or zh=='': 
        await app.send_message(message.chat.id,f'❌ **Carian kata tiada di dalam kamus terkini**   /help',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Cari Google.",url=f'https://www.google.com/search?q={search.replace(" ","%20")}')]]))
    else: 
        # await app.send_message(message.chat.id,f'📕 **{search}** \n\n👲 {zh}\n\n**➡️ [lihat selanjutnya](https://www.ekamus.info/index.php/term/%E9%A9%AC%E6%9D%A5%E6%96%87-%E5%8D%8E%E6%96%87%E5%AD%97%E5%85%B8,{search.replace(" ","%20").lower()}.xhtml)**')#, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📕 Kamus Dewan",url=f'https://prpm.dbp.gov.my/cari1?keyword={query.text.replace(" ","%20")}'),InlineKeyboardButton("🔎 ekamus (bc)",url=f'https://www.ekamus.info/index.php/?a=srch&d=1&q={query.text.replace(" ","%20")}')]]))
        await app.send_message(message.chat.id,f'📕 **{search}** \n\n👲 {zh}\n\n**➡️ [lihat selanjutnya](https://www.ekamus.info/index.php/?a=srch&d=1&q={search.replace(" ","%20").lower()})**')
    await typing.delete()

@app.on_message(filters.command(["lyrics","l"]))
@error_handling
async def findlyrics(client, message):
    #asking for query
    if message.text.lower().strip() in ["/lyrics","/l"] or message.text.strip().__contains__('@BillyKaiChengBot'): #input == ONLY command
        query = await app.ask(message.chat.id, "🎸 Tell me the **song title** __follow by the name of artist (optional)__",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder="Perfect Ed Sheeran"))
        search = query.text.lower().strip()
    else: #args is given together with cmd
        search = message.text.replace(f'/{message.command[0]} ','').lower().strip()
    typing = await app.send_message(message.chat.id,'searching...')

    try:
        # lyrics = genius.search_song(search, get_full_info=True)
        searchresult = ytmusic.search(query=search,filter='songs',limit=1)
        rawsong = ytmusic.get_watch_playlist(searchresult[0]["videoId"])
        l = ytmusic.get_lyrics(browseId =rawsong["lyrics"])
    except:
        await app.send_message(message.chat.id,f"☹️ No search result\n\n **or**\n\n**😀 [Try Google instant search](https://www.google.com/search?q={search.replace(' ','%20')}%20lyrics)**")#,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f"https://www.google.com/search?q={query.text.replace(' ','%20')}%20lyrics")]]))
    else:
        if l['lyrics'] is None:
            return await app.send_message(message.chat.id,f"☹️ No search result\n\n **or**\n\n**😀 [Try Google](https://www.google.com/search?q={search.replace(' ','%20')}%20lyrics)**")#,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Try Google.",url=f"https://www.google.com/search?q={query.text.replace(' ','%20')}%20lyrics")]]))
        response = telegraph.create_page(search, author_name=searchresult[0]['artists'][0]['name'], author_url=f"https://music.youtube.com/channel/{searchresult[0]['artists'][0]['id']}", html_content=l['lyrics'].replace("\n", "<br>"))
        # response = telegraph.create_page(search, html_content='🎸'+lyrics.lyrics.replace("\n", "<br>").replace("Lyrics", "<br>").replace("You might also like", "<br>").replace("Embed", "<br>") , author_name=lyrics.primary_artist.name, author_url=lyrics.primary_artist.url.replace(' ','%20'))
        await app.send_message(message.chat.id,response['url'],reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎧 listen",url=f"https://www.youtube.com/watch?v={searchresult[0]['videoId']}")],[InlineKeyboardButton("not this one ☹️",url=f"https://www.google.com/search?q={search.replace(' ','%20')}%20lyrics")]]))
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
    i = await message.reply('Select the feature you want',reply_markup=ReplyKeyboardMarkup([['/help'],['/peribahasa'],['/wiki'],['/translate'],['/covid']],resize_keyboard=True))
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
    #asking for query
    search = await app.ask(message.chat.id, "🔎 Enter name of article to search ",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder="exp: Tiananmen square"))
    try:
        result = MediaWiki().page(search.text)
    except mediawiki.DisambiguationError as suggestion:
        await search.reply(f'**🤔 Please specify your search query** \n{suggestion} \n\n**Your search query matched mutliple pages.**\n\n/wiki')
    except mediawiki.PageError:
        await search.reply(f'❌ **No search result** Try Google.',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎 Google",url=f"https://www.google.com/search?q={search.text.replace(' ','%20')}")]]))
    else:
        await app.send_message(message.chat.id,f"📖 **{result.title}**\n\n{result.url.replace(' ','%20')}\n‎")

@app.on_message(filters.command(["translate","t"]))
@error_handling
async def translate(client, message):
    query = await app.ask(message.chat.id, f"💬 Enter the word to **translate**",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder="How are you?"))
    async def asklang():
        global code
        choice = await app.ask(message.chat.id,'🌏 Select the language',filters=filters.user(message.from_user.id),reply_markup=ReplyKeyboardMarkup([['🇬🇧 English','🇲🇾 Bahasa Melayu','🇹🇼 正体中文']],resize_keyboard=True))
        if choice.text == '🇬🇧 English':
            return 'en'
        elif choice.text == '🇲🇾 Bahasa Melayu':
            return 'ms'
        elif choice.text == '🇹🇼 正体中文':
            return 'zh-tw'
        else:
            await asklang()
    code = await asklang()
    await app.send_message(message.chat.id,f'{query.text}\n⇓\n{translator.translate(query.text,lang_tgt=code)}\n\n',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📕 Dictionary",switch_inline_query_current_chat=f'{query.text}')]]))

@app.on_message(filters.command(["peribahasa","p"]))
@error_handling
async def peribahasa(client, message):
    query = await app.ask(message.chat.id, "🔎 Masukkan peribahasa yg anda ingin cari",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder="by maksudperibahasa.com"))
    await app.send_message(message.chat.id,f"📕 **{query.text}** \n\nhttps://maksudperibahasa.com/?s={query.text.replace(' ','-')}/")
    await app.send_message(message.chat.id,f"👲 **中文注释** \n\nhttps://www.ekamus.info/index.php/?a=srch&q={query.text.replace(' ','+')}")

@app.on_message(filters.command(["mute"]))
@error_handling
async def muteppl(client, message):
    me = await app.get_me()
    if not message.reply_to_message:
        return await app.send_message(message.chat.id,f'❌  Invalid input /command')
    if message.reply_to_message.from_user.id == me.id:
        return await app.send_message(message.chat.id,f"[Billy cant mute itself](https://upload.wikimedia.org/wikipedia/en/thumb/9/9a/Trollface_non-free.png/220px-Trollface_non-free.png)")
    if message.reply_to_message.from_user.id == message.from_user.id:
        return await app.send_message(message.chat.id,f"Are you trying to /mute yourself")
    time = message.text.replace(f'/{message.command[0]} ','').lower().strip()

    # rawtime = await app.ask(message.chat.id, f"🕒 Pick a Duration",filters=filters.user(message.from_user.id),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("How? 🤔",callback_data="data")]]))
    # time = rawtime.text
    time_convert = {"s":1, "m":60, "h":3600,"d":86400}
    
    try:
        seconds = int(time[:-1]) * time_convert[time[-1]]
    except (ValueError, KeyError,TypeError):
        return await app.send_message(message.chat.id,f"❌ Invalid value")#,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("instructions",callback_data="data")]]))
    if seconds <= 30 or seconds >= 31622400:
        return await app.send_message(message.chat.id,f"❌ Invalid input value")
    
    try:
        await app.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, ChatPermissions(),datetime.datetime.now() + datetime.timedelta(seconds=seconds))
    except errors.ChatAdminRequired: #bot not admin
        await app.send_message(message.chat.id,f'❌  The action requires admin privileges. Pls promote me.')
    except errors.UserAdminInvalid: #target is admin
        await app.send_message(message.chat.id,f'❌  No permission to mute admin')
    else:
        await app.send_message(message.chat.id,f'✅  **{message.reply_to_message.from_user.mention()}** is muted by {message.from_user.mention()} for **{time}**')

@app.on_message(filters.command(["memes","m"]))
@error_handling
async def sendmeme(client, message):
    memelist = [['joe biden'],['very sad'],['caution'],['facts'],['pikachu'],['gay'],['abu'],['lagi gay'],['dont touch'],['rainbow'],['cats'],['nono color'],['no color pills'],['therapist'],['go jail'],['he go jail by himself'],['very very color'],['anti color']]
    await app.send_message(message.chat.id,'Choose your favourite',reply_markup=ReplyKeyboardMarkup(memelist,resize_keyboard=True))
   
        

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
    await app.send_message(message.chat.id,'2022 coded in Python\n[source](https://github.com/lmjaedentai/billy-telegram#readme) • [about](https://telegra.ph/Billy-KaiCheng-09-04) • [feedback](https://github.com/lmjaedentai/billy-telegram/issues/new/choose)\n\n**Main Command**\n• dont touch /shau\n• cn to en /dictionary\n• download /youtube\n• search song /lyrics\n\n**/more Subcommand**\n• google /translate\n• simple math /calc\n• malay /kamus\n• real time statistics /covid\n• search for /wiki\n• cari /peribahasa \n• find /memes'
    ,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("go touch grass 🍃",switch_inline_query_current_chat='')]]), disable_web_page_preview=True)






#QQ other cmd
@app.on_message(filters.text)
@error_handling
async def on_message(client, message):
    async def runner(ask=0,url=None):
        if ask == 2:
            await app.send_message(message.chat.id,url)
            return
        if ask == 1:
            query = await app.ask(message.chat.id, "Enter the text",filters=filters.user(message.from_user.id),reply_markup = ForceReply(placeholder="yeeeet"))
            text = query.text.replace(' ','+')
            url = url.replace('qden',text)
        await app.send_photo(message.chat.id,url)
    
    async def minicmd(argument):
        switcher = {
            '.id': lambda: message.reply(message.chat.id),
            '.err': lambda: this_is_an_error(), 
            '.shutdown': lambda: shutdown(client,message),

            'joe biden': lambda: runner(1,'https://api.popcat.xyz/biden?text=qden'),
            'pikachu': lambda: runner(1,'https://api.popcat.xyz/pikachu?text=qden'),
            'very sad': lambda: runner(1,'https://api.popcat.xyz/sadcat?text=qden'),
            'caution': lambda: runner(1,'https://api.popcat.xyz/caution?text=qden'),
            'facts': lambda: runner(1,'https://api.popcat.xyz/biden?facts=qden'),
            'abu': lambda: runner(2,'https://lmjaedentai.github.io/abu/'),
            'gay': lambda: runner(2,'https://lmjaedentai.github.io/april/'),
            'lagi gay': lambda: runner(2,'https://nextcord.gay'),
            'dont touch': lambda: runner(2,shau()),
            'cats': lambda: runner(2,f"http.cat/{random.choice([100,101,102,200,201,202,203,204,206,207,300,301,302,303,304,305,307,308,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,420,421,422,423,424,425,426,429,431,444,450,451,497,498,499,500,501,502,503,504,506,507,508,509,510,511,521,522,523,525,599])}"),
            'rainbow': lambda: runner(0,'https://i.imgur.com/DuB3YyZ.png'),
            'nono color': lambda: runner(0,'https://www.aixiaola.com/wp-content/uploads/2021/10/c4d36f57bf4cc6e7d0c979398822a755.jpg'),
            'no color pills': lambda: runner(0,'https://img.youxi369.com/article/contents/2021/09/30/small_2021093041011706.jpg'),
            'therapist': lambda: runner(0,'https://truth.bahamut.com.tw/s01/202109/6658b57ae9aee50152692cbd71222066.JPG'),
            'go jail': lambda: runner(0,'https://cdn.hk01.com/di/media/images/dw/20211025/529294578378346496210749.png/Ius3SpY28ZbfQ-GPJi_kJPLI8KbpH7JhlC8qeJQvKng?v=w1920'),
            'he go jail by himself': lambda: runner(0,'https://i.imgur.com/ROnmLbi.png'),
            'very very color': lambda: runner(0,'https://img.league-funny.com/imgur/163421235519_n.jpg'),
            'anti color': lambda: runner(0,'https://pic1.zhimg.com/v2-93a878f9b7e6df2e7cf5f840ef30af38_b.jpg'),
        }
        try:
            await switcher[argument]()
        except KeyError:
            pass
    await minicmd(message.text)

@app.on_inline_query()
@error_handling
async def sticker(client, query):
    string = query.query.lower()
    defaultlist= [
        InlineQueryResultArticle(title='晨曦云',description="dont touch",thumb_url='https://i.imgur.com/ZqGgNt5.jpg', input_message_content=InputTextMessageContent(shau())),
        InlineQueryResultArticle(title='Touch Grass',description="Help", input_message_content=InputTextMessageContent("/help lol back to the origin"),thumb_url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/person-tipping-hand_light-skin-tone_1f481-1f3fb_1f3fb.png'),
        InlineQueryResultArticle(title='About us',description="Coded in python🐍 2021 @lmjaedentai ", input_message_content=InputTextMessageContent("[about](https://telegra.ph/Billy-KaiCheng-09-04)"),thumb_url='https://i.imgur.com/OMuzyF7.png'),
    ]
    searchingmode = [
        InlineQueryResultArticle(title='Search Dictionary',description="Show the definitions in English and Chinese",thumb_url='https://i.imgur.com/8yJ7rmm.png', input_message_content=InputTextMessageContent(f'/dict {string}')),
        InlineQueryResultArticle(title='Find lyrics',description="Enter your song name",thumb_url='https://t3.ftcdn.net/jpg/04/54/66/12/360_F_454661277_NtQYM8oJq2wOzY1X9Y81FlFa06DVipVD.jpg', input_message_content=InputTextMessageContent(f'/lyrics {string}')),
        InlineQueryResultArticle(title='Cari Kamus',description="Powered by Ekamus",thumb_url='https://www.ekamus.info/img/ekamus.png', input_message_content=InputTextMessageContent(f'/kamus {string}')),
    ]
    if string == "":
        await query.answer(results=defaultlist,cache_time=1,switch_pm_text=f"Choose the option or Search",switch_pm_parameter="start",)
    else:
        await query.answer(results=searchingmode ,cache_time=1,switch_pm_text=f"🔍Billy Instant Search",switch_pm_parameter="start",)



    

#QQ tracking
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
    track = app.send_message(-1001518766606,f"#online {pytz.timezone('Asia/Kuala_Lumpur').localize(datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')} for **{ii}**",disable_notification=True)
    
threading.Thread(target=lambda: every(60, foo)).start()

from online import keep_alive 
keep_alive()
app.run()

