from config import Config
from database.naruto import *
from pyrogram import Client, idle
import asyncio, logging
import threading
import os
from flask import Flask

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("Live log streaming to telegram.")
plugins = dict(root="plugins")
if __name__ == "__main__":
    # ─── Flask keep-alive server for Render ───────────────────────────────────────
flask_app = Flask(name)

@flask_app.route('/')
def index():
    return 'Bot is running!'

def run_flask():
    port = int(os.environ.get("PORT", 8000))
    flask_app.run(host="0.0.0.0", port=port)

# Start Flask in background thread so Render detects open port
threading.Thread(target=run_flask, daemon=True).start()
# ─────────────────────────────────────────
    bot = Client(
        "Master",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=120,
        plugins=plugins,
        workers=10000,
    )
    async def main():
        await bot.start()
        bot_info = await bot.get_me()
        LOGGER.info(f"<--- @{bot_info.username} Started --->")
        await idle()
    asyncio.get_event_loop().run_until_complete(main())
    LOGGER.info("<--- Bot Stopped --->")
