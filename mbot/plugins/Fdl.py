import asyncio
import os
import yt_dlp
from config import COOKIES_FILE, DOWNLOAD_DIR, LOG_CHANNEL

from pyrogram import Client, filters
from pyrogram.types import Message 




def _download_sync(url: str, download_dir: str):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{download_dir}/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    
    # Inject cookies if the file exists and contains actual data
    if os.path.exists(COOKIES_FILE) and os.path.getsize(COOKIES_FILE) > 200:
        ydl_opts['cookiefile'] = COOKIES_FILE
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        
        # Ensure correct extension fallback
        if not os.path.exists(file_path):
            base, _ = os.path.splitext(file_path)
            file_path = base + ".mp4"
            
        return file_path, info.get('title', 'Facebook Video')

async def download_facebook_video(url: str, download_dir: str = "downloads"):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _download_sync, url, download_dir)


FB = """
🔵⬜ **FACEBOOK LINK ALERT** 🔵⬜

👊➖➖➖➖➖➖➖➖➖👊
📛**FACEBOOK link** : [click here]({})
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @SocialMediaX_dlbot
➖➖➖➖➖➖➖➖➖➖

#facebook #fb
"""


# Regex specifically targeting Facebook, FB Watch, and Reels variants
FB_REGEX = r"(https?://)?(www\.|m\.|watch\.|web\.)?(facebook\.com|fb\.watch|fb\.gg|fb\.com)/.+"

@Client.on_message(filters.regex(FB_REGEX))
async def handle_facebook_links(client: Client, message: Message):
    # Extract the exact matched link from the message
    url = message.matches[0].group(0)
    
    status = await message.reply_text("🔎 **Link detected. Processing...**")
    user = message.from_user
    mention = user.mention if user else "Anonymous"
    username = f"@{user.username}" if user and user.username else "No Username"
    dc_id = user.dc_id if user else "Unknown"
    user_id = user.id if user else message.chat.id

# Send the log message using the safe variables
    gg = await client.send_message(
        LOG_CHANNEL, 
        IG.format(url, mention, username, dc_id, user_id)
    )
    try:
        await status.edit_text("📥 **Downloading Facebook Video...**")
        file_path, title = await download_facebook_video(url, DOWNLOAD_DIR)
        
        if not os.path.exists(file_path):
            await status.edit_text("❌ Download failed: Media path not found.")
            return
            
        await status.edit_text("📤 **Uploading To Telegram...**")
        
        await message.reply_video(
            video=file_path,
            caption=f"🎬 **{title}**\n\n©️ @SocialMediaX_dlbot\n🔥🤖 @XBOTS_X"
        )
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        await status.delete()
        
    except Exception as e:
        error_msg = str(e)
        if "cookie" in error_msg.lower() or "login" in error_msg.lower():
            await status.edit_text("⚠️ **Authentication Error:** Update the `cookies.txt` file.")
        else:
            await status.edit_text(f"⚠️ **Error:** `{error_msg}`")
            
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

