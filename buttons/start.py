from telegram import (
	Update,
	InputMediaPhoto,
	InputMediaDocument)

from telegram.ext import (
	Application,
	CallbackQueryHandler, 
	CommandHandler,
    ConversationHandler,
	ContextTypes
    )

from config import (
    reply_markup,
    CHOOSING)

from db.MySqlConn import Mysql

import logging
import time

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends a message with three inline buttons attached."""

    mysql = Mysql()
    user = update.effective_user
    user_id = user.id
    nick_name = user.full_name

    user_checkin = mysql.getOne(f"select * from users where user_id={user_id}")
    if not user_checkin:
        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "insert into users (user_id, name, nick_name, level, system_content, created_at) values (%s, %s, %s, %s, %s, %s)"
        value = [user_id, user.username, nick_name, 0, "You are an AI assistant that helps people find information.", date_time]
        mysql.insertOne(sql, value)
    if user_checkin and not user_checkin.get("nick_name"):
        mysql.update("update users set nick_name=%s where user_id=%s", (nick_name, user_id))
    mysql.end()

    # await context.bot.send_photo(
    #     chat_id=update.effective_chat.id,
    #     photo=photo_url,
    #     caption=message_content,
    #     reply_markup=reply_markup
    # )

    user = update.effective_user
    await update.message.reply_html(
        rf"""
        Hej  {user.mention_html()}!
I'm an AI chatbot created to interact with you and make your day a little brighter. If you have any questions or just want to have a friendly chat, I'm here to help! 🤗

Do you know what's great about me? I can help you with anything from giving advice to telling you a joke, and I'm available 24/7! 🕰️
    
Try to click left button to send a photo or a PDF file to me!

So why not share me with your friends? 😍 
You can send them this link: https://t.me/cxlink_bot

我是一个 AI 聊天机器人。我被创建出来是为了与你互动并让你的生活加美好。如果你有任何问题或只是想友好地聊天，我会在这里帮助你！🤗

我可以帮助你做任何事情，从给你建议到讲笑话，而且我全天候在线！🕰️

试试按下左下角按钮向我发送图片或者 PDF 文档吧！

快把我分享给你的朋友们吧！😍
你可以将此链接发送给他们：https://t.me/cxlink_bot
        """,
        reply_markup=reply_markup, disable_web_page_preview=True
    )

    return CHOOSING