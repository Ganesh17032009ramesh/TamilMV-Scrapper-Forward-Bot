import os
from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pyrogram.types import InlineQuery
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from plugins.db import u_db

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

# first source commands
@Client.on_message(filters.command("set_channels") & filters.user(OWNER_ID))
async def set_channels(client, message):
    try:
        # Extract the command parameters
        command_parts = message.text.split(" ", 3)  # Split into 4 parts: command, sources, destination, text
        if len(command_parts) != 4:
            await message.reply("Usage: /set_channels <source_channels(comma-separated)> <destination_channel> <original_text>:<new_text>")
            return

        # Extract source channels, destination channel, and replacement text
        source_channels = list(map(int, command_parts[1].split(",")))  # Comma-separated sources
        destination_channel = int(command_parts[2])
        replace_parts = command_parts[3].split(":")  # Extract original and new text (e.g., /ql:/ql1)
        if len(replace_parts) != 2:
            await message.reply("Text replacement must be in the format: <original_text>:<new_text>")
            return

        original_text, new_text = replace_parts

        # Add channels to the database
        for source_channel in source_channels:
            await u_db.add_channel(source_channel, destination_channel)

        # Replace text in messages (using replace_text)
        modified_count = 0
        for source_channel in source_channels:
            modified_count += await u_db.replace_text(
                collection_name="Messages",
                filter_query={"source_channel": source_channel},
                old_text=original_text,
                new_text=new_text,
            )

        # Store replacement details in the database
        replacement_data = {
            "source_channels": source_channels,
            "destination_channel": destination_channel,
            "original_text": original_text,
            "new_text": new_text,
            "replaced_count": modified_count,
            "timestamp": datetime.datetime.now(),
        }
        await u_db.add_channel("ReplacementData", replacement_data)

        await message.reply(
            f"Channels added successfully: Sources: {', '.join(map(str, source_channels))}, "
            f"Destination: {destination_channel}\n"
            f"Text replacement complete: {modified_count} messages updated."
        )
    except Exception as e:
        await message.reply(f"Failed to add channels or replace text: {str(e)}")

@Client.on_message(filters.command("get_channels"))
async def get_channels(client, message):
    try:
        # Retrieve all source-destination channel pairs
        channels = await u_db.get_all_channels()

        # Prepare response for the channels and replace text details
        response = "Source-Destination Channels:\n"
        for channel in channels:
            source_channel = channel["source_channel"]
            destination_channel = channel["destination_channel"]
            
            # Fetch replacement details for the source channel
            replacement_log = await u_db.replacement_data.find_one({"source_channel": source_channel})
            
            if replacement_log:
                # If there's replacement data, include it in the response
                original_text = replacement_log["original_text"]
                new_text = replacement_log["new_text"]
                replaced_count = replacement_log["replaced_count"]
                replace_info = f" (Replaced '{original_text}' with '{new_text}' in {replaced_count} messages)"
            else:
                replace_info = " (No replacements)"

            # Append the channel and replacement details to the response
            response += f"Source Channel: {source_channel}, Destination Channel: {destination_channel}{replace_info}\n"

        # Send the response
        await message.reply(response)

    except Exception as e:
        await message.reply(f"Failed to retrieve channels or replacement data: {str(e)}")

# second source commands 
@Client.on_message(filters.command("set_channels2") & filters.user(OWNER_ID))
async def set_channels(client, message):
    try:
        # Extract the command parameters
        command_parts = message.text.split(" ", 3)  # Split into 4 parts: command, sources, destination, text
        if len(command_parts) != 4:
            await message.reply("Usage: /set_channels2 <source_channels(comma-separated)> <destination_channel> <original_text>:<new_text>")
            return

        # Extract source channels, destination channel, and replacement text
        source_channels = list(map(int, command_parts[1].split(",")))  # Comma-separated sources
        destination_channel = int(command_parts[2])
        replace_parts = command_parts[3].split(":")  # Extract original and new text (e.g., /ql:/ql1)
        if len(replace_parts) != 2:
            await message.reply("Text replacement must be in the format: <original_text>:<new_text>")
            return

        original_text, new_text = replace_parts

        # Add channels to the database
        for source_channel in source_channels:
            await u_db.add_channel_tb(source_channel, destination_channel)

        # Replace text in messages (using replace_text)
        modified_count = 0
        for source_channel in source_channels:
            modified_count += await u_db.replace_text_tb(
                collection_name="Messages",
                filter_query={"source_channel": source_channel},
                old_text=original_text,
                new_text=new_text,
            )

        # Store replacement details in the database
        replacement_data = {
            "source_channels": source_channels,
            "destination_channel": destination_channel,
            "original_text": original_text,
            "new_text": new_text,
            "replaced_count": modified_count,
            "timestamp": datetime.datetime.now(),
        }
        await u_db.add_channel_tb("ReplacementData", replacement_data)

        await message.reply(
            f"Channels added successfully: Sources: {', '.join(map(str, source_channels))}, "
            f"Destination: {destination_channel}\n"
            f"Text replacement complete: {modified_count} messages updated."
        )
    except Exception as e:
        await message.reply(f"Failed to add channels or replace text: {str(e)}")

@Client.on_message(filters.command("get_channels2"))
async def get_channels(client, message):
    try:
        # Retrieve all source-destination channel pairs
        channels = await u_db.get_all_channels_tb()

        # Prepare response for the channels and replace text details
        response = "Source-Destination Channels:\n"
        for channel in channels:
            source_channel = channel["source_channel"]
            destination_channel = channel["destination_channel"]
            
            # Fetch replacement details for the source channel
            replacement_log = await u_db.replacement_data_tb.find_one({"source_channel": source_channel})
            
            if replacement_log:
                # If there's replacement data, include it in the response
                original_text = replacement_log["original_text"]
                new_text = replacement_log["new_text"]
                replaced_count = replacement_log["replaced_count"]
                replace_info = f" (Replaced '{original_text}' with '{new_text}' in {replaced_count} messages)"
            else:
                replace_info = " (No replacements)"

            # Append the channel and replacement details to the response
            response += f"Source Channel: {source_channel}, Destination Channel: {destination_channel}{replace_info}\n"

        # Send the response
        await message.reply(response)

    except Exception as e:
        await message.reply(f"Failed to retrieve channels or replacement data: {str(e)}")
        
