import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("convert"))
async def convert_video(client: Client, message: Message):
    # Let the user know the process started
    msg = await message.reply_text("Processing video with FFmpeg...")

    input_file = "input.mp4"
    output_file = "output.mkv"

    # Run FFmpeg asynchronously (This DOES NOT freeze the bot)
    process = await asyncio.create_subprocess_exec(
        "ffmpeg", 
        "-i", input_file, 
        "-c:v", "copy", 
        "-c:a", "copy", 
        output_file,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Wait for FFmpeg to finish its job
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        await msg.edit_text("✅ FFmpeg finished successfully!")
        # Now you can send the output_file back to the user
    else:
        await msg.edit_text("❌ FFmpeg encountered an error.")
        print(f"FFmpeg Error: {stderr.decode()}")
