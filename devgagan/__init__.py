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
# Version: 2.0.6 (Fixed FloodWait handling + Koyeb optimized)
# License: MIT License
# ---------------------------------------------------

import asyncio
import logging
import time
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait
from config import API_ID, API_HASH, BOT_TOKEN, STRING, MONGO_DB, DEFAULT_SESSION
from telethon.sync import TelegramClient
from motor.motor_asyncio import AsyncIOMotorClient

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

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
    workers=8,  # Optimized from 50 → 8 (better for Koyeb)
    parse_mode=ParseMode.MARKDOWN
)

# ⚡ REQUIRED: Other modules depend on this symbol
# NOTE: Do NOT use bot_token with TelegramClient if already using it with Pyrogram Client
# Use session string instead to avoid Telegram flood blocking
try:
    sex = TelegramClient('sexrepo', API_ID, API_HASH)
    # Do not start with bot_token - use DEFAULT_SESSION if available
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

# ⚡ OPTIMIZED: Use only if actually needed. Comment out if not used.
# telethon_client = TelegramClient('telethon_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

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

# Run the TTL index creation when the bot starts
async def setup_database():
    if token is None:
        print("⚠️  MongoDB not available. Skipping TTL index setup.")
        return
    await create_ttl_index()
    print("✅ MongoDB TTL index created.")

async def safe_start_bot(client, client_name="Bot", max_retries=3):
    """
    Safely start a Pyrogram client with FloodWait handling.
    
    Args:
        client: Pyrogram Client instance
        client_name: Name of the client (for logging)
        max_retries: Maximum number of retry attempts
    
    Returns:
        bool: True if successful, False otherwise
    """
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
            await asyncio.sleep(5)  # Brief pause before retry
    
    return False

async def restrict_bot():
    """Main bot initialization with safe startup logic."""
    global BOT_ID, BOT_NAME, BOT_USERNAME
    
    await setup_database()
    
    # Start main bot with FloodWait handling
    if not await safe_start_bot(app, "Main Bot", max_retries=3):
        raise RuntimeError("Failed to start main bot after retries")
    
    # Get bot information
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    BOT_NAME = f"{getme.first_name} {getme.last_name}" if getme.last_name else getme.first_name
    
    print(f"✅ Bot started successfully!")
    print(f"📱 Bot ID: {BOT_ID}")
    print(f"👤 Bot Username: @{BOT_USERNAME}")
    
    # Start secondary clients if configured
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

# Start the bot safely
try:
    loop.run_until_complete(restrict_bot())
except FloodWait as e:
    print(f"❌ Critical: Telegram flood protection. Wait {e.value} seconds before restarting.")
    exit(1)
except Exception as e:
    print(f"❌ Critical bot initialization error: {e}")
    exit(1)
