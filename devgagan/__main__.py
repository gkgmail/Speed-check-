import asyncio
import sys

from devgagan import app, restrict_bot


async def main():
    if app is None:
        print("⚠️ Telegram settings are not configured. Nothing to start.")
        return
    await restrict_bot()
    print("✅ Bot ready")
    from pyrogram import idle
    await idle()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped")
    except Exception as e:
        print(f"Critical error: {e}")
        sys.exit(1)
