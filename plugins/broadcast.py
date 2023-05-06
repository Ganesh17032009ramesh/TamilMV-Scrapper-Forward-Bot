from pyrogram import Client ,filters
import os
from helper.database import getid
ADMIN = int(os.environ.get("ADMIN", 1391556668))


@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
 if (message.reply_to_message):
   ms = await message.reply_text("**Geting All IDs From Database...**")
   ids = getid()
   tot = len(ids)
   await ms.edit(f"**Completed Broadcast 💌\n Sending Message To {tot} Users**")
   for id in ids:
     try:
     	await message.reply_to_message.copy(id)
     except:
     	pass
