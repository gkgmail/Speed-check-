from os import getenv

API_ID = int(getenv('API_ID') or 0)
API_HASH = getenv('API_HASH') or ''
BOT_TOKEN = getenv('BOT_TOKEN') or ''
OWNER_ID = list(map(int, (getenv('OWNER_ID') or '').split())) if (getenv('OWNER_ID') or '').strip() else []
MONGO_DB = getenv('MONGO_DB')
LOG_GROUP = getenv('LOG_GROUP') or ''
CHANNEL_ID = int(getenv('CHANNEL_ID') or 0)
FREEMIUM_LIMIT = int(getenv('FREEMIUM_LIMIT') or 0)
PREMIUM_LIMIT = int(getenv('PREMIUM_LIMIT') or 500)

if not (API_ID and API_HASH and BOT_TOKEN):
    print('⚠️  Warning: Missing API_ID, API_HASH, or BOT_TOKEN')