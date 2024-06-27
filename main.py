import logging
from telegram.ext import (
    ApplicationBuilder,
    PicklePersistence
)
from telegram import Update
import requests
import os
from handlers import (
    conv_handler,
    show_chat_modes_callback_query_handler,
    set_chat_mode_callback_query_handler,
    cancel_chat_mode_callback_query_handler,
    show_languages_callback_query_handler,
    ton_wallet_connect_callback_handler
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
    # Create the Updater and pass it your bot's token.
    persistence = PicklePersistence(filepath='conversationbot')

    application = ApplicationBuilder().token(TG_BOT_TOKEN).persistence(persistence).build()
    
    application.add_handler(conv_handler)
    application.add_handler(show_chat_modes_callback_query_handler)
    application.add_handler(set_chat_mode_callback_query_handler)
    application.add_handler(cancel_chat_mode_callback_query_handler)
    application.add_handler(show_languages_callback_query_handler)
    application.add_handler(ton_wallet_connect_callback_handler)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)