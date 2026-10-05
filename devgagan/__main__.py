# ---------------------------------------------------
# File Name: __main__.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 3.0.0 (⚡ ULTRA FAST + PREMIUM UI)
# License: MIT License
# ---------------------------------------------------

import asyncio
import gc
import importlib
import sys
from aiohttp import web
from pyrogram import idle

from devgagan import app, restrict_bot
from devgagan.modules import ALL_MODULES

# ⚡ OPTIMIZED: Try to use uvloop for faster async
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    print("✨ Using uvloop - Ultra Fast Mode Enabled")
except ImportError:
    pass

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def health_check(request):
    return web.json_response({"status": "ok", "service": "telegram_bot", "version": "3.0.0"})


async def start_health_server():
    """⚡ Minimal health server for Koyeb"""
    web_app = web.Application(loop=loop)
    web_app.router.add_get("/", health_check)
    web_app.router.add_get("/health", health_check)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    print("✨ Health server started on port 8000")
    return runner


async def devggn_boot():
    """⚡ FAST bot startup with minimal overhead"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                  🚀 TEAM SPY BOT v3.0.0 🚀               ║
║                  ⚡ ULTRA FAST + PREMIUM ⚡             ║
╠══════════════════════════════════════════════════════════╣
║ 📂 Bot Deployment Mode: PREMIUM OPTIMIZATION             ║
║ 📝 Type: Media Downloader + Content Saver                ║
║ 👨‍💻 Developer: Gagan (@dev_gagan)                        ║
║ 🌐 GitHub: https://github.com/devgaganin/                ║
║ 📬 Telegram: https://t.me/team_spy_pro                   ║
║ ⚡ Speed: ≈15 Mbps Download/Upload (Free Plan)          ║
║ 🛠️ Version: 3.0.0 (Optimized for Koyeb)                 ║
║ 📜 License: MIT License                                  ║
╚══════════════════════════════════════════════════════════╝
    """)

    # ⚡ Load all modules (async)
    for all_module in ALL_MODULES:
        try:
            importlib.import_module("devgagan.modules." + all_module)
        except Exception as e:
            print(f"⚠️  Module {all_module} failed to load: {e}")

    # Start bot
    print("\n🔄 Starting Telegram Bot...")
    await restrict_bot()
    print("✅ Bot started successfully!\n")

    # Start health server
    await start_health_server()

    print("\n🌟 Bot is now LIVE and ready to receive commands!\n")
    print("═" * 60)
    await idle()
    print("\n❌ Bot stopped...")


if __name__ == "__main__":
    try:
        loop.run_until_complete(devggn_boot())
    except KeyboardInterrupt:
        print("\n⚠️  Bot interrupted by user.")
    except Exception as e:
        print(f"\n❌ Critical Error: {e}")
        sys.exit(1)
