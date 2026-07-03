import logging
import time
from typing import List
from pyrogram import Client
from config import Config

# Track container boot timestamps for diagnostics
START_TIME = time.time()

# Advanced Structured Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("mbot.core")

# Fail-Fast Validation: Prevents broken/empty session deployments on cloud services
missing_configs: List[str] = [
    key for key in ["API_ID", "API_HASH", "BOT_TOKEN"] 
    if not getattr(Config, key, None)
]

if missing_configs:
    logger.critical(f"❌ Initialization halted. Missing requirements: {', '.join(missing_configs)}")
    raise ValueError(f"Environment injection failure for attributes: {missing_configs}")

# Optimized MTProto client instance
app = Client(
    name="mbot_session",
    api_id=int(Config.API_ID),
    api_hash=str(Config.API_HASH),
    bot_token=str(Config.BOT_TOKEN),
    plugins=dict(root="mbot/plugins"),
    workers=min(32, getattr(Config, "WORKERS", 16))  # Dynamic thread tuning for handling concurrency
)

__all__ = ["app", "logger", "START_TIME"]
