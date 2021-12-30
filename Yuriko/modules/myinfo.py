# Module Credits @AASFCYBERKING Give Credits Take Module 💓😁
from telethon import custom, events, Button
import os,re
import asyncio

from Yuriko import telethn as bot
from Yuriko import telethn as tgbot
from Yuriko import telethn as aasf
from Yuriko.events import register 

edit_time = 5
yuriko1 = "https://telegra.ph/file/81f062c8feff7247e62bb.jpg"
yuriko2 = "https://telegra.ph/file/c3bef437e795ce2c050b3.jpg"
yuriko3 = "https://telegra.ph/file/da1975cb71798db34e1e8.jpg"
yuriko4 = "https://telegra.ph/file/147b74b6943b8faf40ad5.jpg"

@register(pattern="/myinfo")
async def proboyx(event):
  button = [[custom.Button.inline("CHECK",data="information")]]
  on = await aasf.send_message(event.chat, f"**❦ Hᴇʏ {(event.sender.first_name)}**\n\n**❦ I Aᴍ [Yuriko](https://t.me/YurikoRobot)**\n**❦ I Wᴀs Cʀᴇᴀᴛᴇᴅ Bʏ [DeeCoDeBots](t.me/DeeCoDeBots)**", file=yuriko1, buttons=button)

  await asyncio.sleep(edit_time)
  ok = await aasf.edit_message(event.chat_id, on, file=yuriko2, buttons=button) 

  await asyncio.sleep(edit_time)
  ok2 = await aasf.edit_message(event.chat_id, ok, file=yuriko3, buttons=button)

  await asyncio.sleep(edit_time)
  ok3 = await aasf.edit_message(event.chat_id, ok2, file=yuriko1, buttons=button)
    
  await asyncio.sleep(edit_time)
  ok4 = await aasf.edit_message(event.chat_id, ok3, file=yuriko3, buttons=button)
    
  await asyncio.sleep(edit_time)
  ok5 = await aasf.edit_message(event.chat_id, ok4, file=yuriko2, buttons=button)
    
  await asyncio.sleep(edit_time)
  ok6 = await aasf.edit_message(event.chat_id, ok5, file=yuriko3, buttons=button)
    
  await asyncio.sleep(edit_time)
  ok7 = await aasf.edit_message(event.chat_id, ok6, file=yuriko1, buttons=button)

@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"information")))
async def callback_query_handler(event):
  try:
    boy = event.sender_id
    PRO = await bot.get_entity(boy)
    YURIKO = "YOUR DETAILS BY YURIKO \n"
    YURIKO += f"FIRST NAME : {PRO.first_name} \n"
    YURIKO += f"LAST NAME : {PRO.last_name}\n"
    YURIKO += f"YOU BOT : {PRO.bot} \n"
    YURIKO += f"RESTRICTED : {PRO.restricted} \n"
    YURIKO += f"USER ID : {boy}\n"
    YURIKO += f"USERNAME : {PRO.username}\n"
    await event.answer(YURIKO, alert=True)
  except Exception as e:
    await event.reply(f"{e}")

__mod_name__ = "Myinfo"

__help__ = """
 ~ /myinfo *:* Get Your Details On Inline. 
"""
