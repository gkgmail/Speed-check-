import asyncio
import logging
from pyrogram import Client
from pyrogram.enums import ParseMode
from config import API_ID, API_HASH, BOT_TOKEN

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass

logging.basicConfig(level=logging.INFO)

app = Client(
    'pyrobot',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=2,
    parse_mode=ParseMode.MARKDOWN,
)

BOT_ID = None
BOT_NAME = None
BOT_USERNAME = None

async def restrict_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    try:
        await app.start()
        me = await app.get_me()
        BOT_ID = me.id
        BOT_USERNAME = me.username
        BOT_NAME = me.first_name
        print(f'✅ Bot started: @{BOT_USERNAME}')
    except Exception as e:
        print(f'❌ Error: {e}')