import asyncio
import platform
import sys
import signal
import time
from typing import Any, Dict
from pyrogram import idle
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats
from mbot import app, logger, START_TIME

def global_exception_handler(loop: asyncio.AbstractEventLoop, context: Dict[str, Any]) -> None:
    """Intercepts and logs rogue asynchronous task crashes to avoid silent context dropping."""
    err_msg = context.get("exception", context["message"])
    logger.error(f"🚨 Unhandled exception caught in async thread: {err_msg}", exc_info=context.get("exception"))

async def set_bot_commands() -> None:
    """Registers contextual, localized menu paths optimized for privacy."""
    try:
        private_commands = [
            BotCommand("start", "🚀 Initialize the interface status"),
            BotCommand("help", "📖 Review manual and command directory"),
            BotCommand("settings", "⚙️ Manage download options"),
            BotCommand("status", "📊 Query server engine analytics")
        ]
        # Restricts options layout strictly to Private Chats (DM) to avoid channel/group clutter
        await app.set_bot_commands(private_commands, scope=BotCommandScopeAllPrivateChats())
        logger.info("✅ Contextual API commands verified and bound.")
    except Exception as e:
        logger.error(f"Failed to push navigation command mappings: {e}", exc_info=True)

async def start_services() -> None:
    """Runs structural handshake operations and tracks hardware environment stats."""
    logger.info(f"System Context: {platform.system()} {platform.release()} ({platform.machine()})")
    logger.info(f"Language Layer: Python v{platform.python_version()} [{platform.architecture()[0]}]")
    
    logger.info("Connecting socket pipelines to Telegram Data Centers...")
    await app.start()
    
    bot_identity = await app.get_me()
    logger.info(f"🛡️ Security Matrix Clear: @{bot_identity.username} [{bot_identity.id}] online.")
    
    await set_bot_commands()

async def shutdown_services() -> None:
    """Executes a clean exit cascade to release locked memory blocks and files."""
    logger.info("Termination signal caught. Releasing active operational layers...")
    
    # Safely clear dangling background processing tasks (downloads, uploads, network requests)
    active_runtime_task = asyncio.current_task()
    pending_tasks = [t for t in asyncio.all_tasks() if t is not active_runtime_task]
    
    if pending_tasks:
        logger.info(f"Terminating {len(pending_tasks)} lingering background routines safely...")
        for job in pending_tasks:
            job.cancel()
        await asyncio.gather(*pending_tasks, return_exceptions=True)
        
    if app.is_connected:
        logger.info("Dropping MTProto network protocols safely...")
        await app.stop()
        logger.info("🔌 Database session lock disengaged.")

async def main() -> None:
    """Application lifetime orchestrator."""
    runtime_loop = asyncio.get_running_loop()
    runtime_loop.set_exception_handler(global_exception_handler)

    # Listen directly for Koyeb's container management kill signals (SIGTERM)
    if sys.platform != 'win32':
        for sig_type in (signal.SIGINT, signal.SIGTERM):
            runtime_loop.add_signal_handler(
                sig_type,
                lambda: asyncio.create_task(shutdown_services()).add_done_callback(lambda _: sys.exit(0))
            )

    try:
        await start_services()
        logger.info(f"🔥 Application running loop reached in {(time.time() - START_TIME):.2f}s. Listening for updates...")
        await idle()
        
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as system_fault:
        logger.critical(f"💥 Boot process fatal breakdown: {system_fault}", exc_info=True)
        sys.exit(1)
    finally:
        if sys.platform == 'win32':
            await shutdown_services()
        logger.info("🚀 Main process execution thread stopped. Exit status: 0")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Process forced kill signal processed via console.")
