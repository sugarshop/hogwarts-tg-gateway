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
	ContextTypes)

photo_url = "https://imagedelivery.net/MEE_uC7JRqWuK80eFOMH_A/1d3c4aba-9512-4126-a42a-eeb908d7a700/public"
message_content = "一周重要星象\
	8/13 7pm 月亮与凯龙星刑克，月火六合，看涨；\
	8/14 月蟹换月狮，水星与木星，上升和天顶拱相，上午涨势不错但注意6am和10am前后有反转信号，建议当天有盈利见好就收，晚上星象开始走差；\
	8/15  月狮，土星与凯龙星凶相，看跌；\
	8/16 狮子座新月，太阳刑天王，但火星拱天王，凯龙星与日月金星拱相，不看跌，甚至看涨；\
	8/17  【逃顶日】！！上午12pm前有最好的逃顶机会，下午月亮处女冲土星, 非常糟糕\
	8/18 看跌周期第一天，但也可能出现反弹\
	8/20 月亮天秤，重要行星无明显角度，可能继续下跌"

async def keyboard_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Subscribe", callback_data="1"),
            InlineKeyboardButton("Address Transactions", callback_data="2"),
        ],
        [InlineKeyboardButton("Help", callback_data="3")],
    ]

    # media = InputMediaPhoto(media=photo_url)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=message_content,
        reply_markup=reply_markup
    )
    # await update.message.reply_text(message_content, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")