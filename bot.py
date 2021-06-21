#    This file is part of the ChannelAutoForwarder distribution (https://github.com/xditya/ChannelAutoForwarder).
#    Copyright (c) 2021 Adiya
#    
#    This program is free software: you can redistribute it and/or modify  
#    it under the terms of the GNU General Public License as published by  
#    the Free Software Foundation, version 3.
# 
#    This program is distributed in the hope that it will be useful, but 
#    WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
#    General Public License for more details.
# 
#    License can be found in < https://github.com/xditya/ChannelAutoForwarder/blob/main/License> .

import logging
import asyncio
from telethon import TelegramClient, events, Button
from decouple import config
from telethon.tl.functions.users import GetFullUserRequest

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

# start the bot
print("Starting...")
try:
    apiid = config("APP_ID", cast=int)
    apihash = config("API_HASH")
    bottoken = config("BOT_TOKEN")
    frm = config("FROM_CHANNEL", cast=int)
    tochnl = config("TO_CHANNEL", cast=int)
    datgbot = TelegramClient('bot', apiid, apihash).start(bot_token=bottoken)
except:
    print("Environment vars are missing! Kindly recheck.")
    print("Bot is quiting...")
    exit()


@datgbot.on(events.NewMessage(pattern="/start"))
async def _(event):
    ok = await datgbot(GetFullUserRequest(event.sender_id))
    await event.reply(f"Hi `{ok.user.first_name}`!\n\nI am a channel auto-post bot!! Read /help to know more!\n\nI can be used in only two channels (one user) at a time. Kindly deploy your own bot.\n\n[More bots](https://t.me/its_xditya)..", buttons=[Button.url("Repo", url="https://github.com/xditya/ChannelAutoForwarder"), Button.url("Dev", url="https://t.me/its_xditya")], link_preview=False)


@datgbot.on(events.NewMessage(pattern="/help"))
async def helpp(event):
    await event.reply("**Help**\n\nThis bot will send all new posts in one channel to the other channel. (without forwarded tag)!\nIt can be used only in two channels at a time, so kindly deploy your own bot from [here](https://github.com/xditya/ChannelAutoForwarder).\n\nAdd me to both the channels and make me an admin in both, and all new messages would be autoposted on the linked channel!!\n\nLiked the bot? Drop a ♥ to @xditya_Bot :)")

@datgbot.on(events.NewMessage(incoming=True, chats=frm)) 
async def _(event): 
    if not event.is_private:
        try:
            if event.poll:
                return
            if event.photo:
                photo = event.media.photo
                await datgbot.send_file(tochnl, photo, caption = event.text, link_preview = False)
            elif event.media:
                try:
                    if event.media.webpage:
                        await datgbot.send_message(tochnl, event.text, link_preview = False)
                        return
                except:
                    media = event.media.document
                    await datgbot.send_file(tochnl, media, caption = event.text, link_preview = False)
                    return
            else:
                await datgbot.send_message(tochnl, event.text, link_preview = False)
        except:
            print("TO_CHANNEL ID is wrong or I can't send messages there (make me admin).")


print("Bot has started.")
print("Do visit @its_xditya..")
datgbot.run_until_disconnected()
