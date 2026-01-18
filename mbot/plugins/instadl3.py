from mbot import Mbot as app
from config import LOG_CHANNEL
import io
import time
import asyncio
from typing import List
import httpx
from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaPhoto, InputMediaVideo

IG_API = "https://vkrdownloader.org/server/"
IG_API_KEY = "vkrdownloader"

# 1. ADDED HEADERS: This mimics a real browser to bypass the 403 Forbidden error.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://vkrdownloader.org/"
}

# 2. Increased timeout slightly and added headers to the client
http = httpx.AsyncClient(timeout=120, headers=HEADERS)

# ───────────── RATE LIMIT ─────────────

USER_LIMIT = {}
LIMIT_TIME = 7

def rate_limited(user_id: int) -> bool:
    now = time.time()
    if now - USER_LIMIT.get(user_id, 0) < LIMIT_TIME:
        return True
    USER_LIMIT[user_id] = now
    return False

# ───────────── INSTAGRAM API ─────────────

async def fetch_instagram(url: str) -> dict | None:
    try:
        # Added params and headers check
        r = await http.get(
            IG_API,
            params={"api_key": IG_API_KEY, "vkr": url},
        )
        
        # LOGGING FOR DEBUGGING: Helps you see if it's still 403
        if r.status_code == 403:
            print("Error: 403 Forbidden. The server is blocking the request.")
            return None
        elif r.status_code != 200:
            print(f"Error: Status code {r.status_code}")
            return None
            
        return r.json()
    except Exception as e:
        print(f"Fetch Error: {e}")
        return None

# ───────────── DOWNLOAD ─────────────

async def download_file(url: str) -> bytes | None:
    try:
        # Re-using the headers for the download request too
        async with http.stream("GET", url) as r:
            if r.status_code != 200:
                return None
            return await r.aread()
    except Exception as e:
        print(f"Download Error: {e}")
        return None

# ───────────── LINK EXTRACTOR ─────────────

def extract_link(text: str) -> str | None:
    for word in text.split():
        if "instagram.com" in word:
            # Clean the link to remove extra characters
            return word.split("?")[0] if "?" in word else word
    return None

# ───────────── HANDLER ─────────────

@app.on_message(filters.regex(r"instagram\.com"))
async def instagram_handler(bot, message: Message):
    if not message.from_user or not message.text:
        return

    if rate_limited(message.from_user.id):
        return await message.reply_text("⏳ Please wait before sending another link.")

    link = extract_link(message.text)
    if not link:
        return

    status = await message.reply_text("🔍 Fetching Instagram media...")

    data = await fetch_instagram(link)
    
    # Check for specific failure reasons
    if not data:
        return await status.edit("❌ Server rejected the request (403). Try again later.")
    
    if not data.get("data"):
        return await status.edit("❌ Media not found or private account.")

    downloads = data["data"].get("downloads", [])
    if not downloads:
        return await status.edit("❌ No downloadable media found.")

    media_group = []
    await status.edit("📥 Downloading media...")

    for item in downloads[:10]:
        url = item.get("url")
        ext = item.get("ext", "").lower()

        content = await download_file(url)
        if not content:
            continue

        file = io.BytesIO(content)
        file.name = f"insta.{ext}"
        file.seek(0)

        if ext in ("jpg", "jpeg", "png", "webp"):
            media_group.append(InputMediaPhoto(file))
        elif ext in ("mp4", "webm"):
            media_group.append(InputMediaVideo(file, supports_streaming=True))

    if not media_group:
        return await status.edit("❌ Could not process the media files.")

    await status.edit("📤 Uploading to Telegram...")

    try:
        if len(media_group) == 1:
            m = media_group[0]
            if isinstance(m, InputMediaPhoto):
                await message.reply_photo(m.media)
            else:
                await message.reply_video(m.media, supports_streaming=True)
        else:
            await message.reply_media_group(media_group)
    except Exception as e:
        return await status.edit(f"❌ Upload error:\n`{e}`")

    await status.delete()

    # Log
    try:
        await bot.send_message(
            LOG_CHANNEL,
            f"📥 Instagram Download\n👤 {message.from_user.mention}\n🔗 {link}",
        )
    except:
        pass
