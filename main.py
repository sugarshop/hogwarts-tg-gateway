import logging
from telegram.ext import ApplicationBuilder
import requests
import os
from handlers import (
    start_handler, 
    subscribe_handler, 
    address_transactions_handler, 
    caps_handler, 
    inline_caps_handler
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', 'empty value')

if __name__ == '__main__':
    application = ApplicationBuilder().token(TG_BOT_TOKEN).build()
    
    application.add_handler(start_handler)
    application.add_handler(subscribe_handler)
    application.add_handler(address_transactions_handler)
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)
    
    application.run_polling()