# ---------------------------------------------------
# File Name: __init__.py
# Version: 3.1.0 (⚡ ULTRA FAST + 15MB OPTIMIZED)
# License: MIT License
# ---------------------------------------------------

import asyncio
import logging
import time
import sys
import os
from aiohttp import web
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait
from config import API_ID, API_HASH, BOT_TOKEN, STRING, MONGO_DB, DEFAULT_SESSION
from telethon.sync import TelegramClient
from motor.motor_asyncio import AsyncIOMotorClient

# ⚡ USE UVLOOP for 5x faster async performance
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

# ⚡ OPTIMIZED: Minimal workers for fast response
app = Client(
    "pyrobot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=2,
    parse_mode=ParseMode.MARKDOWN,
    no_updates=False,
    takeout=False,
)

try:
    sex = TelegramClient('sexrepo', API_ID, API_HASH)
except:
    sex = None

pro = Client("ggbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING) if STRING else None
userrbot = Client("userrbot", api_id=API_ID, api_hash=API_HASH, session_string=DEFAULT_SESSION) if DEFAULT_SESSION else None

# ⚡ MongoDB setup with connection pooling
tclient = None
tdb = None
token = None

if MONGO_DB:
    try:
        tclient = AsyncIOMotorClient(
            MONGO_DB,
            serverSelectionTimeoutMS=5000,
            maxPoolSize=10,
            minPoolSize=2,
            retryWrites=False,
        )
        tdb = tclient["telegram_bot"]
        token = tdb["tokens"]
        print("✅ MongoDB connected (pooled)")
    except Exception as e:
        print(f"⚠️  MongoDB failed: {e}")
        tclient = None


async def safe_start_bot(client, name="Bot", max_retries=2):
    """⚡ Fast bot startup with flood wait handling"""
    for attempt in range(1, max_retries + 1):
        try:
            await client.start()
            print(f"✅ {name} started")
            return True
        except FloodWait as e:
            wait_time = min(e.value, 30)
            print(f"⏳ Flood wait {wait_time}s...")
            await asyncio.sleep(wait_time)
        except Exception as e:
            if attempt == max_retries:
                raise
            await asyncio.sleep(2)
    return False


async def start_health_server():
    """⚡ Ultra-minimal health server for fast checks"""
    async def health_check(request):
        return web.json_response({"status": "ok", "uptime": time.time() - botStartTime})

    async def root_check(request):
        return web.Response(text="OK", status=200)

    web_app = web.Application()
    web_app.router.add_get("/", root_check)
    web_app.router.add_get("/health", health_check)
    
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    print("✅ Health server ready on :8000")
    return runner


async def restrict_bot():
    """⚡ Initialize bot with minimal startup time"""
    global BOT_ID, BOT_NAME, BOT_USERNAME
    
    if not await safe_start_bot(app, "Main Bot", max_retries=2):
        raise RuntimeError("Failed to start bot")
    
    try:
        me = await app.get_me()
        BOT_ID = me.id
        BOT_USERNAME = me.username
        BOT_NAME = me.first_name
        print(f"✅ Bot: @{BOT_USERNAME} | ID: {BOT_ID}")
    except Exception as e:
        print(f"❌ Error getting bot info: {e}")
        raise
    
    # Start optional clients (non-blocking)
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
    """⚡ Main startup - health server runs while bot waits"""
    health_runner = await start_health_server()
    await restrict_bot()
    
    try:
        from pyrogram import idle
        await idle()
    finally:
        await health_runner.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⚠️  Bot stopped")
    except Exception as e:
        print(f"❌ Critical error: {e}")
        sys.exit(1)
