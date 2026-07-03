import logging

from pyrogram import Client
from vgx_config import Config



# Setup clean logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mbot")

# Initialize the bot
app = Client(
    name="mbot_session",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="mbot.plugins"), # Uses dot-notation for safer importing
    workers=16
)
