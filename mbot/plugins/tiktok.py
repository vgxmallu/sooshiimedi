from pyrogram import filters
import bs4, requests,re,asyncio
import wget,os,traceback
from mbot import LOG_GROUP as DUMP_GROUP
from mbot import Mbot, LOG_GROUP
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import LOG_CHANNEL
TT = """
📤📱 **LOG ALERT** 💻📱
➖➖➖➖➖➖➖➖➖➖➖
📛**TikTok link** : [click here]({})
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @SocialMediaX_dlbot
➖➖➖➖➖➖➖➖➖➖
#TikTok
"""
@Mbot.on_message(filters.regex(r'https?://.*tiktok[^\s]+') & filters.incoming)
async def link_handler(Mbot, message):
    link = message.matches[0].group(0)
    gg = await Mbot.send_message(LOG_CHANNEL, TT.format(link, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
    ttbutton = InlineKeyboardMarkup(
                     [
                         [
                             InlineKeyboardButton('Open on TikTok', url=f'{link}')
                         ]
                     ]
               )
    try:
        m = await message.reply_text("__Your Request is Processing.\nPlease Wait.__")
        get_api= requests.post("https://lovetik.com/api/ajax/search",data={"query":link}).json()
        if get_api['status'] and "Invalid TikTok video url" in get_api['mess']: 
           return await message.reply("Oops Invalid TikTok video url. Please try again :) ")
        if get_api.get('links'):
           try:
              if "MP3" in get_api['links'][0]['t']:
                 try:
                     await message.reply_photo(get_api['cover'])
                 except:
                     pass 
              dump_file = await message.reply_video(get_api['links'][0]['a'], caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=ttbutton)
           except KeyError:
               return await message.reply("Invalid TikTok video url. Please try again.")
           except Exception:
               snd_msg=await message.reply(get_api['links'][0]['a'])
               await asyncio.sleep(1)
               try:
                  dump_file = await message.reply_video(get_api['links'][0]['a'],caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=ttbutton)
                  await snd_msg.delete()
               except Exception:
                   pass
    except Exception as e:      
        if LOG_GROUP:
               await Mbot.send_message(LOG_GROUP,f"TikTok {e} {link}")
               await Mbot.send_message(LOG_GROUP, traceback.format_exc())          
    finally:
        if 'dump_file' in locals():
            if DUMP_GROUP:
               await dump_file.copy(DUMP_GROUP)
            await m.delete()
