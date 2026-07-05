from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


import yt_dlp
import os
import asyncio

def extract_info_sync(url, opts):
    """Synchronous function to run yt-dlp safely."""
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return info, filename

async def process_download(client, message: Message, url: str, format_type: str):
    opts = {
        'cookiefile': 'ytcookies.txt', # Make sure this file exists in your main folder!
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True
    }

    if format_type == 'vid':
        opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    else:
        opts['format'] = 'bestaudio/best'
        opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        await message.edit_text("⬇️ Downloading from YouTube...")
        
        # Safe async execution for all Python 3.7+ versions
        loop = asyncio.get_event_loop()
        info, filename = await loop.run_in_executor(None, lambda: extract_info_sync(url, opts))
        
        # Adjust filename if yt-dlp converted it to mp3
        if format_type == 'aud' and not filename.endswith('.mp3'):
            filename = filename.rsplit('.', 1)[0] + '.mp3'

        await message.edit_text("⬆️ Uploading to Telegram...")
        
        # Upload to user
        if format_type == 'vid':
            await client.send_video(
                chat_id=message.chat.id, 
                video=filename, 
                caption=f"🎥 **{info.get('title', 'Video')}**"
            )
        else:
            await client.send_audio(
                chat_id=message.chat.id, 
                audio=filename, 
                caption=f"🎵 **{info.get('title', 'Audio')}**"
            )

        # Clean up file from the server
        if os.path.exists(filename):
            os.remove(filename)
            
        await message.delete() 

    except Exception as e:
        # If it fails, send the exact error back so you know what went wrong
        await message.edit_text(f"❌ **Download Error:** `{str(e)}`")


# Regex to detect YouTube links
YT_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+"

@Client.on_message(filters.regex(YT_REGEX))
async def yt_link_handler(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🎥 Video (MP4)", callback_data="vid"),
                InlineKeyboardButton("🎵 Audio (MP3)", callback_data="aud")
            ]
        ]
    )
    
    # quote=True ensures the bot replies to the link message so we can grab it later
    await message.reply_text(
        "**YouTube Link Detected!**\n\nPlease select the format you want to download:",
        reply_markup=keyboard,
        quote=True 
    )

@Client.on_callback_query(filters.regex(r"^(vid|aud)$"))
async def callback_handler(client: Client, callback_query: CallbackQuery):
    # 1. Answer the callback immediately to stop the button loading spinner
    await callback_query.answer("Processing your request...") 
    
    # 2. Retrieve the original message
    original_msg = callback_query.message.reply_to_message
    
    if not original_msg or not original_msg.text:
        await callback_query.message.edit_text("❌ **Error:** Original link not found. Please send the link again.")
        return
    
    url = original_msg.text
    format_type = callback_query.data
    
    await callback_query.message.edit_text("⏳ Processing your request...")
    
    # 3. Hand off to the downloader utility
    await process_download(client, callback_query.message, url, format_type)
