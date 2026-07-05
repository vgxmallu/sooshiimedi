import os
import traceback
import logging
import random
import asyncio
import pytz, datetime
import time 

from pyrogram import filters, StopPropagation

from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
#from pyrogram.errors import UserNotParticipant
from config import LOG_CHANNEL, AUTH_USERS, DB_URL, DB_NAME, PICS
#from pyrogram.types import Message
from handlers.broadcast import broadcast
from handlers.check_user import handle_user_status
from handlers.database import Database
from mbot import app #botStartTime
#from mbot.utils.upt import get_readable_time
#from mbot.utils.tm import ISTIME
#from random import choice



db = Database(DB_URL, DB_NAME)

#f_sub = "songdownload_group"
#photo = f"https://telegra.ph/file/fcd069fccdcf4d74eb5fb.jpg"

#x = ["❤️", "💛", "💚", "🤍", "💙", "💜", "🖤", "♏", "💟", "♥️", "🎧", "💝", "💖", "💞", "❤️‍🔥", "💋"]
#g = random.choice(x)

#h = ["Hi", "Hello", "Hey", "Hey there!", "Hola", "Greetings!", "Namaste!", "Ciao!"]
#hy = random.choice(h)




SRT_TXT = """
👋 Hey there {}!, My name is Social media x dlbot. 

I am your all-in-one tool for extracting high-quality videos, photos, and audio directly to Telegram.

**Supported Platforms:**
📸 **Instagram** (Reels, Posts)
🐦 **X / Twitter** (Videos & Images)
🎵 **TikTok** (Watermark-free)
▶️ **YouTube** (Shorts & Videos)
📘 **Facebook** (Videos & Reels)
📌 **Pinterest** (Pins & vids)

__💡 **Pro Tips:**
• The post or account **must be public**.
• Send only one link at a time.
• No commands needed—just paste the link!

🚀 **Drop a link below to start downloading!**.__
"""
SRT_BTN = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('🔮 Channel', url='https://t.me/XBots_X'),
            ],[
                InlineKeyboardButton("🔥 Help Module", callback_data="hlp"),
                InlineKeyboardButton("👾 About me.", callback_data="ab"),
                InlineKeyboardButton('🎮 Game Bot', url='https://t.me/GomezGamesbot')
            ],[
                InlineKeyboardButton("🗑️ Clear", callback_data="close"),
            ]
        ]
   )

ms_stt = """
Some times bot will be slow, because of Server Overload :(
"""
CMD = ["/", ".", "?", "#", "+", "mg"]


@app.on_message(filters.command("alive", CMD))
async def check_alive(_, message):
    await message.reply_text("ചത്തിട്ടില്ല മുത്തേ ഇവിടെ തന്നെ ഉണ്ട്.. നിനക്ക് ഇപ്പൊ എന്നോട് ഒരു സ്നേഹവും ഇല്ല. കൊള്ളാം.. നീ പാഴെ പോലെയേ അല്ല മാറിപോയി..😔 ഇടക്ക് എങ്കിലും ചുമ്മാ ഒന്ന് /start ചെയ്തു നോക്ക്..🙂")


MS = """
‼️ **STARTRD ALERT** ‼️

📛**Triggered Command** : /start
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @SocialMediaX_dlbot
"""

@app.on_message(filters.private)
async def _(bot, cmd):
    await handle_user_status(bot, cmd)
@app.on_message(filters.command(["start", "help"]))
async def start_command(bot, message):
    chat_id = message.from_user.id
    if not await db.is_user_exist(chat_id):
        data = await client.get_me()
        await db.add_user(chat_id)
        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"🥳NEWUSER🥳 \n\n😼New User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) 😹started @spotifysavetgbot !!",
            )
        else:
            logging.info(f"🥳NewUser🥳 :- 😼Name : {message.from_user.first_name} 😹ID : {message.from_user.id}")
    #joinButton = InlineKeyboardMarkup(
    #    [
    #        [
    #            InlineKeyboardButton('🎵My Group', url='https://t.me/songdownload_group'),
    #            InlineKeyboardButton('❌', callback_data='close')
    #        ]
    #    ]
    #)
    #await message.reply_sticker("CAACAgIAAxkBAAI2QGSWpA9Dzy892oJ24g4dHTSJiNiaAAIoIAACJaYJS-FqCk576-FVHgQ")
    #uptime = get_readable_time(time.time() - botStartTime)
    await bot.send_message(LOG_CHANNEL, MS.format(message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
    await message.reply_photo(
        photo=random.choice(PICS), 
        caption=SRT_TXT.format(message.from_user.mention),
        reply_markup=SRT_BTN,
    )
    await message.delete()
    ab = await message.reply_text(ms_stt)
    a = await message.reply_sticker("CAACAgQAAxkBAAECc_Rlr_DBTtAoTZswcpeTEUozhUBwWAACugsAAtM56FC9TQABc2BqXEEeBA")
    await asyncio.sleep(60)
    await ab.delete()
    await asyncio.sleep(3600)
    await message.reply_text("/start me later 😌🫰🏼.")
    
    


#=======CALLBACK==================
@app.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "srt":
        await update.message.edit_text(
            text=SRT_TXT.format(update.from_user.first_name),
            reply_markup=SRT_BTN,
            disable_web_page_preview=True
        )
        await update.answer("🌲❄️")
        
    elif update.data == "hlp":
        await update.message.edit_text(
            text=HLP_TXT,
            reply_markup=HLP_BTN,
            disable_web_page_preview=True
        )
        await update.answer("Your in my Help Module🆘")
        
#=======
    elif update.data == "fb":
        await update.message.edit_text(
            text=FBDL_TXT,
            reply_markup=FBDL_BTN,
            disable_web_page_preview=True
        )
        await update.answer("🔵FACEBOOK DOWNLOAD⚪")

    elif update.data == "ig":
        await update.message.edit_text(
            text=IGDL_TXT,
            reply_markup=IGDL_BTN,
            disable_web_page_preview=True
        )
        await update.answer("🟣INSTAGRAM DOWNLOAD🟡")

    
    elif update.data == "yt":
        await update.message.edit_text(
            text=YT_TXT,
            reply_markup=YT_BTN,
            disable_web_page_preview=True
        )
        await update.answer("🔴YOUTUBE DOWNLOAD⚪")

    elif update.data == "tt":
        await update.message.edit_text(
            text=TTDL_TXT,
            reply_markup=TTDL_BTN,
            disable_web_page_preview=True
        )
        await update.answer("⚫TIKTOK DOWNLOAD⚪")

    elif update.data == "tw":
        await update.message.edit_text(
            text=TWDL_TXT,
            reply_markup=TWDL_BTN,
            disable_web_page_preview=True
        )
        await update.answer("⚫TWITTER [X] DOWNLOAD⚫")

    elif update.data == "pin":
        await update.message.edit_text(
            text=PINDL_TXT,
            reply_markup=PINDL_BTN,
            disable_web_page_preview=True
        )
        await update.answer("🔴PINTEREST DOWNLOAD⚫")
#========
    elif update.data == "ab":
        await update.message.edit_text(
            text=AB_TXT,
            reply_markup=AB_BTN,
            disable_web_page_preview=True
        )
        await update.answer("My About ℹ️")
        
    elif update.data == "close":
        await update.message.delete()
        await update.answer("Successfully Closed ❌")
        
    elif update.data == "exa":
        await update.answer("More music Request:\n➻ You can download songs by sending the Youtube, Spotify, SoundCloud, Deezer links to the group. It helps to get the proper song.\nThank you, I hope you understand. 😊", show_alert=True)
    elif update.data == "emt":
        await update.answer("Why, its empty man😹")
    elif update.data == "hmm":
        await update.answer("😌")
    elif update.data == "done":
        await update.answer("Your Music has been successfully Uploaded.✅\nThank you for using me💖", show_alert=True) 
            
    elif update.data == "soon":
        await update.answer("Soon...", show_alert=True) 

    #else:
        #await update.message.delete()

#=========CALLBACK========
HLP_TXT = """
Here is my Help Buttons 🔘📥

©️ @SocialMediaX_dlbot
🔥: @XBOTS_X
"""
HLP_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🔵Facebook🔵', callback_data='fb')
        ],[
        InlineKeyboardButton("🟣Instagram🟣", callback_data="ig")
        ],[
        InlineKeyboardButton('⚫Twitter⚫', callback_data='tw')
        ],[
        InlineKeyboardButton('⚫⚪TikTok⚫⚪', callback_data='tt')
        ],[
        InlineKeyboardButton("🔴⚪Pinterest⚪🔴", callback_data="pin")
        ],[
        InlineKeyboardButton('🔴YouTube🔴', callback_data='yt')
        ],[
        InlineKeyboardButton('⬅️Back', callback_data='srt')
        ],[
        InlineKeyboardButton("🗑️Clear", callback_data="close")
        ]]
   )


YT_TXT = """
Help for 🔴**YouTube**🔴 Videos downloads.

Send **Youtube** videO Link in Chat to Download videos.

©️: @XBOTS_X
"""
YT_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️", callback_data="hlp"), 
        InlineKeyboardButton("❌", callback_data="close"),
        InlineKeyboardButton("🏠", callback_data="srt")
        ]]
   )
FBDL_TXT = """
Help for 🔵**Facebook**🔵 Videos/Reels downloads.

Copy & Paste the Facebook direct Video/reels link here.

©️: @XBOTS_X
"""
FBDL_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️", callback_data="hlp"), 
        InlineKeyboardButton("❌", callback_data="close"),
        InlineKeyboardButton("🏠", callback_data="srt")
        ]]
   )
IGDL_TXT = """
Help for 🟣**Instagram**🟣 Video/Reels downloads.

Copy & Paste your Instagram video/reels/photos link here,

why can't download Storys and photo's can't send because of
Photos/Stories: Are highly protected. Instagram requires a logged-in session (cookies) to generate the secure keys needed to view and download photo files.

©️: @XBOTS_X
"""
IGDL_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️", callback_data="hlp"), 
        InlineKeyboardButton("❌", callback_data="close"),
        InlineKeyboardButton("🏠", callback_data="srt")
        ]]
   )


TTDL_TXT = """
Help for ⚪⚫**TikTok** Reels downloads.

Copy & Paste your TikTok Reels links here,

©️: @XBOTS_X
"""
TTDL_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️", callback_data="hlp"), 
        InlineKeyboardButton("❌", callback_data="close"),
        InlineKeyboardButton("🏠", callback_data="srt")
        ]]
   )

TWDL_TXT = """
Help for ⚫**Twitter**⚫ Videos/gifs/photos downloads.

Copy & Paste your Twitter videos links here,

©️: @XBOTS_X
"""
TWDL_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️", callback_data="hlp"), 
        InlineKeyboardButton("❌", callback_data="close"),
        InlineKeyboardButton("🏠", callback_data="srt")
        ]]
   )

PINDL_TXT = """
Help for **Pinterest** Videos/Photos Downloads..

Copy & Paste your Pinterest videos links here, i will download for you.

©️: @XBOTS_X
"""
PINDL_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("⬅️", callback_data="hlp"), 
        InlineKeyboardButton("❌", callback_data="close"),
        InlineKeyboardButton("🏠", callback_data="srt")
        ]]
    )

AB_TXT = """
__About Me__
 
🤖 **Name** : [SocialMedia•𝕏•Dlbot](https://t.me/SocialMediaX_dlbot)

📝 **Language** : [Python3](https://python.org)
 × **Python version** : `3.10.11l`
 
📚 **Library** : [Pyrogram](https://pyrogram.org)
 × **Pyrogram version** : `2.0.73`
 
📡 **Hosted On** : [Digital Ocean 🌊](https://www.digitalocean.com)

📋 **License** : [MIT](https://choosealicense.com/licenses/mit/)

©️ **@SocialMediaX_dlbot**
🔥: @XBOTS_X
"""
AB_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⬅️ Back', callback_data='srt'),
        InlineKeyboardButton('🗑️ Clear', callback_data='close')
        ]]
    )

#==================•BROADCAST•==================
@app.on_message(filters.private & filters.command("broadcast", CMD))
async def broadcast_handler_open(_, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if m.reply_to_message is None:
        await m.delete()
    else:
        await broadcast(m, db)

@app.on_message(filters.private & filters.command("stats", CMD))
async def sts(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    sat = await m.reply_text(
        text=f"**Total Users in Database 📂:** `{await db.total_users_count()}`\n\n**Total Users with Notification Enabled 🔔 :** `{await db.total_notif_users_count()}`",
        quote=True
    )
    await m.delete()
    await asyncio.sleep(180)
    await sat.delete()

@app.on_message(filters.private & filters.command("ban_user", CMD))
async def ban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban 🛑 any user from the bot 🤖.\n\nUsage:\n\n`/ban_user user_id ban_duration ban_reason`\n\nEg: `/ban_user 1234567 28 You misused me.`\n This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = " ".join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."

        try:
            await c.send_message(
                user_id,
                f"You are Banned 🚫 to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n**Message from the admin 🤠**",
            )
            ban_log_text += "\n\nUser notified successfully!"
        except BaseException:
            traceback.print_exc()
            ban_log_text += (
                f"\n\n ⚠️ User notification failed! ⚠️ \n\n`{traceback.format_exc()}`"
            )
        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(ban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured ⚠️! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )

@app.on_message(filters.private & filters.command("unban_user", CMD))
async def unban(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban 😃 any user.\n\nUsage:\n\n`/unban_user user_id`\n\nEg: `/unban_user 1234567`\n This will unban user with id `1234567`.",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user 🤪 {user_id}"

        try:
            await c.send_message(user_id, f"Your ban was lifted!")
            unban_log_text += "\n\n✅ User notified successfully! ✅"
        except BaseException:
            traceback.print_exc()
            unban_log_text += (
                f"\n\n⚠️ User notification failed! ⚠️\n\n`{traceback.format_exc()}`"
            )
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(unban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"⚠️ Error occoured ⚠️! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True,
        )

@app.on_message(filters.private & filters.command("banned_users", CMD))
async def banned_usrs(c, m):
    if m.from_user.id not in AUTH_USERS:
        await m.delete()
        return
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ""
    async for banned_user in all_banned_users:
        user_id = banned_user["id"]
        ban_duration = banned_user["ban_status"]["ban_duration"]
        banned_on = banned_user["ban_status"]["banned_on"]
        ban_reason = banned_user["ban_status"]["ban_reason"]
        banned_usr_count += 1
        text += f"> **User_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, **Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s) 🤭: `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open("banned-users.txt", "w") as f:
            f.write(reply_text)
        await m.reply_document("banned-users.txt", True)
        os.remove("banned-users.txt")
        return
    await m.reply_text(reply_text, True)
