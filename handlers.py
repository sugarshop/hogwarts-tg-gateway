from telegram.ext import CommandHandler, InlineQueryHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from wallet import subscribe_address, address_transactions
from inlineKeyboard import keyboard_start, button, help_command

subscribe_handler = CommandHandler('subscribe', subscribe_address)
address_transactions_handler = CommandHandler('transactions', address_transactions)

start_handler = CommandHandler("start", keyboard_start)
inlineKeyboard_button_handler = CallbackQueryHandler(button)
help_handler = CommandHandler("help", help_command)