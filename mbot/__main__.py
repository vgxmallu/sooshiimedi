import logging
from pyrogram import Client
from mbot.__init__ import app
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import Config

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Initialize Scheduler
scheduler = AsyncIOScheduler()
# Setup Logging

async def main():
    # Start the scheduler
    scheduler.start()
    
    # Start the bot
    async with app:
        logging.info("Bot is running...")
        # Keep the bot running
        await Client.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
