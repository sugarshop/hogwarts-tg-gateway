from telegram import Update
from telegram.ext import ContextTypes

from config import (
    reply_markup,
    CHOOSING)


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'choice' in context.user_data:
        del context.user_data['choice']
    
    await update.message.reply_text('Operation canceled.', reply_markup=reply_markup)
    return CHOOSING