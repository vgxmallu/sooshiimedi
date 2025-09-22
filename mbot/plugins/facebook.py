from pyrogram import filters
import bs4, requests,re,asyncio
import wget,os,traceback
from mbot import LOG_GROUP as DUMP_GROUP, Mbot
from mbot import LOG_GROUP
from config import LOG_CHANNEL
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

FB = """
📤📱 **LOG ALERT** 💻📱
➖➖➖➖➖➖➖➖➖➖➖
📛**Facebook link** : [click here]({})
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @SocialMediaX_dlbot
➖➖➖➖➖➖➖➖➖➖
#facebook
"""
@Mbot.on_message(filters.regex(r'https?://.*facebook[^\s]+') | filters.regex(r'https?://.*fb[^\s]+') & filters.incoming,group=-6)
async def link_handler(Mbot, message):
    link = message.matches[0].group(0)
    gg = await Mbot.send_message(LOG_CHANNEL, FB.format(link, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
    fbbutton = InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton('Open on Facebook', url=f'{link}')
                   ]
               ]
          )
    try:
       m = await message.reply_text("__Your Request is Processing.\nPlease Wait...__")
       get_api=requests.get(f"https://yasirapi.eu.org/fbdl?link={link}").json()
       if get_api['success'] == "false":
          return await message.reply("Invalid Facebook video url. Please try again :)")
       if get_api['success'] == "ok":
          if get_api.get('result').get('hd'):
             try:
                 dump_file = await message.reply_video(get_api['result']['hd'], caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=fbbutton)
             except KeyError:
                 pass 
             except Exception:
                 try:
                     sndmsg = await message.reply(get_api['result']['hd'])
                     await asyncio.sleep(1)
                     dump_file = await message.reply_video(get_api['result']['hd'], caption="**Downloaded via @SocialMediaX_dlbot", reply_markup=fbbutton)
                     await sndmsg.delete()
                 except Exception:
                     try:
                        down_file = wget.download(get_api['result']['hd'])
                        await message.reply_video(down_file, caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=fbbutton)
                        await sndmsg.delete()
                        os.remove(down_file)
                     except:
                         return await message.reply("Oops Failed To Send File Instead Of Link")
          else: 
             if get_api.get('result').get('sd'):
               try:
                   dump_file = await message.reply_video(get_api['result']['sd'], caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=fbbutton)
               except KeyError:
                   pass
               except Exception:
                   try:
                       sndmsg = await message.reply(get_api['result']['sd'])
                       await asyncio.sleep(1)
                       dump_file = await message.reply_video(get_api['result']['sd'], caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=fbbutton)
                       await sndmsg.delete()
                   except Exception:
                      try:
                        down_file = wget.download(get_api['result']['sd'])
                        await message.reply_video(down_file, caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=fbbutton)
                        await sndmsg.delete()
                        os.remove(down_file)
                      except:
                         return await message.reply("`Oops Failed To Send File Instead Of Link`")
    except Exception as e:
           if LOG_GROUP:
               await Mbot.send_message(LOG_GROUP,f"Facebook {e} {link}")
               await Mbot.send_message(LOG_GROUP, traceback.format_exc())          
    finally:
          if 'dump_file' in locals():
            if DUMP_GROUP:
               await dump_file.copy(DUMP_GROUP)
          await m.delete()      
