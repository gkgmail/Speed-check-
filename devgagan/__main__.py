import asyncio
from pyrogram import idle
from devgagan import app, restrict_bot

async def main():
    await restrict_bot()
    print('🤖 Bot ready!')
    await idle()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('⚠️  Bot stopped')