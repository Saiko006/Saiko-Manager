import os
import asyncio

from aiohttp import ClientSession
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

from Yuriko import arq
from Yuriko import pbot as bot1

session = ClientSession()

pornhub = arq.pornhub

db = {}

def get_text(message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None

# Let's Go----------------------------------------------------------------------
@bot1.on_message(filters.command(["phub"]) & ~filters.edited & filters.private)
async def sarch(_, message):
    search = get_text(message)
    if message.chat.username:
        chatusername = f"[{message.chat.title}](t.me/{message.chat.username})"
    else:
        chatusername = message.chat.title
    if not search:
        await message.reply(
            f"""
😏 Woi panteq {message.from_user.mention} kasih judul

» Contoh : /phub mom and soon
""",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"• ᴛᴜᴛᴜᴘ •", callback_data="no_cb"),
                    ],
                ]
            ),
        )
    try:
        resp = await pornhub(search, thumbsize="large_hd")
        res = resp.result
    except:
        await message.delete()
        return
    resolt = f"""
**➡️ TITLE:** {res[0].title}
**⏰ DURATION:** {res[0].duration}
**👁‍🗨 VIEWERS:** {res[0].views}
**🌟 RATING:** {res[0].rating}

**Powered By 🔰:** ᴋᴇᴋɪɴɪᴀɴ ʀᴏʙᴏᴛ!
"""
    await message.delete()
    m = await message.reply_photo(
        photo=res[0].thumbnails[0].src,
        caption=resolt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("➡️", callback_data="next"),
                    InlineKeyboardButton("🔗", callback_data="delete"),
                ],
                [
                    InlineKeyboardButton("📸", callback_data="ss"),
                    InlineKeyboardButton("📥", callback_data="downbad"),
                ],
                [
                    InlineKeyboardButton("Close", callback_data="close"),
                ],
            ]
        ),
        parse_mode="markdown",
    )   
    new_db = {"result": res, "curr_page": 0}
    db[message.chat.id] = new_db


# Next Button--------------------------------------------------------------------------
@bot1.on_callback_query(filters.regex("next"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("something went wrong.. **try again**")
        return
    res = data["result"]
    curr_page = int(data["curr_page"])
    cur_page = curr_page + 1
    db[query.message.chat.id]["curr_page"] = cur_page
    if len(res) <= (cur_page + 1):
        cbb = [
            [
                InlineKeyboardButton("⬅️", callback_data="previous"),
                InlineKeyboardButton("📸", callback_data="ss"),
            ],
            [
                InlineKeyboardButton("🔗", callback_data="delete"),
                InlineKeyboardButton("📥", callback_data="downbad"),
            ],
            [
                InlineKeyboardButton("Close", callback_data="close"),
            ],
        ]
    else:
        cbb = [
            [
                InlineKeyboardButton("⬅️", callback_data="previous"),
                InlineKeyboardButton("➡️", callback_data="next"),
            ],
            [
                InlineKeyboardButton("🔗", callback_data="delete"),
                InlineKeyboardButton("📸", callback_data="ss"),
                InlineKeyboardButton("📥", callback_data="downbad"),
            ],
            [
                InlineKeyboardButton("Close", callback_data="close"),
            ],
        ]
    resolt = f"""
**🏷 TITLE:** {res[cur_page].title}
**⏰ DURATION:** {res[cur_page].duration}
**👁‍🗨 VIEWERS:** {res[cur_page].views}
**🌟 RATING:** {res[cur_page].rating}

**Powered By 🔰:** ᴋᴇᴋɪɴɪᴀɴ ʀᴏʙᴏᴛ!
"""

    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )


# Previous Button--------------------------------------------------------------------------
@bot1.on_callback_query(filters.regex("previous"))
async def callback_query_next(_, query):
    m = query.message
    try:
        data = db[query.message.chat.id]
    except:
        await m.edit("something went wrong.. **try again**")
        return
    res = data["result"]
    curr_page = int(data["curr_page"])
    cur_page = curr_page - 1
    db[query.message.chat.id]["curr_page"] = cur_page
    if cur_page != 0:
        cbb = [
            [
                InlineKeyboardButton("⬅️", callback_data="previous"),
                InlineKeyboardButton("➡️", callback_data="next"),
            ],
            [
                InlineKeyboardButton("🔗", callback_data="delete"),
                InlineKeyboardButton("📸", callback_data="ss"),
                InlineKeyboardButton("📥", callback_data="downbad"),
            ],
            [
                InlineKeyboardButton("Close", callback_data="close"),
            ],
        ]
    else:
        cbb = [
            [
                InlineKeyboardButton("➡️", callback_data="next"),
                InlineKeyboardButton("🔗", callback_data="Delete"),
            ],
            [
                InlineKeyboardButton("📸", callback_data="ss"),
                InlineKeyboardButton("📥", callback_data="downbad"),
            ],
            [
                InlineKeyboardButton("Close", callback_data="close"),
            ],
        ]
    resolt = f"""
**🏷 TITLE:** {res[cur_page].title}
**⏰ DURATION:** {res[cur_page].duration}
**👁‍🗨 VIEWERS:** {res[cur_page].views}
**🌟 RATING:** {res[cur_page].rating}

**Powered By 🔰:** ᴋᴇᴋɪɴɪᴀɴ ʀᴏʙᴏᴛ!
"""
    await m.edit_media(media=InputMediaPhoto(res[cur_page].thumbnails[0].src))
    await m.edit(
        resolt,
        reply_markup=InlineKeyboardMarkup(cbb),
        parse_mode="markdown",
    )


# Delete Button--------------------------------------------------------------------------
# @bot1.on_callback_query(filters.regex("delete"))
@bot1.on_callback_query(filters.regex("delete"))
def callback_query_delete(bot, query):
    # await query.message.delete()
    data = db[query.message.chat.id]
    res = data["result"]
    curr_page = int(data["curr_page"])
    cur_page = curr_page - 1
    db[query.message.chat.id]["curr_page"] = cur_page
    umrl = res[curr_page].url
    bot.send_message(
        text=umrl, chat_id=query.message.chat.id, disable_web_page_preview=True
    )


# SCREENSHOT BUTTON ---------------------------------------


@bot1.on_callback_query(filters.regex("ss"))
async def callback_query_delete(bot, query):
    data = db[query.message.chat.id]
    res = data["result"]
    curr_page = int(data["curr_page"])
    ss = res[curr_page].thumbnails
    for src in ss:
        await bot.send_photo(photo=src.src, chat_id=query.message.chat.id)


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


@bot1.on_callback_query(filters.regex("downbad"))
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


#no cb
@bot1.on_callback_query(filters.regex("no_cb"))
async def cb_cls(client, query):
    await query.message.delete()
    tm = await client.send_message(
        query.message.chat.id,
        "**Baikla {} Selamat Sange**".format(query.from_user.mention),
    )
    await asyncio.sleep(5)
    await tm.delete()
