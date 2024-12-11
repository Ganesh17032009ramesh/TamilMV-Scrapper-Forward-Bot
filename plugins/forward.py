from pyrogram import enums
import os, asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ.get("API_ID",11973721))
API_HASH = os.environ.get("API_HASH", "5264bf4663e9159565603522f58d3c18")
STRING_SESSION = os.environ.get("STRING_SESSION", "1BVtsOKEBu5Pf_Oesjuxt4TIzNijt1iMjJ8hEa3xtURQFrsd0GFYLhS_XFm2iJ61NfFeKR5icfMSu_SWH3eRvvdZ-X7IyOVFZuQ4sHKoiju_WXCH4uQqqd7vB7_9hGyMbDk7mUgjVKNkRg0trupt-5mu8pAeWAZ3US61kBnLKvsMYSjiaiL3uWI3UDfzyNQzFhf_hXWF_XskD0QrMPS87wEd85iNzXBgBE9Sae2haJ8YppGWxhcGtmJDSqHnDSlxh2dFLBZ1K_o7zxE6i1FrOaqEL_gKW87xqc2W43kCsUj-s9A9GyXdP7aUxu1Mku5j3GyMxEWS79Yku7AfxyeGUYhTw5dXGScE=")
#SOURCE_CHANNELS = list(
#    map(int, os.environ.get("SOURCE_CHANNELS", "-1001822541447 -1002056074553 -1001864825324").split(" "))
#)
SOURCE_CHANNEL = int(os.environ.get("SOURCE_CHANNEL", -1001864825324))
SOURCE_CHANNEL_1 = int(os.environ.get("SOURCE_CHANNEL_1", -1001822541447))
SOURCE_CHANNEL_2 = int(os.environ.get("SOURCE_CHANNEL_2", -100182254848494847))
DESTINATION_CHANNEL = int(os.environ.get("DESTINATION_CHANNEL", -1001542301808))
DESTINATION_CHANNEL_1 = int(os.environ.get("DESTINATION_CHANNEL_1", -1001542301808))
DESTINATION_CHANNEL_2 = int(os.environ.get("DESTINATION_CHANNEL_2", -1001542301808))

app = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH).start()

@app.on(events.NewMessage)
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

@app.on(events.NewMessage(chats=SOURCE_CHANNEL))  # Listen to multiple source channels
async def forward_message(event):
    try:
        await asyncio.sleep(300)
        if event.message.media:  # If the message has media
            await event.client.send_message(DESTINATION_CHANNEL, event.message)
        else:  # If the message is text-only
            await event.client.send_message(DESTINATION_CHANNEL, event.message.text)
    except Exception as e:
        print(f"Failed to forward the message: {str(e)}")
        
@app.on(events.NewMessage(chats=SOURCE_CHANNEL_1))  # Listen to multiple source channels
async def forward_message(event):
    try:
        await asyncio.sleep(300)
        if event.message.media:
            await event.client.send_message(DESTINATION_CHANNEL_1, event.message)
        else:  # If the message is text-only
            modified_text = event.message.text.replace("/qbleech", "/qbleech1")
            await event.client.send_message(DESTINATION_CHANNEL_1, modified_text)
    except Exception as e:
        print(f"Failed to forward the message: {str(e)}")

@app.on(events.NewMessage(chats=SOURCE_CHANNEL_2))  # Listen to multiple source channels
async def forward_message(event):
    try:
        await asyncio.sleep(300)
        if event.message.media:
            await event.client.send_message(DESTINATION_CHANNEL_2, event.message)
        else:  # If the message is text-only
            modified_text = event.message.text.replace("/qbleech", "/qbleech2")
            await event.client.send_message(DESTINATION_CHANNEL_2, modified_text)
    except Exception as e:
        print(f"Failed to forward the message: {str(e)}")
