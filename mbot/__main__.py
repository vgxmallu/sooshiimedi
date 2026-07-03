from mbot import app

if __name__ == "__main__":
    # app.run() handles 100% of the async loops automatically.
    # No asyncio.run(), no idle(), no loop crashes!
    app.run()
