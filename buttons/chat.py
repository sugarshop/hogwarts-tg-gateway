from telegram import Update
from telegram.ext import ContextTypes

from config import (
    CHOOSING, reply_markup
    )
# Define a few command handlers. These usually take the two arguments update and
# context.
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a message when the command /chat is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"""
        Hej  {user.mention_html()}!
I'm an AI chatbot created to interact with you and make your day a little brighter. If you have any questions or just want to have a friendly chat, I'm here to help! 🤗

Do you know what's great about me? I can help you with anything from giving advice to telling you a joke, and I'm available 24/7! 🕰️

So why not share me with your friends? 😍 
You can send them this link: https://t.me/cxlink_bot

我是一个 AI 聊天机器人。我被创建出来是为了与你互动并让你的生活加美好。如果你有任何问题或只是想友好地聊天，我会在这里帮助你！🤗

我可以帮助你做任何事情，从给你建议到讲笑话，而且我全天候在线！🕰️

快把我分享给你的朋友们吧！😍
你可以将此链接发送给他们：https://t.me/cxlink_bot
        """,
        reply_markup=reply_markup, disable_web_page_preview=True
    )
    return CHOOSING