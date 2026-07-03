import traceback

async def safe_task(coro):

    try:
        await coro

    except Exception:
        traceback.print_exc()
