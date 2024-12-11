import os
from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram.types import InlineQuery
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from plugins.core.db import u_db

OWNER_ID = int(os.environ.get("OWNER_ID", 1391556668))

@Client.on_message(filters.private & filters.command(['start']))
async def start(query: InlineQuery, message):
          await message.reply_text(text =f"<b>Hello 👋🏻 {message.from_user.first_name} ❤️\n\nI'm Star Bots Official 1TamilMV Scrapper Bot. I Can Bypass any Movie to You Sent 1TamilMV Link. You Can Sent Torrent Links and Magnet Links Seperately to Your Channel/Group.\n\nTo know How to Use me check /help.\n\nI'll Work in Inline Anywhere.</b>",reply_to_message_id = message.id, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(            [                [                    InlineKeyboardButton("🤖 Bot Channel" ,url="https://t.me/Star_Bots_Tamil"),InlineKeyboardButton("Go Inline Here",switch_inline_query_current_chat='')],                 [InlineKeyboardButton("🎥 Movie Updates", url="https://t.me/Star_Moviess_Tamil"),InlineKeyboardButton("👥 Support Group",url = "https://t.me/Star_Bots_Tamil_Support") ]           ]        ) )
  
@Client.on_message(filters.private & filters.command(['help']))
async def help(client, message):
          await message.reply_text(text =f"<b>Hey 👋🏻 {message.from_user.first_name} Follow These Steps :-\n\n● Send /bypass to 1TamilMV website Movies\n● /auto_leech to Send Torrent Links 🌐 to Leeching Group\n● /send_torrents to Send Torrent Links 🌐 to Channel\n● /send_magnets to Send Magnet Links 🧲 to Channel\n\nAvailable Commands\n\n● /start - Check if 😊 I'm Alive\n● /help - How to Use❓\n● /about - to Know About Me 😌\n\nMade by <a href=https://t.me/Star_Bots_Tamil><b></b>Star Bots Tamil</a></b>",reply_to_message_id = message.id , disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(            [                [                    InlineKeyboardButton("🤖 Bot Channel" ,url="https://t.me/Star_Bots_Tamil") ],                 [InlineKeyboardButton("🎥 Movie Updates", url="https://t.me/Star_Moviess_Tamil"),InlineKeyboardButton("👥 Support Group",url = "https://t.me/Star_Bots_Tamil_Support") ]           ]        ) )

@Client.on_message(filters.private & filters.command(['about']))
async def about(client, message):
          await message.reply_text(text =f"<b>🤖 My Name :- <a href=https://t.me/TamilMV_Scrapper_Bot><b>1TamilMV Scrapper Bot</b></a>\n\n🧑🏻‍💻 Developer :- <a href=https://t.me/U_Karthik><b>Karthik</b></a>\n\n📝 Language :- Python3\n\n📚 Framework :- Pyrogram\n\n📡 Hosted on :- VPS\n\n🤖 Bot Channel :- <a href=https://t.me/Star_Bots_Tamil><b>Star Bots Tamil</b></a>\n\n🎥 Movie Updates :- <a href=https://t.me/Star_Moviess_Tamil><b>Star Movies Tamil</b></a></b>",reply_to_message_id = message.id, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(            [                [                    InlineKeyboardButton("🤖 Bot Channel" ,url="https://t.me/Star_Bots_Tamil") ],                 [InlineKeyboardButton("🎥 Movie Updates", url="https://t.me/Star_Moviess_Tamil"),InlineKeyboardButton("👥 Support Group",url = "https://t.me/Star_Bots_Tamil_Support") ]           ]        ) )

@Client.on_message(filters.command("links") & filters.private)
async def links(c: Client, m: Message):
    ''' Start Message of the Bot !!'''

    await m.reply_text(
        text='''
<b>🔰 Hello, I am TamilMVAutoRss and Multi-Tasking Bot! 🔰</b>

<b>Get All RSS Feed Channel Links</b>''',
        quote=True,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("1TamilMV", url="https://t.me/+3rd6z7uhqTxiYWM1")],
            [InlineKeyboardButton("1TamilBlasters", url="https://t.me/+cFk95Ozi_RA2MGE1")],
            [InlineKeyboardButton("2TamilRockers", url="https://t.me/+Un9tkoLZVz41NDk1")]
        ])
    )
    
@app.on_message(filters.command("add_channels"))
async def add_channels_command(client, message):
    try:
        # Extract the source and destination channels from the command
        command_parts = message.text.split(" ")
        if len(command_parts) != 3:
            await message.reply("Usage: /add_channels <source_channel> <destination_channel>")
            return

        source_channel = int(command_parts[1])
        destination_channel = int(command_parts[2])

        # Add channels to the database
        await u_db.add_channel(source_channel, destination_channel)
        await message.reply(f"Channels added: Source: {source_channel}, Destination: {destination_channel}")
    except Exception as e:
        await message.reply(f"Failed to add channels: {str(e)}")

# Forwarding Message Function for Telethon Client (using Telethon Events)
@telethon_app.on(events.NewMessage)
async def forward_message(event):
    try:
        # Fetch the channel mappings from the database
        channels = await u_db.get_all_channels()
        
        # Check for each channel mapping and forward the message
        for channel in channels:
            if event.chat_id == channel['source_channel']:
                # Delay the message forwarding
                await asyncio.sleep(300)  # Wait for 5 minutes

                # Forward the message to the destination channel
                if event.message.media:
                    await event.client.send_message(channel['destination_channel'], event.message)
                else:  # If it's a text-only message
                    modified_text = event.message.text.replace("/qbleech", "/qbleech1")  # Modify text if necessary
                    await event.client.send_message(channel['destination_channel'], modified_text)
                break
    except Exception as e:
        print(f"Failed to forward message: {str(e)}")
