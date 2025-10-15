
# ⚙️ BOT VA KANAL SOZLAMALARI

# config.py

import os
from dotenv import load_dotenv

# .env faylni yuklaymiz
load_dotenv()

# Token va kanal nomini o‘qiymiz
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

if not BOT_TOKEN or not CHANNEL_USERNAME:
    raise ValueError("⚠️ Iltimos, .env faylda BOT_TOKEN va CHANNEL_USERNAME qiymatlarini to‘ldiring!")
