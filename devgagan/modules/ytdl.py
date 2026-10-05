# ---------------------------------------------------
# File Name: ytdl.py
# Description: ⚡ ULTRA OPTIMIZED video/audio downloader
# Version: 3.0.0 (Premium Speed Edition)
# License: MIT License
# ---------------------------------------------------

import yt_dlp
import os
import tempfile
import time
import asyncio
import random
import string
import requests
import logging
from devgagan import sex as client
from pyrogram import Client, filters
from telethon import events
from telethon.tl.types import DocumentAttributeVideo
from concurrent.futures import ThreadPoolExecutor
import aiohttp
from devgagan import app
import aiofiles

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# ⚡ OPTIMIZED: Minimal thread pool
thread_pool = ThreadPoolExecutor(max_workers=3)
ongoing_downloads = {}

# ⚡ CHUNK sizes optimized for speed
CHUNK_SIZE = 8 * 1024 * 1024  # 8MB chunks
MAX_CONNECTIONS = 4  # Parallel connections

# 🎨 PREMIUM UI STYLES
PREMIUM_DOWNLOAD = "\n╔════════════════════════════════════════╗\n║     🎬 PREMIUM DOWNLOADER ACTIVE 🎬     ║\n╚════════════════════════════════════════╝"
PREMIUM_UPLOAD = "\n╔════════════════════════════════════════╗\n║      ⬆️ PREMIUM UPLOADER ACTIVE ⬆️       ║\n╚════════════════════════════════════════╝"
PREMIUM_SUCCESS = "\n╔════════════════════════════════════════╗\n║    ✅ DOWNLOAD COMPLETED ✅ PREMIUM      ║\n╚════════════════════════════════════════╝"

def d_thumbnail(thumbnail_url, save_path):
    """⚡ Fast thumbnail download"""
    try:
        response = requests.get(thumbnail_url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        return save_path
    except:
        return None


async def download_thumbnail_async(url, path):
    """⚡ Async thumbnail download"""
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(path, 'wb') as f:
                        f.write(await response.read())
        except:
            pass


def get_random_string(length=7):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


@client.on(events.NewMessage(pattern="/dl"))
async def handler(event):
    """⚡ PREMIUM Video Downloader"""
    user_id = event.sender_id
    
    if user_id in ongoing_downloads:
        await event.reply("⏳ **You already have an ongoing download!**\n*Please wait...*")
        return
    
    if len(event.message.text.split()) < 2:
        await event.reply(f"{PREMIUM_DOWNLOAD}\n\n**📥 Usage:** `/dl <video-link>`\n\n*Supported:* YouTube, Instagram, Facebook, TikTok & 100+ sites")
        return
    
    url = event.message.text.split()[1]
    ongoing_downloads[user_id] = True
    
    try:
        msg = await event.reply(f"{PREMIUM_DOWNLOAD}\n\n⏳ **Fetching video info...**")
        
        # ⚡ FAST yt-dlp options
        ydl_opts = {
            'format': 'best[height<=720]',  # ⚡ Smaller size = faster
            'outtmpl': f"/tmp/{get_random_string()}.mp4",
            'socket_timeout': 30,
            'concurrent_fragment_downloads': MAX_CONNECTIONS,
            'quiet': True,
            'no_warnings': True,
            'retries': 2,
        }
        
        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=True)
        
        info = await asyncio.get_event_loop().run_in_executor(thread_pool, download)
        title = info.get('title', 'Video')
        file_path = ydl_opts['outtmpl'].replace(f"{get_random_string()}", os.path.basename(ydl_opts['outtmpl']).split('.')[0])
        
        # ⚡ Find actual file
        for f in os.listdir('/tmp'):
            if f.endswith('.mp4') and f.startswith(get_random_string()):
                file_path = os.path.join('/tmp', f)
                break
        
        if os.path.exists(file_path):
            await msg.edit(f"{PREMIUM_UPLOAD}\n\n⬆️ **Uploading to Telegram...**")
            
            file_size = os.path.getsize(file_path) / (1024*1024)
            await app.send_document(
                event.chat_id,
                file_path,
                caption=f"\n✨ **{title}** ✨\n\n📊 Size: `{file_size:.2f}` MB\n⚡ Downloaded by **PREMIUM TEAM SPY BOT**\n🔗 *Powered by @team_spy_pro*",
                progress=progress_bar,
                progress_args=("═", 10, "⬆️ UPLOADING")
            )
            
            await msg.delete()
            os.remove(file_path)
            await event.reply(f"{PREMIUM_SUCCESS}\n\n🎉 **Download Complete!**")
        else:
            await msg.edit("❌ **Download failed!** File not found.")
    
    except Exception as e:
        await event.reply(f"❌ **Error:** `{str(e)[:50]}`")
    
    finally:
        ongoing_downloads.pop(user_id, None)


@client.on(events.NewMessage(pattern="/adl"))
async def audio_handler(event):
    """⚡ PREMIUM Audio Downloader"""
    user_id = event.sender_id
    
    if user_id in ongoing_downloads:
        await event.reply("⏳ **Audio download in progress!**")
        return
    
    if len(event.message.text.split()) < 2:
        await event.reply(f"{PREMIUM_DOWNLOAD}\n\n**🎵 Usage:** `/adl <link>`\n\n*Extract MP3 from any video*")
        return
    
    url = event.message.text.split()[1]
    ongoing_downloads[user_id] = True
    
    try:
        msg = await event.reply(f"{PREMIUM_DOWNLOAD}\n\n🎵 **Extracting audio...**")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"/tmp/{get_random_string()}.mp3",
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            'quiet': True,
            'no_warnings': True,
        }
        
        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=True)
        
        info = await asyncio.get_event_loop().run_in_executor(thread_pool, download)
        
        await msg.edit(f"{PREMIUM_UPLOAD}\n\n⬆️ **Uploading audio...**")
        
        audio_file = ydl_opts['outtmpl']
        if os.path.exists(audio_file):
            await app.send_document(
                event.chat_id,
                audio_file,
                caption=f"\n🎵 **{info.get('title', 'Audio')}** 🎵\n\n⚡ Extracted by **PREMIUM BOT**"
            )
            os.remove(audio_file)
            await msg.delete()
            await event.reply(f"{PREMIUM_SUCCESS}\n\n🎉 **Audio Ready!**")
    
    except Exception as e:
        await event.reply(f"❌ **Error:** `{str(e)[:50]}`")
    
    finally:
        ongoing_downloads.pop(user_id, None)


def progress_bar(current, total, ud_type, file_name, ud_type_str):
    """⚡ PREMIUM Progress Bar"""
    percentage = current * 100 / total
    pro_bar = "" * int(percentage // 10) + "▯" * (10 - int(percentage // 10))
    
    return f"""
╔════════════════════════════════════════╗
║  {ud_type_str} PREMIUM UPLOAD ACTIVE   ║
╠════════════════════════════════════════╣
║ {pro_bar}
║ Progress: {percentage:.2f}%
║ Speed: {current / (1024*1024):.2f}MB / {total / (1024*1024):.2f}MB
╚════════════════════════════════════════╝
    """
