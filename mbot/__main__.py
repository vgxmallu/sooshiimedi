import asyncio
import logging
from pyrogram import idle
from mbot import app, logger

# 1. Suppress the harmless "signal wakeup fd" error from Python's async engine
logging.getLogger("asyncio").setLevel(logging.CRITICAL)

async def main():
    logger.info("Starting bot services...")
    
    # 2. Start the Pyrogram client
    await app.start()
    
    bot_info = await app.get_me()
    logger.info(f"✅ Bot is online: @{bot_info.username}")
    
    try:
        # 3. Keep the bot running
        await idle()
    except KeyboardInterrupt:
        logger.warning("Bot stopped manually.")
    finally:
        # 4. Graceful shutdown to prevent session file corruption on Koyeb
        logger.info("Cleaning up active tasks...")
        if app.is_connected:
            await app.stop()
        logger.info("Shutdown complete.")

if __name__ == "__main__":
    # 5. The standard, modern way to run an async Python app
    asyncio.run(main())
