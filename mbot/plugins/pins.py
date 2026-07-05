import asyncio
import importlib
import logging
import math
import os
import shutil
import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from config import LOG_CHANNEL

TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)
logger = logging.getLogger(__name__)

# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n.get(raised_to_pow, "") + "B"

def time_formatter(seconds: int) -> str:
    result = ""
    v_m = 0
    remainder = seconds
    r_ange_s = {"days": 24 * 60 * 60, "hours": 60**2, "minutes": 60, "seconds": 1}
    for age, divisor in r_ange_s.items():
        v_m, remainder = divmod(remainder, divisor)
        v_m = int(v_m)
        if v_m != 0:
            result += f" {v_m} {age} "
    return result

async def progress(current, total, status_msg, start, type_of_ps):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        percentage = current * 100 / total
        elapsed_time = round(diff)
        if elapsed_time == 0:
            return
        speed = current / diff
        time_to_completion = round((total - current) / speed)
        estimated_total_time = elapsed_time + time_to_completion
        
        progress_str = "[{0}{1}]\nPercent: {2}%\n".format(
            "".join(["█" for _ in range(math.floor(percentage / 5))]),
            "".join(["░" for _ in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        try:
            await status_msg.edit_text(f"{type_of_ps}\n {tmp}")
        except Exception:
            pass 

async def take_screen_shot(video_file, output_directory, ttl):
    out_put_file_name = f"{output_directory}/{time.time()}.jpg"
    file_generator_command = [
        "ffmpeg", "-ss", str(ttl), "-i", video_file, "-vframes", "1", out_put_file_name,
    ]
    process = await asyncio.create_subprocess_exec(
        *file_generator_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await process.communicate()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None

# ==========================================
# SMART DIRECT LINK HANDLER
# ==========================================


@Client.on_message(filters.command("pidl2"))
async def pinimg(client: Client, message: Message):
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)

    if len(message.command) < 2:
        return await message.reply_text("Use command `/pidl [link]` to download Pinterest Images.")
        
    url = message.command[1]
    user = message.from_user

    # Send Log
    mm = f"Bot: @SocialMediaX_dlbot\n👤**User** : [{user.first_name}](tg://user?id={user.id})\n👻**User Name** : @{user.username}\n🪧**Message** : {message.text}\n\n#Pinterest #ImageDl"
    try:
        await client.send_message(LOG_CHANNEL, mm)
    except Exception:
        pass

    markup = InlineKeyboardMarkup([[InlineKeyboardButton("Open on Pinterest", url=url)]])
    status = await message.reply_text("__Your Request is Processing.\nPlease Wait...__")

    try:
        pin_dl = importlib.import_module("pin2")
        
        # Wrapped in to_thread so the custom module doesn't block the async loop
        await asyncio.to_thread(
            pin_dl.run_library_main,
            url, TMP_DOWNLOAD_DIRECTORY, 0, -1, False, False, False, False, False, True, False, False, None, None, None
        )
        
        j = None
        for file in os.listdir(TMP_DOWNLOAD_DIRECTORY):
            if file.endswith(".log"):
                os.remove(f"{TMP_DOWNLOAD_DIRECTORY}/{file}")
                continue
            if file.endswith(".jpg") and file != "thumb_image.jpg":
                j = f"{TMP_DOWNLOAD_DIRECTORY}/{file}"

        if j and os.path.exists(j):
            c_time = time.time()
            await client.send_photo(
                chat_id=message.chat.id,
                photo=j,
                caption="**Downloaded via @SocialMediaX_dlbot**",
                reply_to_message_id=message.id,
                reply_markup=markup,
                progress=progress,
                progress_args=(status, c_time, "Uploading Image...")
            )
            await status.delete()
            os.remove(j)
        else:
            await status.edit_text("❌ Could not extract image from the provided link.")

    except Exception as e:
        await status.edit_text(f"❌ Failed to process image: `{e}`")

# Regex catches pin.it and pinterest.com links automatically
PINTEREST_REGEX = r"(https?://(?:www\.)?(?:pinterest\.[a-zA-Z0-9]+|pin\.it)[^\s]+)"

@Client.on_message(filters.regex(PINTEREST_REGEX) & filters.private)
async def auto_pinterest_download(client: Client, message: Message):
    # 1. Extract URL and setup unique folder for this specific user's task
    url = message.matches[0].group(1)
    user = message.from_user
    task_dir = os.path.join(TMP_DOWNLOAD_DIRECTORY, f"task_{user.id}_{int(time.time())}")
    os.makedirs(task_dir, exist_ok=True)
    
    # Send Log
    mm = f"Bot: @SocialMediaX_dlbot\n👤**User** : [{user.first_name}](tg://user?id={user.id})\n👻**User Name** : @{user.username}\n🪧**Link** : {url}\n\n#Pinterest #AutoDL"
    try:
        await client.send_message(LOG_CHANNEL, mm)
    except Exception:
        pass

    markup = InlineKeyboardMarkup([[InlineKeyboardButton("Open on Pinterest", url=url)]])
    status = await message.reply_text("🔄 **Processing your link...**")
    
    try:
        # 2. Try fetching as Video first using yt-dlp
        komut = f"yt-dlp -o '{task_dir}/media.%(ext)s' {url}"
        process = await asyncio.create_subprocess_shell(komut)
        await process.communicate()
        
        # Check if an mp4 was downloaded
        video_file = None
        for file in os.listdir(task_dir):
            if file.endswith(".mp4"):
                video_file = os.path.join(task_dir, file)
                break
                
        c_time = time.time()
        
        # 3. IF IT IS A VIDEO:
        if video_file:
            await status.edit_text("📤 **Uploading to telegram...**")
            duration = 0
            width, height = 0, 0
            thumb = None
            
            metadata = extractMetadata(createParser(video_file))
            if metadata and metadata.has("duration"):
                duration = metadata.get("duration").seconds
                thumb = await take_screen_shot(video_file, task_dir, (duration / 2))
                
            if thumb and os.path.exists(thumb):
                thumb_meta = extractMetadata(createParser(thumb))
                if thumb_meta:
                    if thumb_meta.has("width"): width = thumb_meta.get("width")
                    if thumb_meta.has("height"): height = thumb_meta.get("height")
            
            await client.send_video(
                chat_id=message.chat.id,
                video=video_file,
                thumb=thumb,
                caption="**Downloaded via @SocialMediaX_dlbot**",
                duration=duration,
                width=width,
                height=height,
                supports_streaming=True,
                reply_to_message_id=message.id,
                reply_markup=markup,
                progress=progress,
                progress_args=(status, c_time, "Uploading Video...")
            )
            
        # 4. IF NO VIDEO, FALLBACK TO IMAGE (pin module):
        else:
            await status.edit_text("📸 **Extracting Image...**")
            pin_dl = importlib.import_module("pin")
            await asyncio.to_thread(
                pin_dl.run_library_main,
                url, task_dir, 0, -1, False, False, False, False, False, True, False, False, None, None, None
            )
            
            image_file = None
            for file in os.listdir(task_dir):
                if file.endswith(".jpg"):
                    image_file = os.path.join(task_dir, file)
                    break
                    
            if image_file:
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=image_file,
                    caption="**Here is your 🔴⚪Pinterest⚪🔴 video! 🎬\n\n©️ @SocialMediaX_dlbot\n🔥🤖 @XBOTS_X",
                    reply_to_message_id=message.id,
                    reply_markup=markup,
                    progress=progress,
                    progress_args=(status, c_time, "Uploading Image...")
                )
            else:
                await status.edit_text("❌ **Failed:** Could not extract a video or image from this link.")
                return

        # Delete processing message after success
        await status.delete()

    except Exception as e:
        await status.edit_text(f"❌ Failed to process: `{e}`")
        
    finally:
        # 5. Clean up the unique temporary folder to save server space
        if os.path.exists(task_dir):
            shutil.rmtree(task_dir)
