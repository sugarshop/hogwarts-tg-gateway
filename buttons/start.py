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

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=message_content,
        reply_markup=reply_markup
    )
    return CHOOSING