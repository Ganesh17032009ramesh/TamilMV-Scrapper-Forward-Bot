from pyrogram import Client, __version__, idle
import re, os, time
from datetime import datetime
from pytz import timezone
from pyrogram.raw.all import layer
from aiohttp import web
from route import web_server
import pyromod
import pyrogram.utils
from plugins.core.bypass_checker import app as Client2

pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

id_pattern = re.compile(r'^.\d+$') 

BOT_TOKEN = os.environ.get("TOKEN", "7713324413:AAGYzSbK5Z9KbhaJGiQdA7Rs-YaYLk4fNiU")
API_ID = int(os.environ.get("API_ID",11973721))
API_HASH = os.environ.get("API_HASH", "5264bf4663e9159565603522f58d3c18")
BOT_UPTIME  = time.time()
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001821439025"))
WEBHOOK = bool(os.environ.get("WEBHOOK", True))
ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1391556668 1242556540').split()]
STRING_SESSION = os.environ.get("STRING_SESSION", "1BVtsOKEBu5Pf_Oesjuxt4TIzNijt1iMjJ8hEa3xtURQFrsd0GFYLhS_XFm2iJ61NfFeKR5icfMSu_SWH3eRvvdZ-X7IyOVFZuQ4sHKoiju_WXCH4uQqqd7vB7_9hGyMbDk7mUgjVKNkRg0trupt-5mu8pAeWAZ3US61kBnLKvsMYSjiaiL3uWI3UDfzyNQzFhf_hXWF_XskD0QrMPS87wEd85iNzXBgBE9Sae2haJ8YppGWxhcGtmJDSqHnDSlxh2dFLBZ1K_o7zxE6i1FrOaqEL_gKW87xqc2W43kCsUj-s9A9GyXdP7aUxu1Mku5j3GyMxEWS79Yku7AfxyeGUYhTw5dXGScE=")

Bot = Client("1TamilMVScrapper", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root='plugins'))

# Flag to control running status
running = True

async def start(self):
    global running
        apps = [Client2, self]
        for app in apps:
            app.start()
        idle()
        for app in apps:
            app.stop()
    await super().start()
    print("Bot Started!")

    # Notify in log channels
    for chat in [LOG_CHANNEL, Config.TAMILMV_LOG, Config.TAMILBLAST_LOG, Config.GROUP_ID]:
        await self.send_message(chat, "Bot Started!")
        await Client2.send_message(chat, "Bot Started For Auto Leech")

    # Start the scraper loop
    while running:
        try:
            print("TamilMV RSS Feed Running...")
            await tamilmv_rss_feed(self)

            print("TamilBlasters RSS Feed Running...")
            await tamilblasters_rss_feed(self)

            print("TamilMV RSS Feed Running for Group...")
            await tamilmv_rss_feed_user(Client2)

            print("TamilBlasters RSS Feed Running for Group...")
            await tamilblasters_rss_feed_user(Client2)

            print("Sleeping for 5 minutes...")
            await asyncio.sleep(300)
        except Exception as e:
            print(f"Error: {e}")
            await self.send_message(LOG_CHANNEL, f"Error occurred: {str(e)}")
            await asyncio.sleep(60)

    print("Bot Stopped!")
    for chat in [LOG_CHANNEL]:
        await self.send_message(chat, "Bot Stopped!")
        
