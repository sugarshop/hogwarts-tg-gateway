from telegram.ext import (
	CommandHandler, 
	InlineQueryHandler, 
	CallbackQueryHandler,
	ConversationHandler,
	MessageHandler,
	filters,
	)
from telegram import (
	InlineQueryResultArticle, 
	InputTextMessageContent
	)
from wallet import (
	subscribe_address, 
	address_transactions
	)
from inlineKeyboard import (
	keyboard_start, 
	button, 
	help_command,
	subscribe_address_conv,
	cancel,
	SUBSCRIBE
	)

subscribe_handler = CommandHandler('subscribe', subscribe_address)
address_transactions_handler = CommandHandler('transactions', address_transactions)

start_handler = CommandHandler("start", keyboard_start)
inlineKeyboard_button_handler = CallbackQueryHandler(button)
subscribe_address_conv_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, subscribe_address_conv)
help_handler = CommandHandler("help", help_command)
conv_cancel_handler = CommandHandler("cancel", cancel)

wallet_address_subscribe_handler = ConversationHandler(
	entry_points=[start_handler, inlineKeyboard_button_handler],
	states={
		SUBSCRIBE: [subscribe_address_conv_handler],
	},
    fallbacks=[conv_cancel_handler],
)