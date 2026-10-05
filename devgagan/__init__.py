# ---------------------------------------------------
# File Name: __init__.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.7 (Koyeb health check fix)
# License: MIT License
# ---------------------------------------------------

import asyncio
import logging
import time
from aiohttp import web
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait
from config import API_ID, API_HASH, BOT_TOKEN, STRING, MONGO_DB, DEFAULT_SESSION
from telethon.sync import TelegramClient
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

botStartTime = time.time()

# ⚡ OPTIMIZED: Reduced workers from 50 to 8 for faster startup & lower memory
app = Client(
    "pyrobot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=8,
    parse_mode=ParseMode.MARKDOWN,
)

try:
    sex = TelegramClient('sexrepo', API_ID, API_HASH)
except Exception as e:
    print(f"⚠️  Secondary Telethon client initialization failed: {e}")
    sex = None

if STRING:
    pro = Client("ggbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING)
else:
    pro = None

if DEFAULT_SESSION:
    userrbot = Client("userrbot", api_id=API_ID, api_hash=API_HASH, session_string=DEFAULT_SESSION)
else:
    userrbot = None

# ⚡ OPTIMIZED: MongoDB setup - only if MONGO_DB is provided
tclient = None
tdb = None
token = None

if MONGO_DB:
    try:
        tclient = AsyncIOMotorClient(MONGO_DB)
        tdb = tclient["telegram_bot"]
        token = tdb["tokens"]
        print("✅ MongoDB client initialized")
    except Exception as e:
        print(f"⚠️  MongoDB initialization failed: {e}")
        tclient = None
        token = None
else:
    print("⚠️  MONGO_DB not configured. Database features disabled.")


async def create_ttl_index():
    """Ensure the TTL index exists for the `tokens` collection."""
    if token is None:
        return
    try:
        await token.create_index("expires_at", expireAfterSeconds=0)
    except Exception as e:
        print(f"⚠️  TTL index creation failed: {e}")


async def setup_database():
    if token is None:
        print("⚠️  MongoDB not available. Skipping TTL index setup.")
        return
    await create_ttl_index()
    print("✅ MongoDB TTL index created.")


async def safe_start_bot(client, client_name="Bot", max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            await client.start()
            print(f"✅ {client_name} started successfully (attempt {attempt}/{max_retries})")
            return True
        except FloodWait as e:
            wait_seconds = max(30, e.value + 5)
            print(f"⏳ {client_name}: Telegram flood protection activated. Waiting {wait_seconds} seconds (attempt {attempt}/{max_retries})...")
            await asyncio.sleep(wait_seconds)
        except Exception as e:
            print(f"❌ {client_name} startup error (attempt {attempt}/{max_retries}): {e}")
            if attempt == max_retries:
                raise
            await asyncio.sleep(5)
    return False


async def start_health_server():
    """Serve a tiny HTTP endpoint so Koyeb/hosting platform can health check the bot."""
    async def health_check(request):
        return web.json_response({"status": "ok", "service": "telegram_bot"})

    web_app = web.Application()
    web_app.router.add_get("/", health_check)
    web_app.router.add_get("/health", health_check)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    print("✅ Health server started on port 8000")
    return runner


async def restrict_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await setup_database()

    if not await safe_start_bot(app, "Main Bot", max_retries=3):
        raise RuntimeError("Failed to start main bot after retries")

    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    BOT_NAME = f"{getme.first_name} {getme.last_name}" if getme.last_name else getme.first_name

    print(f"✅ Bot started successfully!")
    print(f"📱 Bot ID: {BOT_ID}")
    print(f"👤 Bot Username: @{BOT_USERNAME}")

    if pro:
        try:
            await safe_start_bot(pro, "Pro Client", max_retries=2)
        except Exception as e:
            print(f"⚠️  Pro client failed: {e}")

    if userrbot:
        try:
            await safe_start_bot(userrbot, "User Bot", max_retries=2)
        except Exception as e:
            print(f"⚠️  User bot failed: {e}")


async def main():
    await restrict_bot()
    await start_health_server()
    print("🚀 Bot and health server are running...")
    await app.idle()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
    except FloodWait as e:
        print(f"❌ Critical: Telegram flood protection. Wait {e.value} seconds before restarting.")
        raise
    except Exception as e:
        print(f"❌ Critical bot initialization error: {e}")
        raise
