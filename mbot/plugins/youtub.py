from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio


import yt_dlp
import os
import asyncio

def extract_meta_sync(url, opts):
    """Synchronous function to get video metadata without downloading the media."""
    opts['playlist_items'] = '1' # Ensure we only get one item if it's a playlist link
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)

def extract_info_sync(url, opts):
    """Synchronous function to execute the full download phase."""
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return info, filename

async def process_download(client, message: Message, url: str, format_type: str):
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
        # Note: We use edit_caption because the target message is now a Photo message type
        await message.edit_caption(caption="⬇️ Downloading from YouTube...")
        
        loop = asyncio.get_event_loop()
        info, filename = await loop.run_in_executor(None, lambda: extract_info_sync(url, opts))
        
        # Adjust file extension pointer if postprocessors converted it to .mp3
        if format_type == 'audx' and not filename.endswith('.mp3'):
            filename = filename.rsplit('.', 1)[0] + '.mp3'

        await message.edit_caption(caption="⬆️ Uploading to Telegram...")
        
        # Handle delivery back to the private chat
        if format_type == 'vidx':
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

        # Remove local media file from hosting space to optimize storage
        if os.path.exists(filename):
            os.remove(filename)
            
        await message.delete() 

    except Exception as e:
        await message.edit_caption(caption=f"❌ **Download Error:** `{str(e)}`")


YT_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+"

@Client.on_message(filters.regex(YT_REGEX))
async def yt_link_handler(client: Client, message: Message):
    url = message.text
    status_msg = await message.reply_text("🔍 Fetching video details...", quote=True)
    
    opts = {'cookiefile': 'cookies.txt', 'quiet': True}
    
    try:
        # Fetch metadata safely in a background thread
        loop = asyncio.get_event_loop()
        meta = await loop.run_in_executor(None, lambda: extract_meta_sync(url, opts))
        
        title = meta.get("title", "Video")
        thumbnail = meta.get("thumbnail")
        
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🎥 Video (MP4)", callback_data="vidx"),
                    InlineKeyboardButton("🎵 Audio (MP3)", callback_data="audx")
                ]
            ]
        )
        
        caption = f"🎬 **{title}**\n\nSelect your preferred download format below:"
        
        # If a thumbnail is available, send it as a photo UI
        if thumbnail:
            await message.reply_photo(
                photo=thumbnail,
                caption=caption,
                reply_markup=keyboard,
                quote=True
            )
            await status_msg.delete()
        else:
            # Fallback to text if no thumbnail is found
            await status_msg.edit_text(caption, reply_markup=keyboard)
            
    except Exception as e:
        await status_msg.edit_text(f"❌ **Error fetching video details:** `{str(e)}`")

@Client.on_callback_query(filters.regex(r"^(vidx|audx)$"))
async def callbackx_handler(client: Client, callback_query: CallbackQuery):
    # 1. Answer callback instantly to dismiss Telegram's loading indicator
    await callback_query.answer("Processing download...") 
    
    # 2. Get the user's original message containing the link
    original_msg = callback_query.message.reply_to_message
    
    if not original_msg or not original_msg.text:
        await callback_query.message.edit_caption(caption="❌ **Error:** Original link missing. Resend the link.")
        return
    
    url = original_msg.text
    format_type = callback_query.data
    
    await callback_query.message.edit_caption(caption="⏳ Initializing downoad...")
    
    # 3. Process download utility pass-through
    await process_download(client, callback_query.message, url, format_type)
