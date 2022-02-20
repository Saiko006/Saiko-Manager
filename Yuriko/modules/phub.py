# Disclaimer:
#   Telegram May ban your bot or your account since Porns aren't allowed in Telegram.
#   We aren't reponsible for Your causes....Use with caution...
#   We recommend you to use Alt account.
#   For support https://t.me/PatheticProgrammers

import os
from aiohttp import ClientSession
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo
from Python_ARQ import ARQ 
from asyncio import get_running_loop
from wget import download

db = {}

async def download_url(url: str):
    loop = get_running_loop()
    file = await loop.run_in_executor(None, download, url)
    return file


# Let's Go----------------------------------------------------------------------
@app.on_message(filters.private & filters.incoming & filters.command("phub"))
async def sarch(_,message):
    if len(message.command) < 2:
        await message.reply_text(
            "**😏 Woi panteq kasih judul**\n\n» Contoh : /phub mom and son"
        )
        return
    m = await message.reply_text("Getting Results.....")
    search = message.text.split(None, 1)[1]
    try:
        resp = await pornhub(search)
        res = resp.result
    except:
        await m.edit("Found Nothing")
        return
    resolt = f"""
**🏷Title:** {res[0].title}
**⏰DURATION:** {res[0].duration}
**👀views:** {res[0].views}
**⭐rating:** {res[0].rating}
**Powered By 🔰:** ᴋᴇᴋɪɴɪᴀɴ ʀᴏʙᴏᴛ!"""
    await m.delete()
    m = await message.reply_photo(
        photo=res[0].thumbnails[0].src,
        caption=resolt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("↪️ Next",
                                         callback_data="next"),
                    InlineKeyboardButton("🚮 Delete",
                                         callback_data="delete"),
                ],
                [
                    InlineKeyboardButton("📥 Download",
                                         callback_data="downbad")
                ]
            ]
        ),
        parse_mode="markdown",
    )
    new_db={"result":res,"curr_page":0}
    db[message.chat.id] = new_db
    
 # Next Button--------------------------------------------------------------------------
@app.on_callback_query(filters.regex("next"))
async def callback_query_next(_, query):
    if not db[query.message.chat.id]:
        return
    data = db[query.message.chat.id]
    m = query.message
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page+1
    db[query.message.chat.id]['curr_page'] = cur_page
    if len(res) <= (cur_page+1):
        cbb = [
                [
                    InlineKeyboardButton("↩️Previous",
                                         callback_data="previous"),
                    InlineKeyboardButton("Download",
                                         callback_data="downbad"),
                ],
                [
                    InlineKeyboardButton("🚮Delete",
                                         callback_data="delete"),
                ]
              ]
    else:
        cbb = [
                [
                    InlineKeyboardButton("↩️ Previous",
                                         callback_data="previous"),
                    InlineKeyboardButton("↪️ Next",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("🚮 Delete",
                                         callback_data="delete"),
                    InlineKeyboardButton("📥 Download",
                                         callback_data="downbad")
                ]
              ]
    resolt = f"""
**🏷Title:** {res[cur_page].title}
**⏰DURATION:** {res[cur_page].duration}
**👀views:** {res[cur_page].views}
**⭐rating:** {res[cur_page].rating}
**Powered By 🔰:** ᴋᴇᴋɪɴɪᴀɴ ʀᴏʙᴏᴛ!"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )
 
# Previous Button-------------------------------------------------------------------------- 
@app.on_callback_query(filters.regex("previous"))
async def callback_query_next(_, query):
    if not db[query.message.chat.id]:
        return
    data = db[query.message.chat.id]
    m = query.message
    res = data['result']
    curr_page = int(data['curr_page'])
    cur_page = curr_page-1
    db[query.message.chat.id]['curr_page'] = cur_page
    if cur_page != 0:
        cbb=[
                [
                    InlineKeyboardButton("↩️ Previous",
                                         callback_data="previous"),
                    InlineKeyboardButton("↪️ Next",
                                         callback_data="next"),
                ],
                [
                    InlineKeyboardButton("🚮 Delete",
                                         callback_data="delete"),
                    InlineKeyboardButton("📥 Download",
                                         callback_data="downbad")
                ]
            ]
    else:
        cbb=[
                [
                    InlineKeyboardButton("↪️ Next",
                                         callback_data="next"),
                    InlineKeyboardButton("🚮 Delete",
                                         callback_data="Delete"),
                ],
                [
                    InlineKeyboardButton("📥 Download",
                                         callback_data="downbad")
                ]
            ]
    resolt = f"""
**🏷Title:** {res[cur_page].title}
**⏰DURATION:** {res[cur_page].duration}
**👀views:** {res[cur_page].views}
**⭐rating:** {res[cur_page].rating}
**Powered By 🔰:** ᴋᴇᴋɪɴɪᴀɴ ʀᴏʙᴏᴛ!"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )

# Download Button--------------------------------------------------------------------------    
# DOWNLOAD BUTTON ------------------------------------------

import os

import requests
import validators
import youtube_dl
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def downloada(url, quality):

    if quality == "2":
        ydl_opts_start = {
            "format": "best",  # This Method Don't Need ffmpeg , if you don't have ffmpeg use This
            "outtmpl": f"localhoct/%(id)s.%(ext)s",
            "no_warnings": False,
            "logtostderr": False,
            "ignoreerrors": False,
            "noplaylist": True,
            "http_chunk_size": 2097152,
            "writethumbnail": True,
        }
        with youtube_dl.YoutubeDL(ydl_opts_start) as ydl:
            result = ydl.extract_info("{}".format(url))
            title = ydl.prepare_filename(result)
            ydl.download([url])
        return f"{title}"



@app.on_callback_query(filters.regex("downbad"))
def webpage(c, m):  # c Mean Client | m Mean Message
    print(m.message.chat.id)
    data = db[m.message.chat.id]
    curr_page = int(data["curr_page"])
    curr_page - 1

    vidtitle = data["result"][curr_page].title
    vidurl = data["result"][curr_page].url

    url1 = res = data["result"][curr_page].url
    if validators.url(url1):
        sample_url = "https://da.gd/s?url={}".format(url1)
        url = requests.get(sample_url).text

    global check_current
    check_current = 0

    def progress(current, total):
        global check_current
        if ((current // 1024 // 1024) % 50) == 0:
            if check_current != (current // 1024 // 1024):
                check_current = current // 1024 // 1024
                upmsg.edit(f"{current//1024//1024}MB / {total//1024//1024}MB Uploaded.")
        elif (current // 1024 // 1024) == (total // 1024 // 1024):
            upmsg.delete()

    url1 = f"{url} and 2"
    chat_id = m.message.chat.id
    data = url1
    url, quaitly = data.split(" and ")
    dlmsg = c.send_message(chat_id, "`downloading video..`")
    path = downloada(url, quaitly)
    upmsg = c.send_message(chat_id, "`uploading video..`")
    dlmsg.delete()
    thumb = path.replace(".mp4", ".jpg", -1)
    if os.path.isfile(thumb):
        thumb = open(thumb, "rb")
        path = open(path, "rb")
        # c.send_photo(chat_id,thumb,caption=' ') #Edit it and add your Bot ID :)
        c.send_video(
            chat_id,
            path,
            thumb=thumb,
            caption=f"[{vidtitle}]({vidurl})",
            file_name=" ",
            supports_streaming=True,
            progress=progress,
        )  # Edit it and add your Bot ID :)
        upmsg.delete()
    else:
        path = open(path, "rb")
        c.send_video(
            chat_id,
            path,
            caption=f"[{vidtitle}]({vidurl})",
            file_name=" ",
            supports_streaming=True,
            progress=progress,
        )
        upmsg.delete()
    
# Delete Button-------------------------------------------------------------------------- 
@app.on_callback_query(filters.regex("delete"))
async def callback_query_delete(_, query):
    m = query.message
    await m.delete()
    
app.run()
