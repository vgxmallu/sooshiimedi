from os import mkdir
from random import randint
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from mbot import LOG_GROUP, AUTH_CHATS, LOGGER, Mbot
from mbot.utils.ytdl import audio_opt, getIds, thumb_down, ytdl_down
from config import LOG_CHANNEL
#from youtube_search import YoutubeSearch
YT = """
📤📱 **LOG ALERT** 💻📱
➖➖➖➖➖➖➖➖➖➖➖
📛**YouTube link** : [click here]({})
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @SocialMediaX_dlbot
➖➖➖➖➖➖➖➖➖➖
#youtube
"""

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


@Mbot.on_message(
    filters.private
    & filters.regex(r"(https?://)?.*you[^\s]+") & filters.incoming
    | filters.command(["yt", "ytd", "ytmusic"])
    & filters.regex(r"https?://.*you[^\s]+")
    & filters.chat(AUTH_CHATS)
)
async def _(c, message):
    link = message.matches[0].group(0)
    m = await message.reply_text("__Your Request is Processing.\nPlease Wait...__")
    gg = await c.send_message(LOG_CHANNEL, YT.format(link, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
    n = await message.reply_chat_action(enums.ChatAction.TYPING)
    #results = YoutubeSearch(link, max_results=1).to_dict()
    #duration = results[0]["duration"]
    #if time_to_seconds(duration) >= 3600:  # duration limit #900 #600 10minut, 2400 40m, 3600 1h
    #    await message.reply_text("❗This won't be downloaded because its Video length is longer than the limit\nSend videos less than 1 hours.")
    #    return
    if link in [
        "https://youtube.com/",
        "https://youtube.com",
        "https://youtu.be/",
        "https://youtu.be",
    ]:
        return await m.edit_text("Please send a valid playlist or video link.")
    elif "channel" in link or "/c/" in link:
        return await m.edit_text("**Channel** Download Not Available. ")
    try:
        ids = await getIds(message.matches[0].group(0))
        
        videoInPlaylist = len(ids)
        randomdir = "/tmp/" + str(randint(1, 100000000))
        mkdir(randomdir)
        for id in ids:
            #PForCopy = await message.reply_photo(
             #   f"https://i.ytimg.com/vi/{id[0]}/hqdefault.jpg",
              #  caption=f"🎧 **Title**: `{id[3]}`\n👤 **Artist**: `{id[2]}`\n🔗 **Link**: [Click here](https://youtu.be/{id[0]})\n🔢 **Tracks**: `{id[1]}`/`{videoInPlaylist}`",
            #)
            ytbutton = InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton('Open on YouTube', url=f'https://youtu.be/{id[0]}')
                   ]
               ]
            )
            
            fileLink = await ytdl_down(audio_opt(randomdir, id[2]), id[0])
            thumnail = await thumb_down(id[0])
            dForChat = await message.reply_chat_action(enums.ChatAction.UPLOAD_VIDEO)
            AForCopy = await message.reply_video(
                fileLink,
                duration=id[4],
                thumb=thumnail,
                caption=f"📹 {id[3]}/{id[2]}\nTracks: [`{id[1]}/{videoInPlaylist}`]\n\n**Downloaded via @SocialMediaX_dlbot**",
                reply_markup=ytbutton,
            )
            #feedback = await message.reply_text(f"Done ✅",   
            # reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="✅ Done", callback_data="done")]]))
            if LOG_GROUP:
                await AForCopy.copy(LOG_GROUP)
            
        await m.delete()
    except Exception as e:
        LOGGER.error(e)
        await m.edit_text(e)
