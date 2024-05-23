from telegram.ext import CommandHandler, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from utils import start, subscribe_address, address_transactions, caps, inline_caps

start_handler = CommandHandler('start', start)
subscribe_handler = CommandHandler('subscribe', subscribe_address)
address_transactions_handler = CommandHandler('transactions', address_transactions)
caps_handler = CommandHandler('caps', caps)
inline_caps_handler = InlineQueryHandler(inline_caps)