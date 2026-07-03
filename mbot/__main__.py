import logging
from pyrogram import idle
from mbot import app, logger

# Suppress the harmless "signal wakeup fd" error
logging.getLogger("asyncio").setLevel(logging.CRITICAL)

async def main():
    logger.info("Starting bot services...")
    
    # We do NOT need to call await app.start() here! 
    # Pyrogram does it automatically before running this function.
    
    bot_info = await app.get_me()
    logger.info(f"✅ Bot is online: @{bot_info.username}")
    
    # Keep the bot running and listening for messages
    await idle()
    
    logger.info("Shutdown signal received. Cleaning up active tasks...")
    # We do NOT need to call await app.stop() here!
    # Pyrogram will automatically stop the bot safely when this function ends.

if __name__ == "__main__":
    # Let Pyrogram's built-in engine handle the event loop safely
    app.run(main())

