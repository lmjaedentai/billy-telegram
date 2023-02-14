print('==========start==========')
import os
import sys
import asyncio
import random
import datetime
import traceback
from pyromod import listen
from pyrogram import Client,filters, errors
from pyrogram.types import Message, InlineKeyboardButton,ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineQueryResultArticle, InputTextMessageContent, ForceReply, ReplyKeyboardRemove, ChatPermissions

mylist=[
    [['jden','jaeden'],['electron']],
    [['yz','cyz','chan','yanzhe','@na_ch_t'],['gay','yanzhe is the future therapist','班长~~']],
    [['jus','justin'],['banana','diploma','gay']],
    [['gay'],['gay']],
    [['game','bs','cr','krunker'],['不要打game']],
    [['js','jiashiu','shau','家修','晨曦云','羽球学会副主席'],['lyl','milo susu','sunat?','puasa?','senior对我笑','我文学好低分啊']],
    [['rz','abu','runze'],['肾虚','腰酸','骨头痛','kp','kpl','suami rumah']],
    [['yy'],['callista']],
    [['callista'],['yy']],
    [['jolin'],['班长~~']],
    [['上帝','simyl'],['多吃水果','喝上帝汤','意外是可以避免的','上帝爱你','wei jen他啊']],
    [['yong','lw','linwei'],['不要打game','早点睡觉','几时追到她']],
    [['maznah'],['chan karangan?']],
    [['lol','lmao'],['lol','lmao']],
    [['bruh'],['bruh']],
    [['rasul'],['deputy prime minister...','Guys soalan KBAt','in 1957, Tunku...']],
    [['jibai','fk','fuck','shit'],['经研究显示，骂粗话可缓解肌肉酸痛','生气别人就是惩罚自己','不要鸡动，要蛋定']],
    [['georgia','joja','gg'],['why is ur bottle wearing ur mask?','SDG','sanitize this group.. too dirty']],
    [['lyl','chemi','chemistry'],['@Jiashiuuu','打起精神','jiashiu can u understand?']],
    ]


#QQ before we start
app = Client("verypigbot",api_id="17817209",api_hash=os.environ['API'],bot_token=os.environ['chan'])
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


#QQ other cmd
@app.on_message(filters.text)
@error_handling
async def on_message(client, message):
    if random.randint(0,1) != 1:
        return
    for i in mylist:
        for a in i[0]:
            if a in message.text.strip().lower():
                await app.send_message(message.chat.id,f'{i[1][random.randint(0, len(i[1]) - 1)]}')



from online import keep_alive 
keep_alive()
app.run()
