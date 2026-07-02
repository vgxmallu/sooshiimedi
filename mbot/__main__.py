import logging
from pyrogram import Client
from mbot import app

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
