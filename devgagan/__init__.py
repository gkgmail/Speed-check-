# ---------------------------------------------------
# File Name: __init__.py
# Version: 3.0.0 (⚡ ULTRA FAST + PREMIUM)
# License: MIT License
# ---------------------------------------------------

import asyncio
import logging
import time
import sys
from aiohttp import web
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait
from config import API_ID, API_HASH, BOT_TOKEN, STRING, MONGO_DB, DEFAULT_SESSION
from telethon.sync import TelegramClient
from motor.motor_asyncio import AsyncIOMotorClient

# ⚡ USE UVLOOP for faster async
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

logging.basicConfig(
    format="[%(levelname)s] %(message)s",
    level=logging.INFO,
)

botStartTime = time.time()

# ⚡ OPTIMIZED: Minimal workers
app = Client(
    "pyrobot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=4,
    parse_mode=ParseMode.MARKDOWN,
)

try:
    sex = TelegramClient('sexrepo', API_ID, API_HASH)
except:
    sex = None

pro = Client("ggbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING) if STRING else None
userrbot = Client("userrbot", api_id=API_ID, api_hash=API_HASH, session_string=DEFAULT_SESSION) if DEFAULT_SESSION else None

# ⚡ MongoDB setup
tclient = None
tdb = None
token = None

if MONGO_DB:
    try:
        tclient = AsyncIOMotorClient(MONGO_DB, serverSelectionTimeoutMS=5000)
        tdb = tclient["telegram_bot"]
        token = tdb["tokens"]
        print("✅ MongoDB connected")
    except Exception as e:
        print(f"⚠️  MongoDB failed: {e}")
        tclient = None


async def safe_start_bot(client, name="Bot", max_retries=2):
    """⚡ Fast bot startup"""
    for attempt in range(1, max_retries + 1):
        try:
            await client.start()
            print(f"✅ {name} started")
            return True
        except FloodWait as e:
            await asyncio.sleep(max(10, e.value))
        except Exception as e:
            if attempt == max_retries:
                raise
            await asyncio.sleep(3)
    return False


async def start_health_server():
    """⚡ Minimal health endpoint"""
    async def health_check(request):
        return web.json_response({"status": "ok"})

    web_app = web.Application()
    web_app.router.add_get("/health", health_check)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    print("✅ Health server ready")
    return runner


async def restrict_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    
    if not await safe_start_bot(app, "Main Bot", max_retries=2):
        raise RuntimeError("Failed to start bot")
    
    me = await app.get_me()
    BOT_ID = me.id
    BOT_USERNAME = me.username
    BOT_NAME = me.first_name
    
    print(f"✅ Bot: @{BOT_USERNAME}")
    
    if pro:
        try:
            await safe_start_bot(pro, "Pro Client", max_retries=1)
        except:
            pass
    
    if userrbot:
        try:
            await safe_start_bot(userrbot, "User Bot", max_retries=1)
        except:
            pass


async def main():
    await restrict_bot()
    await start_health_server()
    from pyrogram import idle
    await idle()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
