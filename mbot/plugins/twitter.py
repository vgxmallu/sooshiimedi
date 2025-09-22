from pyrogram import filters
from mbot import LOG_GROUP as DUMP_GROUP
from mbot import Mbot, LOG_GROUP
import os,re,asyncio,bs4
import requests,wget,traceback
from bs4 import BeautifulSoup
from config import LOG_CHANNEL
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
TW = """
📤📱 **LOG ALERT** 💻📱
➖➖➖➖➖➖➖➖➖➖➖
📛**Twitter link** : [click here]({})
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @SocialMediaX_dlbot
➖➖➖➖➖➖➖➖➖➖
#Twitter
"""
@Mbot.on_message(filters.regex(r'https?://.*twitter[^\s]+') & filters.incoming | filters.regex(r'https?://(?:www\.)?x\.com/\S+') & filters.incoming,group=-5)
async def twitter_handler(Mbot, message):
   try:            
      link=message.matches[0].group(0)
      if "x.com" in link:
         link=link.replace("x.com","fxtwitter.com")
      elif "twitter.com" in link:
         link = link.replace("twitter.com","fxtwitter.com")
      m = await message.reply_text("__Your Request is Processing.\nPlease Wait.__")
      gg = await Mbot.send_message(LOG_CHANNEL, TW.format(link, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
      twbutton = InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton('Open on Twitter', url=f'{link}')
                   ]
               ]
         )
      try:
          dump_file = await message.reply_video(link, caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=twbutton)
      except Exception as e:
          print(e)
          try:
             snd_message=await message.reply(link)
             await asyncio.sleep(1)
             dump_file = await message.reply_video(link, caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=twbutton)
             await snd_message.delete()
          except Exception as e:
              print(e)
              await snd_message.delete()
              get_api=requests.get(link).text
              soup=bs4.BeautifulSoup(get_api,"html.parser")
              meta_tag= soup.find("meta", attrs = {"property": "og:video"})
              if not meta_tag:
                  meta_tag = soup.find("meta", attrs={"property": "og:image"})
              content_value  = meta_tag['content']
              try:
                  dump_file = await message.reply_video(content_value, caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=twbutton)
              except Exception as e:
                  print(e)
                  try:
                     snd_msg=await message.reply(content_value)
                     await asyncio.sleep(1)
                     await message.reply_video(content_value,caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=twbutton)
                     await snd_msg.delete()
                  except Exception as e:
                      print(e)
                      await message.reply("Oops Invalid link or Use this command to download,\nExample: [/twdl your link here.]")
   except Exception as e:
        print(e)
        if LOG_GROUP:
           await Mbot.send_message(LOG_GROUP,e)
           await Mbot.send_message(LOG_GROUP,traceback.format_exc())
   finally:
       if DUMP_GROUP:
          if "dump_file" in locals():
             await dump_file.copy(DUMP_GROUP)
       await m.delete()
