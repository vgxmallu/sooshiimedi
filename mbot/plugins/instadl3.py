#!/usr/bin/env python3
# instabot_pyrogram.py
import os
import io
import time
import sqlite3
import asyncio
from contextlib import closing
from typing import List, Optional
from dotenv import load_dotenv

import httpx
from pyrogram import Client, filters
from pyrogram.types import Message
load_dotenv()
from mbot import Mbot as app
from config import LOG_CHANNEL
API_URL = "https://vkrdownloader.xyz/server/"
API_KEY = "vkrdownloader"

DB_FILE = "users.db"

IG = """
📤📱 **LOG ALERT** 💻📱
➖➖➖➖➖➖➖➖➖➖➖
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @SocialMediaX_dlbot
➖➖➖➖➖➖➖➖➖➖
#ig #instagram
"""

# ---------- External API ----------
async def fetch_insta_media(link: str) -> Optional[dict]:
    params = {"api_key": API_KEY, "vkr": link}
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(API_URL, params=params)
            if resp.status_code != 200:
                return None
            data = resp.json()
            if not data.get("data") or not data["data"].get("downloads"):
                return None
            return data
    except Exception:
        return None

# ---------- Download with progress ----------
async def download_with_progress(url: str, msg: Message, label: str) -> Optional[bytes]:
    """
    Downloads the given URL and edits `msg` every ~2s with progress.
    Returns bytes on success or None on failure.
    """
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("GET", url) as resp:
                if resp.status_code != 200:
                    return None
                total = int(resp.headers.get("content-length", 0) or 0)
                # If content-length missing, we fallback to a simpler download
                if total == 0:
                    # fallback: read all bytes without progress
                    content = await resp.aread()
                    return content

                chunks = bytearray()
                start = time.time()
                last_update = 0.0
                downloaded = 0
                async for chunk in resp.aiter_bytes(1024 * 64):
                    if not chunk:
                        continue
                    chunks.extend(chunk)
                    downloaded += len(chunk)
                    now = time.time()
                    if now - last_update >= 2.0:
                        last_update = now
                        pct = int(downloaded * 100 / total) if total else 0
                        elapsed = now - start
                        eta = (total - downloaded) * elapsed / downloaded if downloaded else 0
                        eta_str = f"{int(eta)}s" if eta < 3600 else f"{int(eta//60)}m"
                        try:
                            await msg.edit_text(f"{label} {pct}%  ETA: {eta_str}")
                        except Exception:
                            # ignore edit errors (message may be deleted)
                            pass
                return bytes(chunks)
    except Exception:
        return None


# Instagram link handler (anywhere in text)
@app.on_message(filters.regex(r"(?i)instagram\.com"))
async def download_insta(client: Client, message: Message):
    if not message.text:
        return
    link = message.text.strip().split()[0]  # take first token as link (similar to original)
    wait = await message.reply_text("Fetching media…")
    await client.send_message(LOG_CHANNEL, IG.format(message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
   
    data = await fetch_insta_media(link)
    if not data:
        return await wait.edit_text("❌ Could not retrieve media.")
    downloads = data["data"].get("downloads", [])
    best_video = None
    for item in downloads:
        url = item.get("url")
        if not url:
            continue
        ext = (item.get("ext") or "mp4").lower()
        if ext in {"mp4", "webm"}:
            best_video = url
            break
    if not best_video:
        return await wait.edit_text("❌ No video found.")
    await wait.edit_text("📥 Downloading…")
    media_bytes = await download_with_progress(best_video, wait, "📥")
    if not media_bytes:
        return await wait.edit_text("❌ Download failed.")
    await wait.edit_text("📤 Uploading…")
    # prepare BytesIO for Pyrogram
    filename = f"insta_{message.id}.mp4"
    bio = io.BytesIO(media_bytes)
    bio.name = filename
    bio.seek(0)
    try:
        await message.reply_video(bio)
    except Exception as e:
        # fallback: send as document if video fails
        try:
            bio.seek(0)
            await message.reply_document(bio, file_name=filename)
        except Exception as e2:
            await wait.edit_text(f"❌ Upload failed: {e} / {e2}")
            return
    await wait.delete()
