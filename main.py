import logging
from telegram.ext import ApplicationBuilder
from telegram import Update
import requests
import os
from handlers import (
    wallet_address_subscribe_handler
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', 'empty value')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TG_BOT_TOKEN).build()
    
    application.add_handler(wallet_address_subscribe_handler)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)