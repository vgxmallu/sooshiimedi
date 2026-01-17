
from mbot import Mbot as app
from config import LOG_CHANNEL


#!/usr/bin/env python3
import io
import time
import asyncio
from typing import List

import httpx
from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaPhoto, InputMediaVideo



IG_API = "https://vkrdownloader.xyz/server/"
IG_API_KEY = "vkrdownloader"

http = httpx.AsyncClient(timeout=120)

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
        r = await http.get(
            IG_API,
            params={"api_key": IG_API_KEY, "vkr": url},
        )
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# ───────────── DOWNLOAD ─────────────

async def download_file(url: str) -> bytes | None:
    try:
        async with http.stream("GET", url) as r:
            if r.status_code != 200:
                return None
            return await r.aread()
    except:
        return None

# ───────────── LINK EXTRACTOR ─────────────

def extract_link(text: str) -> str | None:
    for word in text.split():
        if "instagram.com" in word:
            return word
    return None

# ───────────── HANDLER ─────────────

@app.on_message(filters.regex(r"instagram\.com"))
async def instagram_handler(_, message: Message):
    if not message.from_user or not message.text:
        return

    if rate_limited(message.from_user.id):
        return await message.reply_text("⏳ Please wait before sending another link.")

    link = extract_link(message.text)
    if not link:
        return

    status = await message.reply_text("🔍 Fetching Instagram media...")

    data = await fetch_instagram(link)
    if not data or not data.get("data"):
        return await status.edit("❌ Failed to fetch media.")

    downloads = data["data"].get("downloads", [])
    if not downloads:
        return await status.edit("❌ No media found.")

    media_group = []

    await status.edit("📥 Downloading media...")

    for item in downloads[:10]:  # Telegram max album = 10
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
        return await status.edit("❌ Media download failed.")

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
        await app.send_message(
            LOG_CHANNEL,
            f"📥 Instagram Download\n👤 {message.from_user.mention}\n🔗 {link}",
        )
    except:
        pass
