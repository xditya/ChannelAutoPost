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
from telethon.sessions import StringSession
from decouple import config
from telethon.tl.functions.users import GetFullUserRequest

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

# start the bot
print("Starting...")
try:
    apiid = config("APP_ID", cast=int)
    apihash = config("API_HASH")
    frm = config("FROM_CHANNEL", cast=int)
    tochnl = config("TO_CHANNEL", cast=int)
except:
    print("Environment vars are missing! Kindly recheck.")
    print("Bot is quiting...")
    exit()

bottoken = config("BOT_TOKEN", default=None)
if bottoken:
    try:
        BotzHub = TelegramClient('bot', apiid, apihash).start(bot_token=bottoken)
    except Exception as e:
        print(str(e))
        exit(0)

session = config("SESSION", default=None)
if session:
    try:
        BotzHubUser = TelegramClient(StringSession(session), apiid, apihash)
        BotzHubUser.start()
    except Exception as ap:
        print(f"ERROR - {ap}")
        exit(1)

@BotzHub.on(events.NewMessage(pattern="/start"))
async def _(event):
    ok = await BotzHub(GetFullUserRequest(event.sender_id))
    await event.reply(f"Hi `{ok.user.first_name}`!\n\nI am a channel auto-post bot!! Read /help to know more!\n\nI can be used in only two channels (one user) at a time. Kindly deploy your own bot.\n\n[More bots](https://t.me/its_xditya)..", buttons=[Button.url("Repo", url="https://github.com/xditya/ChannelAutoForwarder"), Button.url("Dev", url="https://t.me/its_xditya")], link_preview=False)


@BotzHub.on(events.NewMessage(pattern="/help"))
async def helpp(event):
    await event.reply("**Help**\n\nThis bot will send all new posts in one channel to the other channel. (without forwarded tag)!\nIt can be used only in two channels at a time, so kindly deploy your own bot from [here](https://github.com/xditya/ChannelAutoForwarder).\n\nAdd me to both the channels and make me an admin in both, and all new messages would be autoposted on the linked channel!!\n\nLiked the bot? Drop a ♥ to @xditya_Bot :)", link_preview=False)


if session:
    @BotzHubUser.on(events.NewMessage(incoming=True, chats=frm))    # use the user client.
    async def _(event): 
        if not event.is_private:
            try:
                await BotzHubUser.send_message(tochnl, event.message)   # make the user send the message.
            except Exception as e:
                print(f"TO_CHANNEL ID is wrong or I can't send messages there (make me admin).\n\nERROR - {str(e)}")
else:
    @BotzHub.on(events.NewMessage(incoming=True, chats=frm))    # the bot is to be used here.
    async def _(event): 
        if not event.is_private:
            try:
                await BotzHub.send_message(tochnl, event.message)   # the bot sends the message.
            except Exception as e:
                print(f"TO_CHANNEL ID is wrong or I can't send messages there (make me admin).\n\nERROR - {str(e)}")


print("Bot has started.")
print("Do visit @BotzHub..")
BotzHub.run_until_disconnected()