from pyrogram import Client, filters
from pyrogram.types import Message
import logging
import asyncio
from datetime import datetime
from pyrogram.enums import ChatMemberStatus
from dotenv import load_dotenv
from os import environ
import os
import time

from handlers.status import format_progress_bar
from handlers.video import download_video, upload_video
from mbot import Mbot as app


dump_id = os.environ.get('CHAT_ID', '-1001939311530')

@app.on_message(filters.private & filters.regex(r'https?://.*teraboxlink[^\s]+') | filters.private & filters.regex(r'https?://.*1024terabox[^\s]+') | filters.private & filters.regex(r'https?://.*freeterabox[^\s]+') | filters.private & filters.regex(r'https?://.*terabox.fun[^\s]+') | filters.private & filters.regex(r'https?://.*terabox.com[^\s]+') | filters.private & filters.regex(r'https?://.*4funbox[^\s]+') | filters.private & filters.regex(r'https?://.*tibibox[^\s]+') | filters.private & filters.regex(r'https?://.*mirrobox[^\s]+'))
async def handle_message(client, message: Message):
    user_id = message.from_user.id
    user_mention = message.from_user.mention
    #is_member = await is_user_member(client, user_id)
    terabox_link = message.matches[0].group(0)
    #terabox_link = message.text.strip()
    if "terabox" not in terabox_link:
        await message.reply_text("please send me valid terabox link.")
        return

    reply_msg = await message.reply_text("Sending media please wait...")

    try:
        file_path, thumbnail_path, video_title = await download_video(terabox_link, reply_msg, user_mention, user_id)
        await upload_video(client, file_path, thumbnail_path, video_title, reply_msg, dump_id, user_mention, user_id, message)
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        await reply_msg.edit_text("Failed to download.")

