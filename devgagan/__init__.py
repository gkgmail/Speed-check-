# ---------------------------------------------------
# File Name: __init__.py
# Version: 3.1.0
# License: MIT License
# ---------------------------------------------------

import asyncio
import logging
import os

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    pass

logging.basicConfig(level=logging.INFO)

from pyrogram import Client
from pyrogram.enums import ParseMode
from config import API_ID, API_HASH, BOT_TOKEN

app = None

if API_ID and API_HASH and BOT_TOKEN:
    app = Client(
        "pyrobot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        workers=2,
        parse_mode=ParseMode.MARKDOWN,
    )
else:
    app = None

BOT_ID = None
BOT_NAME = None
BOT_USERNAME = None


async def restrict_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    if app is None:
        print("⚠️ Telegram env vars missing; bot startup skipped.")
        return
    try:
        await app.start()
        me = await app.get_me()
        BOT_ID = me.id
        BOT_USERNAME = me.username
        BOT_NAME = me.first_name
        print(f"✅ Bot started: @{BOT_USERNAME}")
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
