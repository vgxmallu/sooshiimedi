import logging

from pyrogram import Client
from vgx_config import Config




app = Client(
    "VGXBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=100,
    sleep_threshold=30,
    plugins=dict(root="mbot.plugins")
)
