# If You Kanged This Module Plz Give Credits It Was Made By @AASFCYBERKING
# I Really Hardworked For This Module
import asyncio
import os
import requests
import datetime
import time
from PIL import Image
from io import BytesIO
from datetime import datetime
import random
from telethon import events, version
from Yuriko.events import register
from Yuriko import telethn as aasf
from Yuriko import StartTime, dispatcher
from telethon.tl.types import ChannelParticipantsAdmins

edit_time = 5
""" =======================2022====================== """
newyear1 = "https://telegra.ph/file/1d07f65c9bf8c3ee19b58.jpg"
newyear2 = "https://telegra.ph/file/58f1b1d5f0a9676df0965.jpg"
newyear3 = "https://telegra.ph/file/8fd3001e529edcf74abc6.jpg"
newyear4 = "https://telegra.ph/file/82f463463ee8b9775ae43.jpg"
newyear5 = "https://telegra.ph/file/60df28d89f49395728f48.jpg"
""" =======================2022====================== """

@register(pattern=("/newyear"))
async def hmm(event):
    chat = await event.get_chat()
    await event.delete()
    pm_caption = f"**Happy New Year 2022 From {(event.sender.first_name)} **\n\n"
    pm_caption += "**By @TeamDeeCoDe X Team**\n\n"
    on = await aasf.send_file(event.chat_id, file=newyear1,caption=pm_caption)

    await asyncio.sleep(edit_time)
    ok = await aasf.edit_message(event.chat_id, on, file=newyear2) 

    await asyncio.sleep(edit_time)
    ok2 = await aasf.edit_message(event.chat_id, ok, file=newyear3)

    await asyncio.sleep(edit_time)
    ok3 = await aasf.edit_message(event.chat_id, ok2, file=newyear4)
    
    await asyncio.sleep(edit_time)
    ok4 = await aasf.edit_message(event.chat_id, ok3, file=newyear1)
    
    await asyncio.sleep(edit_time)
    ok5 = await aasf.edit_message(event.chat_id, ok4, file=newyear2)
    
    await asyncio.sleep(edit_time)
    ok6 = await aasf.edit_message(event.chat_id, ok5, file=newyear3)
    
    await asyncio.sleep(edit_time)
    ok7 = await aasf.edit_message(event.chat_id, ok6, file=newyear4)
    
    await asyncio.sleep(edit_time)
    ok8 = await aasf.edit_message(event.chat_id, ok7, file=newyear5)
