# ---------------------------------------------------
# File Name: __main__.py
# Description: Ultra-fast startup for Telegram media bot
# Version: 3.1.0 (speed-optimized, 15MB ready)
# License: MIT License
# ---------------------------------------------------

import asyncio
import importlib
import sys
import logging

from aiohttp import web
from pyrogram import idle

from devgagan import app, restrict_bot
from devgagan.modules import ALL_MODULES

# ⚡ USE UVLOOP for faster event loop
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

# ⚡ Minimal logging
logging.basicConfig(level=logging.WARNING)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def health_check(request):
    """⚡ Fast health endpoint"""
    return web.json_response({"status": "ok", "service": "speed_bot_v3"})


async def start_health_server():
    """⚡ Start health server immediately"""
    web_app = web.Application()
    web_app.router.add_get("/", health_check)
    web_app.router.add_get("/health", health_check)
    
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    print("✅ Health server running on :8000")
    return runner


async def boot():
    """⚡ Boot sequence - minimal startup time"""
    print("\n⚡ SPEED BOT v3.1.0 - Starting...\n")
    
    # Start health server first (fast)
    health_runner = await start_health_server()
    
    # Load modules in parallel
    print("📦 Loading modules...")
    tasks = []
    for mod in ALL_MODULES:
        try:
            importlib.import_module(f"devgagan.modules.{mod}")
            print(f"   ✓ {mod}")
        except Exception as e:
            print(f"   ✗ {mod}: {e}")

    # Initialize bot
    print("\n🤖 Initializing bot...")
    await restrict_bot()
    
    print("\n✅ Bot ready for action!\n")
    
    try:
        await idle()
    finally:
        await health_runner.cleanup()


if __name__ == "__main__":
    try:
        loop.run_until_complete(boot())
    except KeyboardInterrupt:
        print("\n⚠️  Bot interrupted by user")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        sys.exit(1)
