from pyrogram import idle
from mbot import app

async def main():
    await app.start()
    print("🟢🟢BOT IS RUNNING!🟢🟢")
    await idle()
    await app.stop()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
