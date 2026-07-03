import asyncio

from pyrogram import idle

from mbot import app
from ultis.logger import logger
from ultis.ffmpeg import check_ffmpeg
from ultis.folders import create_folders


async def startup():

    logger.info("🚀 Starting Bot...")

    create_folders()

    check_ffmpeg()

    await app.start()

    me = await app.get_me()

    logger.info(f"Logged in as @{me.username}")

    logger.info("✅ Bot Started Successfully")


async def shutdown():

    logger.info("Stopping Bot...")

    await app.stop()

    logger.info("Bot Stopped")


async def main():

    await startup()

    await idle()

    await shutdown()


if __name__ == "__main__":
    asyncio.run(main())
