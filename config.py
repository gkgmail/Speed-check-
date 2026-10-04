from os import getenv

INST_COOKIES = """
# write insta cookies
"""

YTUB_COOKIES = """
# write yt cookies
"""

API_ID = int(getenv("API_ID") or 0)
API_HASH = getenv("API_HASH") or ""
BOT_TOKEN = getenv("BOT_TOKEN") or ""
OWNER_ID = list(map(int, (getenv("OWNER_ID") or "").split())) if (getenv("OWNER_ID") or "").strip() else []
MONGO_DB = getenv("MONGO_DB") or None
LOG_GROUP = getenv("LOG_GROUP") or ""
CHANNEL_ID = int(getenv("CHANNEL_ID") or 0)
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT") or 0)
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT") or 500)
WEBSITE_URL = getenv("WEBSITE_URL") or "upshrink.com"
AD_API = getenv("AD_API") or ""
STRING = getenv("STRING") or None
YT_COOKIES = getenv("YT_COOKIES") or YTUB_COOKIES
DEFAULT_SESSION = getenv("DEFAULT_SESSION") or getenv("DEFAUL_SESSION") or None
INSTA_COOKIES = getenv("INSTA_COOKIES") or INST_COOKIES

# required checks for deployment
if not (API_ID and API_HASH and BOT_TOKEN):
    raise RuntimeError("Missing required env vars: API_ID, API_HASH, BOT_TOKEN")
