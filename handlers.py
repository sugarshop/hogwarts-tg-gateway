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
	address_transactions_conv,
	cancel,
	CHOOSING,
	SUBSCRIBE_BUTTON_TRIGGERED,
	ADDRESS_TRANSACTION_BUTTON_TRIGGERED,
	CALLBACK_DATA_SUBSCRIBE,
	CALLBACK_DATA_ADDRESS_TRANSACTION,
	CALLBACK_DATA_HELP
	)

subscribe_handler = CommandHandler('subscribe', subscribe_address)
address_transactions_handler = CommandHandler('transactions', address_transactions)

start_handler = CommandHandler("start", keyboard_start)
subscribe_address_conv_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, subscribe_address_conv)
address_transactions_conv_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, address_transactions_conv)
help_handler = CommandHandler("help", help_command)
conv_cancel_handler = CommandHandler("cancel", cancel)

wallet_address_subscribe_handler = ConversationHandler(
	entry_points=[start_handler],
	states={
		CHOOSING: [CallbackQueryHandler(button, pattern=f"^({CALLBACK_DATA_SUBSCRIBE}|{CALLBACK_DATA_HELP}|{CALLBACK_DATA_ADDRESS_TRANSACTION})$")],
		SUBSCRIBE_BUTTON_TRIGGERED: [subscribe_address_conv_handler],
		ADDRESS_TRANSACTION_BUTTON_TRIGGERED: [address_transactions_conv_handler]
	},
    fallbacks=[conv_cancel_handler],
)