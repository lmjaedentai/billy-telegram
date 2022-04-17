print('==========youtube==========')
import os
from pyromod import listen
from pyrogram import Client,filters,emoji
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube, exceptions

#QQ slash commands
app = Client("pokokpisangbot",api_id="17817209",api_hash="1317fd0bcc2b193c3dbd04defc748358",bot_token="5104353128:AAHgalcIDT_Q7MWcAfwmXqvak8rCYD-PPQ4")
with app:
    app.send_message("lmjaedentai", "login\ndevice: [repl.it](https://replit.com/@lmjaedentai/Billy-Youtube#main.py)", disable_web_page_preview=True, disable_notification=True)
    print('==========login==========')


@app.on_message(filters.command(["help","start"]))
async def start_command(client, message):
    await message.reply('**KaiCheng Youtube Downloader 📽️**\nDownload mp3, mp4 from Youtube video or a playlist.\nTelegram can block annoying ads, security risk and privacy leakage so you can use the command safely. \n \n/video - download mp4 from Youtube  \n/audio - download mp3 from Youtube  \n/playlist - download Youtube playlist \n\n\n2022 by KaiCheng 🦄. Contact @lmjaedentai 🧐 if you face any problem.')

def checkvalid(url):
    try:
        title = YouTube(url).title 
    except exceptions.RegexMatchError:
        return False
    else:
        return True

@app.on_message(filters.command("video"))
async def video(client, message):
    #download
    query = await app.ask(message.chat.id, "📺  What is the **url** of youtube video you want to download?")
    if checkvalid(query.text) == False:
        return await message.reply("❌ **Invalid url.** We only support videos from Youtube. ")
    await app.send_chat_action(message.chat.id, "typing")
    status = await message.reply("⬇️  downloading media...")
    music = YouTube(query.text).streams.filter(file_extension='mp4').order_by('resolution').desc().first().download()
    await status.delete()
    #send
    await app.send_chat_action(message.chat.id, "upload_video")
    status = await message.reply("➡️  sending media...")
    await message.reply_document(music,caption=YouTube(query.text).title,force_document=True)
    #done
    await app.send_chat_action(message.chat.id, "cancel")
    await status.delete()
    os.remove(music)

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

@app.on_message(filters.command("playlist"))
async def playlist(client, message):
    return await message.reply("still under construction 🏗️ 🚧")
    query = await app.ask(message.chat.id, "🎦 Which format of the media you want to download?", reply_markup=ReplyKeyboardMarkup([['mp3','mp4']],resize_keyboard=False))



# from online import keep_alive 
# keep_alive()
#/cancel LINK https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
app.run()