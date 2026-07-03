import logging

from pyrogram import Client
from vgx_config import Config

from pyrogram.types import BotCommand


# 1. Advanced Logging (Silences the harmless 'wakeup fd' spam)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.CRITICAL) 
logger = logging.getLogger("mbot")

# 2. Enterprise-Grade Bot Class
class AdvancedBot(Client):
    def __init__(self):
        super().__init__(
            name="mbot_session",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="mbot.plugins"), # Auto-loads command files
            workers=16
        )

    async def start(self):
        """Executes safely on the correct event loop when the bot boots."""
        await super().start()
        
        me = await self.get_me()
        logger.info(f"✅ Bot initialized successfully: @{me.username} (ID: {me.id})")
        
        # Dynamically set Telegram menu commands
        try:
            await self.set_bot_commands([
                BotCommand("start", "Wake up the bot"),
                BotCommand("ffmpeg", "Run an advanced FFmpeg test")
            ])
            logger.info("✅ Bot menu commands registered.")
        except Exception as e:
            logger.error(f"⚠️ Could not set menu commands: {e}")

    async def stop(self, *args):
        """Executes safely when Koyeb shuts down the container, preventing database corruption."""
        logger.info("🛑 Termination signal received. Cleaning up background tasks...")
        await super().stop()
        logger.info("👋 Network connections closed cleanly.")

# 3. Instantiate the app so it can be imported safely
app = AdvancedBot()
