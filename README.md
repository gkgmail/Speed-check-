# Speed-check-

A small deployable Python application with a health check endpoint ready for Koyeb/Render/Heroku.

## Deployment

- Build uses Dockerfile
- Start command is `python app.py`
- Health endpoint is `/health`

## Required env vars for Telegram bot

```bash
API_ID=123456
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
OWNER_ID=123456789
MONGO_DB=your_mongodb_url  # optional
```

## Run locally

```bash
python app.py
```
