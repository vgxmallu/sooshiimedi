from pyrogram import Client
#from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import BOT_TOKEN, API_HASH, API_ID
import logging
#from pyrogram.types import BotCommand

# Setup Logging
logging.basicConfig(level=logging.INFO)
# Initialize Scheduler
#scheduler = AsyncIOScheduler()




# Initialize Bot
app = Client(
    "scheduler_bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="mbot") # Automatically loads files in plugins/
)
