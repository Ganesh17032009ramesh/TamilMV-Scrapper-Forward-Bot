from pyrogram import enums
import os, asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import PeerChannel

API_ID = int(os.environ.get("API_ID",11973721))
API_HASH = os.environ.get("API_HASH", "5264bf4663e9159565603522f58d3c18")
STRING_SESSION = os.environ.get("STRING_SESSION", "1BVtsOKEBu5Pf_Oesjuxt4TIzNijt1iMjJ8hEa3xtURQFrsd0GFYLhS_XFm2iJ61NfFeKR5icfMSu_SWH3eRvvdZ-X7IyOVFZuQ4sHKoiju_WXCH4uQqqd7vB7_9hGyMbDk7mUgjVKNkRg0trupt-5mu8pAeWAZ3US61kBnLKvsMYSjiaiL3uWI3UDfzyNQzFhf_hXWF_XskD0QrMPS87wEd85iNzXBgBE9Sae2haJ8YppGWxhcGtmJDSqHnDSlxh2dFLBZ1K_o7zxE6i1FrOaqEL_gKW87xqc2W43kCsUj-s9A9GyXdP7aUxu1Mku5j3GyMxEWS79Yku7AfxyeGUYhTw5dXGScE=")
#SOURCE_CHANNELS = list(
#    map(int, os.environ.get("SOURCE_CHANNELS", "-1001822541447 -1002056074553 -1001864825324").split(" "))
#)

app = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH).start()

@app.on(events.NewMessage)
async def forward_message(event):
    try:
        # Get the source channel ID (where the message is coming from)
        source_channel_id = event.chat_id

        # Retrieve the destination channel based on the source channel from the database
        channel_data = await u_db.channels.find_one({"source_channel": source_channel_id})
        
        if not channel_data:
            # If there's no mapping for this source channel, return
            print(f"No destination channel found for source channel {source_channel_id}")
            return
        
        destination_channel_id = channel_data["destination_channel"]
        
        # Fetch replacement data from the ReplacementData collection for the source channel
        replacement_log = await u_db.replacement_data.find_one({"source_channel": source_channel_id})

        if replacement_log:
            # If replacement data exists, perform the text replacement
            original_text = replacement_log["original_text"]
            new_text = replacement_log["new_text"]

            # If the message contains the original text, replace it with the new text
            if event.message.text and original_text in event.message.text:
                updated_message = event.message.text.replace(original_text, new_text)
            else:
                updated_message = event.message.text
        else:
            # If no replacement data, proceed with the original message
            updated_message = event.message.text

        # Forward the updated message to the destination channel
        if updated_message:
            # Forward text messages
            await app.send_message(destination_channel_id, updated_message)
        elif event.message.media:
            # Forward media messages (e.g., photos, videos, etc.)
            await app.forward_messages(destination_channel_id, event.message)

        print(f"Message forwarded from source channel {source_channel_id} to destination channel {destination_channel_id}")
    
    except Exception as e:
        print(f"Error forwarding message: {e}")
