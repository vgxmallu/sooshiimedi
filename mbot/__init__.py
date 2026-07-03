
import logging
import asyncio
import os
from pyrogram import Client
from pyrogram.types import BotCommand
from vgx_config import Config

# Advanced Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.CRITICAL) 
logger = logging.getLogger("mbot")

class AdvancedBot(Client):
    def __init__(self):
        super().__init__(
            name="mbot_session",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="mbot.plugins"),
            workers=16
        )
        self._health_server = None

    async def _health_handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Responds to Koyeb's network probes to prove the container is alive."""
        try:
            writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 2\r\n\r\nOK")
            await writer.drain()
        except Exception:
            pass
        finally:
            writer.close()

    async def start(self):
        """Executes safely on the native event loop when the bot boots."""
        await super().start()
        
        # Bind a lightweight background ping responder on the port Koyeb checks
        port = int(os.environ.get("PORT", 8080))
        try:
            self._health_server = await asyncio.start_server(self._health_handler, "0.0.0.0", port)
            logger.info(f"🌐 Internal health check server active on port {port}")
        except Exception as e:
            logger.warning(f"⚠️ Could not bind health check server: {e}")
        
        me = await self.get_me()
        logger.info(f"✅ Bot initialized successfully: @{me.username} (ID: {me.id})")
        
        try:
            await self.set_bot_commands([
                BotCommand("start", "Wake up the bot"),
                BotCommand("ffmpeg", "Run an advanced FFmpeg test")
            ])
            logger.info("✅ Bot menu commands registered.")
        except Exception as e:
            logger.error(f"⚠️ Could not set menu commands: {e}")

    async def stop(self, *args):
        """Gracefully releases resources when the container intercepts termination events."""
        logger.info("🛑 Termination signal received. Cleaning up background tasks...")
        
        if self._health_server:
            self._health_server.close()
            await self._health_server.wait_closed()
            logger.info("🌐 Health check server stopped.")
            
        await super().stop()
        logger.info("👋 Network connections closed cleanly.")

app = AdvancedBot()
