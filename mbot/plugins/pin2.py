import asyncio
import os
import shutil
import time
from pyrogram import Client, filters

# Ensure this path points to where your cookies.txt is stored

TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")

@Client.on_message(filters.command("pidl"))
async def pinterest_dl_with_cookies(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ **Usage:** `/pidl [Pinterest Link]`")
        
    url = message.command[1]
    user = message.from_user
    task_dir = os.path.join(TMP_DOWNLOAD_DIRECTORY, f"img_{user.id}_{int(time.time())}")
    os.makedirs(task_dir, exist_ok=True)
    
    status = await message.reply_text("🔄 **Downloading using cookie auth...**")
    
    try:
        # Add the --cookies flag to the yt-dlp command
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
        await process.communicate()
        
        # Logic to find and send the file
        files = os.listdir(task_dir)
        if not files:
            raise Exception("No media downloaded. Check if cookies are valid.")
            
        media_path = os.path.join(task_dir, files[0])
        
        # Send as Photo or Document
        await client.send_photo(message.chat.id, photo=media_path, reply_to_message_id=message.id)
        await status.delete()

    except Exception as e:
        await status.edit_text(f"❌ **Error:** {str(e)}")
    finally:
        if os.path.exists(task_dir):
            shutil.rmtree(task_dir)
