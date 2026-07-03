import logging
import time
from typing import List
from pyrogram import Client
from vgx_config import Config

app = Client(
    "mbot_session",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="mbot/plugins")
)
