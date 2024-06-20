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
from config import (
	subscribe_address_button,
	address_transactions_button,
    contact_admin,
    chat_button,
    set_sys_content_button,
    reset_context_button,
    statistics_button,
    switch_role_button,
    language_button,
    cancel_button,
    CHOOSING, TYPING_REPLY, TYPING_SYS_CONTENT, TYPING_SUBSCRIBED_ADDR, TYPING_ADDR_TRANS
)
from buttons.inline import (
    show_chat_modes_handle,
    show_chat_modes_callback_handle,
    set_chat_mode_handle,
    cancel_chat_mode_handle,
)
from buttons.start import start
from buttons.language import show_languages, show_languages_callback_handle
from buttons.wallet import subscribe_address, address_transactions, subscribe_address_handler, address_transactions_handler
from buttons.help import helper
from buttons.chat import chat
from buttons.cancel import cancel_handler
from buttons.role import set_system_content, reset_context, set_system_content_handler
from buttons.statistics import statistics
from buttons.others import non_text_handler, done, error_handler

from chat.handler import answer_handler


conv_handler = ConversationHandler(
	entry_points=[
			MessageHandler(filters.Regex(f'^/start$'), start, ),
		],
	states={
		CHOOSING: [
			MessageHandler(filters.Regex(f'^/start$'), start, ),
			MessageHandler(filters.Regex(f'^{contact_admin}$'), helper, ),
            MessageHandler(filters.Regex(f'^({chat_button}|/chat|Chat)$'), chat, ),
            MessageHandler(filters.Regex(f'^{language_button}$'), show_languages, ),
            MessageHandler(filters.Regex(f'^{subscribe_address_button}$'), subscribe_address, ),
            MessageHandler(filters.Regex(f'^{address_transactions_button}$'), address_transactions, ),
            MessageHandler(filters.Regex(f"^{reset_context_button}$"), reset_context),
            MessageHandler(filters.Regex(f"^{set_sys_content_button}$"), set_system_content),
            MessageHandler(filters.Regex(f"^{statistics_button}$"), statistics),
            MessageHandler(filters.Regex(f"^{switch_role_button}$"), show_chat_modes_handle),
            MessageHandler(filters.TEXT, answer_handler),
            MessageHandler(filters.ATTACHMENT, non_text_handler),
		],
		TYPING_REPLY: [
			MessageHandler(filters.Regex(f'^/start$'), start, ),
			MessageHandler(filters.Regex(f'^{contact_admin}$'), helper, ),
            MessageHandler(filters.Regex(f'^({chat_button}|/chat|Chat)$'), chat, ),
            MessageHandler(filters.Regex(f'^{language_button}$'), show_languages, ),
            MessageHandler(filters.Regex(f'^{subscribe_address_button}$'), subscribe_address, ),
            MessageHandler(filters.Regex(f'^{address_transactions_button}$'), address_transactions, ),
            MessageHandler(filters.Regex(f"^{reset_context_button}$"), reset_context),
            MessageHandler(filters.Regex(f"^{set_sys_content_button}$"), set_system_content),
            MessageHandler(filters.Regex(f"^{statistics_button}$"), statistics),
            MessageHandler(filters.Regex(f"^{switch_role_button}$"), show_chat_modes_handle),
            MessageHandler(filters.TEXT, answer_handler),
            MessageHandler(filters.ATTACHMENT, non_text_handler),
		],
		TYPING_SYS_CONTENT: [
            MessageHandler(filters.TEXT, set_system_content_handler),
            MessageHandler(filters.Regex(f"^{cancel_button}$"), cancel_handler, )
        ],
        TYPING_SUBSCRIBED_ADDR: [
        	MessageHandler(filters.Regex(f'^{subscribe_address_button}$'), subscribe_address_handler),
            MessageHandler(filters.Regex(f"^{cancel_button}$"), cancel_handler, )
        ],
        TYPING_ADDR_TRANS: [
        	MessageHandler(filters.Regex(f'^{address_transactions_button}$'), address_transactions_handler),
        	MessageHandler(filters.Regex(f"^{cancel_button}$"), cancel_handler, )
        ],
	},
    fallbacks=[MessageHandler(filters.Regex('^Done$'), done)],
    name="my_conversation",
    persistent=True,
)

show_chat_modes_callback_query_handler = CallbackQueryHandler(show_chat_modes_callback_handle, pattern="^show_chat_modes")
set_chat_mode_callback_query_handler = CallbackQueryHandler(set_chat_mode_handle, pattern="^set_chat_mode")
cancel_chat_mode_callback_query_handler = CallbackQueryHandler(cancel_chat_mode_handle, pattern="^cancel")
show_languages_callback_query_handler = CallbackQueryHandler(show_languages_callback_handle, pattern="^lang")
