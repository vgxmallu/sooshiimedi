from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import re


import yt_dlp
import os
import asyncio

def extract_info_sync(url, opts):
    """Synchronous function to run yt-dlp"""
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return info, filename

async def process_download(client, message: Message, url: str, format_type: str):
    # Tell yt-dlp to use your cookies.txt file
    opts = {
        'cookiefile': 'ytcookies.txt',
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
        
        # Run yt-dlp in a separate thread to prevent blocking the Pyrogram async event loop
        info, filename = await asyncio.to_thread(extract_info_sync, url, opts)
        
        # Adjust filename extension if post-processed to mp3
        if format_type == 'aud' and not filename.endswith('.mp3'):
            filename = filename.rsplit('.', 1)[0] + '.mp3'

        await message.edit_text("⬆️ Uploading to Telegram...")
        
        # Uploading back to the user
        if format_type == 'vid':
            await client.send_video(
                chat_id=message.chat.id, 
                video=filename, 
                caption=f"🎥 **{info.get('title')}**"
            )
        else:
            await client.send_audio(
                chat_id=message.chat.id, 
                audio=filename, 
                caption=f"🎵 **{info.get('title')}**"
            )

        # Clean up the file from your server after uploading
        if os.path.exists(filename):
            os.remove(filename)
            
        await message.delete() # Remove the "Uploading..." text

    except Exception as e:
        await message.edit_text(f"❌ **Error:** `{str(e)}`")


# Regex to detect YouTube links
YT_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+"

@Client.on_message(filters.regex(YT_REGEX))
async def yt_link_handler(client: Client, message: Message):
    # The UI Keyboard
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🎥 Video (MP4)", callback_data="vid"),
                InlineKeyboardButton("🎵 Audio (MP3)", callback_data="aud")
            ]
        ]
    )
    
    # Replying to the user's link (quote=True is crucial here to retrieve the URL later)
    await message.reply_text(
        "**YouTube Link Detected!**\n\nPlease select the format you want to download:",
        reply_markup=keyboard,
        quote=True 
    )

@Client.on_callback_query(filters.regex(r"^(vid|aud)$"))
async def callback_handler(client: Client, callback_query: CallbackQuery):
    # Retrieve the original message that contained the YouTube URL
    original_msg = callback_query.message.reply_to_message
    
    if not original_msg:
        await callback_query.answer("Error: Original link not found. Send the link again.", show_alert=True)
        return
    
    url = original_msg.text
    format_type = callback_query.data
    
    await callback_query.message.edit_text("⏳ Processing your request...")
    
    # Hand off to the downloader utility
    await process_download(client, callback_query.message, url, format_type)
