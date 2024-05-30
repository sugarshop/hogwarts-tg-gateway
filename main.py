import logging
from telegram.ext import ApplicationBuilder
from telegram import Update
import requests
import os
from handlers import (
    start_handler, 
    subscribe_handler, 
    address_transactions_handler, 
    start_handler,
    inlineKeyboard_button_handler,
    help_handler,
    conv_cancel_handler,
    subscribe_address_conv_handler,
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
    
    application.add_handler(start_handler)
    application.add_handler(subscribe_handler)
    application.add_handler(address_transactions_handler)
    application.add_handler(inlineKeyboard_button_handler)
    application.add_handler(help_handler)
    application.add_handler(conv_cancel_handler)
    application.add_handler(subscribe_address_conv_handler)
    application.add_handler(wallet_address_subscribe_handler)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)