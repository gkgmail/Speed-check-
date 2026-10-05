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
# Version: 2.0.8 (Koyeb healthcheck + startup fix)
# License: MIT License
# ---------------------------------------------------

import asyncio
import gc
import importlib
from aiohttp import web
from aiojobs import create_scheduler
from pyrogram import idle

from devgagan import app, restrict_bot
from devgagan.modules import ALL_MODULES
from devgagan.core.mongo.plans_db import check_and_remove_expired_users

# ----------------------------Bot-Start---------------------------- #

loop = asyncio.get_event_loop()


async def schedule_expiry_check():
    scheduler = await create_scheduler()
    while True:
        await scheduler.spawn(check_and_remove_expired_users())
        await asyncio.sleep(60)
        gc.collect()


async def health_check(request):
    return web.json_response({"status": "ok", "service": "telegram_bot"})


async def start_health_server():
    web_app = web.Application()
    web_app.router.add_get("/", health_check)
    web_app.router.add_get("/health", health_check)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()
    print("✅ Health server started on port 8000")
    return runner


async def devggn_boot():
    for all_module in ALL_MODULES:
        importlib.import_module("devgagan.modules." + all_module)

    print("""
---------------------------------------------------
📂 Bot Deployed successfully ...
📝 Description: A Pyrogram bot for downloading files from Telegram channels or groups 
                and uploading them back to Telegram.
👨‍💻 Author: Gagan
🌐 GitHub: https://github.com/devgaganin/
📬 Telegram: https://t.me/team_spy_pro
▶️ YouTube: https://youtube.com/@dev_gagan
🗓️ Created: 2025-01-11
🔄 Last Modified: 2025-01-11
🛠️ Version: 2.0.8
📜 License: MIT License
---------------------------------------------------
""")

    # Start Telegram bot first
    await restrict_bot()

    # Then start HTTP health endpoint for Koyeb/Docker health checks
    await start_health_server()

    asyncio.create_task(schedule_expiry_check())
    print("Auto removal started ...")

    await idle()
    print("Bot stopped...")


if __name__ == "__main__":
    loop.run_until_complete(devggn_boot())

# ------------------------------------------------------------------ #
