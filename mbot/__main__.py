from pyrogram import idle
from mbot import app

if __name__ == "__main__":
    app.start()

    print("🚀 Bot Started! Send /schedule")
    idle()
    app.stop()
