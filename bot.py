from pyrogram import Client, __version__, idle
import re, os, time
from datetime import datetime
from pytz import timezone
from pyrogram.raw.all import layer
from aiohttp import web
from route import web_server
import pyromod
from plugins.core.rss_feed import tamilmv_rss_feed, tamilblasters_rss_feed, TAMILBLAST_LOG, TAMILMV_LOG
import pyrogram.utils
from plugins.core.bypass_checker import app as Client2

pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

id_pattern = re.compile(r'^.\d+$') 

BOT_TOKEN = os.environ.get("TOKEN", "6502200200:AAExzSPuFw8H4nIjDUHOj3RG8aZv1fZdpoM")
API_ID = int(os.environ.get("API_ID", 11973721))
API_HASH = os.environ.get("API_HASH", "5264bf4663e9159565603522f58d3c18")
BOT_UPTIME = time.time()
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001821439025"))
WEBHOOK = bool(os.environ.get("WEBHOOK", True))
ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1391556668 1242556540').split()]
STRING_SESSION = os.environ.get("STRING_SESSION", "1BVtsOKEBu5Pf_Oesjuxt4TIzNijt1iMjJ8hEa3xtURQFrsd0GFYLhS_XFm2iJ61NfFeKR5icfMSu_SWH3eRvvdZ-X7IyOVFZuQ4sHKoiju_WXCH4uQqqd7vB7_9hGyMbDk7mUgjVKNkRg0trupt-5mu8pAeWAZ3US61kBnLKvsMYSjiaiL3uWI3UDfzyNQzFhf_hXWF_XskD0QrMPS87wEd85iNzXBgBE9Sae2haJ8YppGWxhcGtmJDSqHnDSlxh2dFLBZ1K_o7zxE6i1FrOaqEL_gKW87xqc2W43kCsUj-s9A9GyXdP7aUxu1Mku5j3GyMxEWS79Yku7AfxyeGUYhTw5dXGScE=")

Bot = Client(
    "1TamilMVScrapper",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins=dict(root="plugins"),
)

async def start_bot(clients):
    """Start the bots and run the RSS scraping tasks."""
    for client in clients:
        await client.start()
        print(f"{client.name} Started!")
        for chat in [TAMILMV_LOG, TAMILBLAST_LOG]:
            await client.send_message(chat, "**Bot Started!**")
    while True:
        print("TamilMV RSS Feed Running...")
        await tamilmv_rss_feed(Bot)
        time.sleep(60)

        print("TamilBlasters RSS Feed Running...")
        await tamilblasters_rss_feed(Bot)
        time.sleep(60)

async def stop_bot(clients):
    """Stop the bots."""
    for client in clients:
        await client.stop()
        print(f"{client.name} Stopped!")

if STRING_SESSION:
    # Include both Bot and Client2
    async def main():
        clients = [Bot, Client2]
        try:
            await start_bot(clients)
        except KeyboardInterrupt:
            await stop_bot(clients)
    Bot.start()
    Client2.start()
    idle()
    Bot.stop()
    Client2.stop()
else:
    Bot.run()
    
