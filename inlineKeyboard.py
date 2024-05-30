from telegram import (
	InlineKeyboardButton, 
	InlineKeyboardMarkup, 
	Update,
	InputMediaPhoto,
	InputMediaDocument)

from telegram.ext import (
	Application,
	CallbackQueryHandler, 
	CommandHandler,
    ConversationHandler,
	ContextTypes)

from wallet import (
    subscribe_address,
    address_transactions
    )

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

photo_url = "https://imagedelivery.net/MEE_uC7JRqWuK80eFOMH_A/1d3c4aba-9512-4126-a42a-eeb908d7a700/public"
# TODO: 临时添加静态内容
message_content = "一周重要星象\
	8/13 7pm 月亮与凯龙星刑克，月火六合，看涨；\
	8/14 月蟹换月狮，水星与木星，上升和天顶拱相，上午涨势不错但注意6am和10am前后有反转信号，建议当天有盈利见好就收，晚上星象开始走差；\
	8/15  月狮，土星与凯龙星凶相，看跌；\
	8/16 狮子座新月，太阳刑天王，但火星拱天王，凯龙星与日月金星拱相，不看跌，甚至看涨；\
	8/17  【逃顶日】！！上午12pm前有最好的逃顶机会，下午月亮处女冲土星, 非常糟糕\
	8/18 看跌周期第一天，但也可能出现反弹\
	8/20 月亮天秤，重要行星无明显角度，可能继续下跌"

# definition of callback data
CALLBACK_DATA_SUBSCRIBE = "subscribe"
CALLBACK_DATA_ADDRESS_TRANSACTION = "address_transactions"
CALLBACK_DATA_HELP = "help"
CALLBACK_DATA_EMPTY = "empty"

SUBSCRIBE, = range(1)

async def keyboard_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Subscribe", callback_data=CALLBACK_DATA_SUBSCRIBE),
            InlineKeyboardButton("Address Transactions", callback_data=CALLBACK_DATA_ADDRESS_TRANSACTION),
        ],
        [InlineKeyboardButton("Help", callback_data=CALLBACK_DATA_HELP)],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=message_content,
        reply_markup=reply_markup
    )
    # await update.message.reply_text(message_content, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    logger.info("[button]: button query data: %s.", query.data)

    # Handle different callback data options
    if query.data == CALLBACK_DATA_SUBSCRIBE:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter your Ethereum address:")
        return SUBSCRIBE
    elif query.data == CALLBACK_DATA_ADDRESS_TRANSACTION:
        await address_transactions(update, context)
        return 0
    elif query.data == CALLBACK_DATA_HELP:
        await help_command(update, context)
        return 0
    else:
        await query.edit_message_text(text=f"Selected option: {query.data}")

    await query.edit_message_text(text=f"Selected option: {query.data}")
    return 0

async def subscribe_address_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("[subscribe_address_conv]: %s.", update.message.text)
    await subscribe_address(update, context)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.")
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Use /start to test this bot.")