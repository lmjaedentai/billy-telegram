print('==========start==========')
import os
import sys
import csv
import asyncio
import random
import requests
import datetime
import traceback
from imgur_python import Imgur
from pyromod import listen
from pyrogram import Client,filters, errors
from pyrogram.types import Message, InlineKeyboardButton,ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineQueryResultArticle, InputTextMessageContent, ForceReply, ReplyKeyboardRemove, ChatPermissions

mylist=[
    [['jden','jaeden'],['hal ehwal no fren','不要跟我抢printer','nat geo director','god of art','hand some','quarks are smaller than electron']],
    [['yz','cyz','chan','yanzhe','@na_ch_t'],['gay','yanzhe is the future therapist','班长~~']],
    [['jus','justin'],['banana','diploma','gay']],
    [['gay'],['gay','highest ranking in py grp']],
    [['game','bs','cr','krunker'],['不要打game']],
    [['js','jiashiu','shau','家修','晨曦云','羽球学会副主席'],['lyl','milo susu','sunat?','puasa?','senior对我笑','我文学好低分啊']],
    [['rz','abu','runze'],['肾虚','腰酸','骨头痛','kp','kpl','suami rumah']],
    [['yy'],['callista']],
    [['callista'],['yy']],
    [['jolin'],['班长~~']],
    [['上帝','simyl','syl','玉兰姐','god'],['多吃水果','喝上帝汤','意外是可以避免的','上帝爱你','wei jen他啊']],
    [['yong','lw','linwei'],['不要打game','早点睡觉','几时追到她']],
    [['maznah','bm','malay','karangan','essay'],['chan karangan?']],
    [['lol','lmao'],['lol','lmao']],
    [['bruh'],['bruh']],
    [['rasul'],['our deputy prime minister...','Guys soalan KBAt','in 1957, Tunku...']],
    [['jibai','fk','fuck','shit'],['经研究显示，骂粗话可缓解肌肉酸痛','生气别人就是惩罚自己','不要鸡动，要蛋定']],
    [['georgia','joja','gg'],['why is ur bottle wearing ur mask?','SDG','sanitize this group.. too dirty']],
    [['lyl','chemi','chemistry'],['@Jiashiuuu','NaCl','jiashiu can u understand?']],
    [['rs','chong','botak'],['cute baby','rs or rs','你听华晨宇专辑了吗','几时交女朋友？','Boy For Aunty']],
    [['find','cari','explore'],['https://assets.nickjr.com/uri/mgid:arc:imageassetref:shared.nickjr.us:0a3d8cad-0749-4c1e-a4b2-85639f610209?quality=0.7&gen=ntrn&legacyStatusCode=true',]],
    [['69','porn','onlyfans','sex','%%%'],['https://i.pinimg.com/736x/f3/d4/fb/f3d4fbd789f7fc46576bd6fa82e11eba.jpg','data:image/jpeg;base64,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','https://cdn.hk01.com/di/media/images/dw/20211025/529294578378346496210749.png/Ius3SpY28ZbfQ-GPJi_kJPLI8KbpH7JhlC8qeJQvKng?v=w1920']],
    [['error'],['yala jden noob','failure','dissapointment','u just an intern for unemployment']],
    [['sorry','sry','抱歉','对不起','maaf'],['我原谅你','烂']],
    [['malim'],['area 51','Add Math college','school of dissapointment','*庄轩*']],
]

memelist = [[row['name']] for row in csv.DictReader(open('memes.csv', 'r', encoding='utf-8'), delimiter='|',fieldnames=['name','type','action'])]

#QQ before we start
app = Client("verypigbot",api_id="17817209",api_hash=os.environ['API'],bot_token='5672506489:AAEz6KoOB2o4GS1WmVCxdmPLyyR2SBnlnJY')
imgur_client = Imgur({'client_id': 'cf8cccd3042fc58d1f4'})
try:
    with app:
        app.send_message(-1001518766606, "#login\ndevice: [server](https://replit.com/@lmjaedentai/billy-telegram#main.py)", disable_web_page_preview=True,disable_notification=True,reply_markup=ReplyKeyboardRemove())
        print('==========login==========')
        track = app.send_message(-1001518766606, f"#online {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} for **0**", disable_web_page_preview=True,disable_notification=True)
        #app.send_message(-1001733031563, f"**Billy Dictionary 📘**\n\nYou can search any definition for English word here. Simple and Fast. We support translation to Chinese in high accuracy. Just send me a word here now.\n\n[source](https://lmjaedentai.github.io/billy-telegram/) • [about](https://telegra.ph/Billy-KaiCheng-09-04) • [feedback](https://github.com/lmjaedentai/billy-telegram/issues/new/choose)", disable_web_page_preview=True,disable_notification=True)
except errors.exceptions.not_acceptable_406.AuthKeyDuplicated:
    os.remove("verypigbot.session")
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
            printerror = await app.send_message(-1001518766606,f'❌ **{error}**\n```\n{fullerror}\n```#error', disable_web_page_preview=True)
            if isinstance(error, errors.RPCError): #telegram own error
                await app.send_message(message.chat.id,f"⁉️ **[Telegram API error]({printerror.link})**\n\nWe are sorry for that   /help", disable_web_page_preview=True,reply_markup=ReplyKeyboardRemove())
            else:
                await app.send_message(message.chat.id,f"❌ **[An unexpected error has occur]({printerror.link})** \n```\n{error}\n```\nWe are sorry for that   /help", disable_web_page_preview=True)
            traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)
    return err_inner

async def shutdown(app,message):
    if message.from_user.id in [986857222,1499315224]:
        await message.reply('shutting down...')
        await app.send_message(-1001518766606,f'😴  shut down by **{message.from_user.mention()}**')
        sys.exit(f'shut down by **[{message.from_user.mention()}]**')
    else:
        await message.reply('https://http.cat/450')

def antispam():
    err = ['400','499','429']
    return f"https://http.cat/{random.choice(err)}"


#QQ other cmd



@app.on_message(filters.command(["memes","m"]))
@error_handling
async def sendmeme(client, message):  
    response = requests.get('https://api.popcat.xyz/meme')
    raw = response.json()
    await app.send_photo(message.chat.id,raw["image"],caption='Select a template',reply_markup=ReplyKeyboardMarkup(memelist,resize_keyboard=True, one_time_keyboard=True)) #send meme list
    await asyncio.sleep(30)
    remove = await message.reply("times up",reply_markup=ReplyKeyboardRemove())
    await remove.delete()

previous='electron'
@app.on_message(filters.text & filters.group)
@error_handling
async def on_message(client, message):
    global previous
    if message.text.lower()  == previous: #antispam
        return await app.send_photo(message.chat.id,antispam())
    else:
        previous = message.text.lower()

    if random.randint(0,1) != 1:
        return
    for i in mylist: #keyword
        for a in i[0]:
            if a in message.text.strip().lower():
                return await app.send_message(message.chat.id,f'{i[1][random.randint(0, len(i[1]) - 1)]}')

    async def memecmd(ask=0,url=None):
        if ask == 2: #url / text
            return await app.send_message(message.chat.id,url)
        elif ask == 1: #cuztomizable memes --> send photo
            query = await app.ask(message.chat.id, "Enter the text",reply_to_message_id=message.id,filters=filters.user(message.from_user.id),reply_markup = ForceReply(selective=True,placeholder="yeeeet"))
            text = query.text.replace(' ','%20')
            await app.send_photo(message.chat.id,url.replace('qden',text))
        elif ask == 3: #func
            return await app.send_message(message.chat.id,eval(url))
        elif ask == 4:
            target = await app.ask(message.chat.id,f'send me any message that u replying the person you want',filters=filters.user(message.from_user.id))
            if not target.reply_to_message: #target user avatar
                return await app.send_message(message.chat.id,f'https://http.cat/400')
            status = await app.send_message(message.chat.id,f'loading...')
            result = await app.download_media(target.reply_to_message.from_user.photo.big_file_id) #download user avatar
            image = imgur_client.image_upload(result, 'Untitled', 'My first image upload')          #upload to imgur
            imagelink = image['response']['data']['link']                                           #get imgur link
            if message.text == 'sayang':
                return await app.send_animation(message.chat.id,url.replace('qden',imagelink))  #process & send photo
            await app.send_photo(message.chat.id,url.replace('qden',imagelink))                 #process & send photo
            await status.delete()
        else: #0 send photo
            await app.send_photo(message.chat.id,url)

    if any(message.text in x for x in memelist): #memecmd
        for row in csv.DictReader(open('memes.csv', 'r', encoding='utf-8'), delimiter='|',fieldnames=['name','type','action']):
            if message.text == row['name']:
                await memecmd(int(row['type']),row['action'])
                return
    else: #minicmd
        if message.text == ".err":
            this_is_an_error() #type: ignore
        elif message.text == ".id":
            await message.reply(message.chat.id)
        elif message.text == ".shutdown":
            await shutdown(client,message)


@app.on_message(filters.text & filters.private)
@error_handling
async def on_message(client, message):
    await app.send_photo(message.chat.id,antispam())


from online import keep_alive 
keep_alive()
app.run()