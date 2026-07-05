import asyncio
import os
import shutil
import time
from pyrogram import Client, filters
from pyrogram.types import Message # Fix: Imported Message type

# Ensure this path points to where your cookies.txt is stored
TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")

@Client.on_message(filters.command("pidl") & filters.private) # Added & filters.private for consistency
async def pinterest_dl_with_cookies(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ **Usage:** `/pidl [Pinterest Link]`")
        
    url = message.command[1]
    user = message.from_user
    # Create the base directory if it doesn't exist
    if not os.path.exists(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)

    task_dir = os.path.join(TMP_DOWNLOAD_DIRECTORY, f"img_{user.id}_{int(time.time())}")
    os.makedirs(task_dir, exist_ok=True)
    
    status = await message.reply_text("🔄 **Downloading using cookie auth...**")
    
        try:
        # Force yt-dlp to download only the image (thumbnail) and skip video processing
        # This prevents the "No video formats found" error entirely
        cmd = [
            "yt-dlp", 
            "--cookies", "pincookies.txt", 
            "-o", f"{task_dir}/media.%(ext)s", 
            "--write-thumbnail",  # Force download of the preview image
            "--skip-download",    # Skip actual video stream downloading
            url
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd, 
            stdout=asyncio.subprocess.PIPE, 
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        
        # Search specifically for image files
        image_files = [f for f in os.listdir(task_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        if not image_files:
            raise Exception("Could not extract an image from this pin.")
            
        media_path = os.path.join(task_dir, image_files[0])
        
        # Always send as a photo
        await client.send_photo(
            chat_id=message.chat.id, 
            photo=media_path, 
            reply_to_message_id=message.id
        )
        await status.delete()

    except Exception as e:
        await status.edit_text(f"❌ **Error:** `{str(e)}`")

