from pyrogram import Client, __version__, idle
import re, os, time
from datetime import datetime
from pytz import timezone
from pyrogram.raw.all import layer
from aiohttp import web
from route import web_server
import pyromod
import pyrogram.utils
from plugins.forward import app as Client2

pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

id_pattern = re.compile(r'^.\d+$') 

BOT_TOKEN = os.environ.get("TOKEN", "8025198727:AAF7sQa6srVJwKOxhRyUtgk_rbKG2p26ZC8")
API_ID = int(os.environ.get("API_ID", "20902603"))
API_HASH = os.environ.get("API_HASH", "79e5caa103a9e9fb0183390b4800845d")
BOT_UPTIME  = time.time()
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002513674254"))
WEBHOOK = bool(os.environ.get("WEBHOOK", True))
ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '6283322330').split()]
STRING_SESSION = os.environ.get("STRING_SESSION", "BQGtaBQAuA5hibW90nwEkYh4CLA0yR-lwrZ1Eky_XZ0EEutuqXHx9r3PtZPbYltBJK1Y8sODkdnxFQPghZ813ATMwZUU9IvgQfL-dM5a3RqvemSWLV4aJLFz63i0sU7LiiBU4Oet8tMFQhDlRZrTzpmRrIv43od92n_V7HzFADZ_cNdQbE93Y3KI1P3MjKTV5JpAukwTK0D3W4Y6dNZKMbySFOuvLSp2GuctV2fv9kWQivwlcRFpnlbF68M7GVWr_QOhWW8uIy0egAYFeQ4XmhQPiTKNPfRq1o44yTGEBafxgCCXpu-j-GSk8Ej0IRTOIRSJYJTBml2WuPbk8TLU3xlyCkJBowAAAAHCCCOwAQ")

Bot = Client("1TamilMVScrapper", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root='plugins'))

if STRING_SESSION:
    apps = [Client2,Bot]
    for app in apps:
        app.start()
    idle()
    for app in apps:
        app.stop()
    
else:
    Bot().run()

