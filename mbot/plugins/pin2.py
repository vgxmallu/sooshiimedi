import asyncio
import importlib
import os
import shutil
import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Set your download directory
TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")

@Client.on_message(filters.command("pidl") & filters.private)
async def pinterest_image_dl(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ **Usage:** `/pidl [Pinterest Link]`")
        
    url = message.command[1]
    user = message.from_user
    
    # 1. Setup a unique folder for this specific task to prevent file overwrites
    task_dir = os.path.join(TMP_DOWNLOAD_DIRECTORY, f"img_{user.id}_{int(time.time())}")
    os.makedirs(task_dir, exist_ok=True)
    
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("Open on Pinterest", url=url)]])
    status = await message.reply_text("📸 **Extracting Image...**")
    
    try:
        # 2. Run your custom 'pin' library in a background thread
        pin_dl = importlib.import_module("pin")
        await asyncio.to_thread(
            pin_dl.run_library_main,
            url, task_dir, 0, -1, False, False, False, False, False, True, False, False, None, None, None
        )
        
        # 3. Search the unique folder for the downloaded JPG
        image_file = None
        for file in os.listdir(task_dir):
            if file.endswith(".jpg"):
                image_file = os.path.join(task_dir, file)
                break
                
        # 4. Upload to Telegram
        if image_file:
            await client.send_photo(
                chat_id=message.chat.id,
                photo=image_file,
                caption="**Downloaded via @SocialMediaX_dlbot**",
                reply_to_message_id=message.id,
                reply_markup=markup
            )
            await status.delete()
        else:
            await status.edit_text("❌ **Failed:** Could not extract an image from this link. Make sure it is a valid image Pin.")

    except Exception as e:
        await status.edit_text(f"❌ Failed to process image: `{e}`")
        
    finally:
        # 5. Clean up the folder to keep your Koyeb server storage completely empty
        if os.path.exists(task_dir):
            shutil.rmtree(task_dir)
  
