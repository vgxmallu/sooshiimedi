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
        # Note: Ensure 'pincookies.txt' exists in your bot's root directory
        cmd = [
            "yt-dlp", 
            "--cookies", "pincookies.txt", 
            "-o", f"{task_dir}/media.%(ext)s", 
            url
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd, 
            stdout=asyncio.subprocess.PIPE, 
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        # Check if the process failed
        if process.returncode != 0:
            error_msg = stderr.decode().splitlines()[-1] if stderr else "Unknown error"
            raise Exception(error_msg)
        
        # Logic to find and send the file
        files = os.listdir(task_dir)
        if not files:
            raise Exception("No media downloaded. Check if cookies are valid or link is correct.")
            
        media_path = os.path.join(task_dir, files[0])
        
        # Send as Photo
        await client.send_photo(
            chat_id=message.chat.id, 
            photo=media_path, 
            reply_to_message_id=message.id
        )
        await status.delete()

    except Exception as e:
        await status.edit_text(f"❌ **Error:** `{str(e)}`")
    finally:
        # Cleanup
        if os.path.exists(task_dir):
            shutil.rmtree(task_dir)
