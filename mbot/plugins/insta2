from pyrogram import filters
import bs4, requests,re,asyncio
import os,traceback,random
from mbot import LOG_GROUP as DUMP_GROUP
from mbot import Mbot, LOG_GROUP
from config import LOG_CHANNEL
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
#    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "99",
    "Origin": "https://saveig.app",
    "Connection": "keep-alive",
    "Referer": "https://saveig.app/en",
}

IG = """
📤📱 **LOG ALERT** 💻📱
➖➖➖➖➖➖➖➖➖➖➖
📛**Instagram link** : [click here]({})
👤**Name** : {}
👾**Username** : @{}
💾**DC** : {}
♐**ID** : `{}`
🤖**BOT** : @SocialMediaX_dlbot
➖➖➖➖➖➖➖➖➖➖
#ig #instagram
"""


#https://saveig.app/api/ajaxSearch
@Mbot.on_message(filters.regex(r'https?://.*instagram[^\s]+') & filters.incoming)
async def link_idl(Mbot, message):
    link = message.matches[0].group(0)
    gg = await Mbot.send_message(LOG_CHANNEL, IG.format(link, message.from_user.mention, message.from_user.username, message.from_user.dc_id, message.from_user.id))
    Igbutton = InlineKeyboardMarkup(
                     [
                         [
                             InlineKeyboardButton('Open on Instagram', url=f'{link}')
                         ]
                     ]
               )
    global headers
    try:
        m = await message.reply_text("__Your Request is Processing...\nPlease Wait__")
        url= link.replace("instagram.com","ddinstagram.com")
        url=url.replace("==","%3D%3D")
        if url.endswith("="):
           dump_file=await message.reply_video(url[:-1],caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=Igbutton)
        else:
            dump_file=await message.reply_video(url,caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=Igbutton)
        if 'dump_file' in locals():
           await dump_file.forward(DUMP_GROUP)
        await m.delete()
    except Exception as e:
        try:
            if "/reel/" in url:
               ddinsta=True 
               getdata = requests.get(url).text
               soup = bs4.BeautifulSoup(getdata, 'html.parser')
               meta_tag = soup.find('meta', attrs={'property': 'og:video'})
               try:
                  content_value =f"https://ddinstagram.com{meta_tag['content']}"
               except:
                   pass 
               if not meta_tag:
                  ddinsta=False
                  meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"}, headers=headers)
             
                  if meta_tag.ok:
                     res=meta_tag.json()
               
                #     await message.reply(res)
                     meta=re.findall(r'href="(https?://[^"]+)"', res['data']) 
                     content_value = meta[0]
                  else:
                      return await message.reply("oops something went wrong")
               try:
                   if ddinsta:
                      dump_file=await message.reply_video(content_value, caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=Igbutton)
                   else:
                       dump_file=await message.reply_video(content_value, caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=Igbutton)
               except:
                   downfile=f"{os.getcwd()}/{random.randint(1,10000000)}"
                   with open(downfile,'wb') as x:
                       headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                       x.write(requests.get(content_value,headers=headers).content)
                   dump_file=await message.reply_video(downfile,caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=Igbutton) 
            elif "/p/" in url:
                  meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"}, headers=headers)
                  if meta_tag.ok:
                     res=meta_tag.json()
                     meta=re.findall(r'href="(https?://[^"]+)"', res['data']) 
                  else:
                      return await message.reply("oops something went wrong")
              #    await message.reply(meta)
                  for i in range(len(meta) - 1):
                     com=await message.reply_text(meta[i])
                     await asyncio.sleep(1)
                     try:
                        dump_file=await message.reply_video(com.text, caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=Igbutton)
                        await com.delete()
                     except:
                         pass 
            elif "stories" in url:
                  meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"}, headers=headers)
                  if meta_tag.ok:
                     res=meta_tag.json()
                     meta=re.findall(r'href="(https?://[^"]+)"', res['data']) 
                  else:
                      return await message.reply("Oops something went wrong")
                  try:
                     dump_file=await message.reply_video(meta[0], caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=Igbutton)
                  except:
                      com=await message.reply(meta[0])
                      await asyncio.sleep(1)
                      try:
                          dump_file=await message.reply_video(com.text, caption="**Downloaded via @SocialMediaX_dlbot**", reply_markup=Igbutton)
                          await com.delete()
                      except:
                          pass

        except KeyError:
            await message.reply(f"400: Sorry, Unable To Find It Make Sure Its Publically Available :)")
        except Exception as e:
          #  await message.reply_text(f"https://ddinstagram.com{content_value}")
            if LOG_GROUP:
               await Mbot.send_message(LOG_GROUP,f"Instagram {e} {link}")
               await Mbot.send_message(LOG_GROUP, traceback.format_exc())
          #     await message.reply(tracemsg)
            ##optinal 
            await message.reply(f"400: Sorry, Unable To Find It  try another or report it  to @xyz")

        finally:
            if 'dump_file' in locals():
               if DUMP_GROUP:
                  await dump_file.copy(DUMP_GROUP)
            await m.delete()
            if 'downfile' in locals():
                os.remove(downfile)
