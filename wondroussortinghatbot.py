import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import requests
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN', 'empty value')
WALLET_URL = os.environ.get('WALLET_URL', 'empty value')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Hogwarts, the wisdom hat guides you towards the gateway of the magical world.")


async def subscribe_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = WALLET_URL + "/v1/subscribe"
    text = update.message.text.split(' ')[-1]
    wallet_address = text

    # Check address if is valid.
    params = {"address": wallet_address}
    # POST
    response = requests.post(url, data=params)
    
    return_message = "subscribe wallet address"
    
    # check resp status code
    if response.status_code == 200:
        # parse JSON
        data = response.json()

        # check resp code
        if data["code"] == 0:
            return_message = wallet_address + " transactions subscribed."
        else:
            return_message = f"subscribed failed with err code: {data['code']}"
    else:
        return_message = f"request failed, status code: {response.status_code}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=return_message)


async def address_transactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.split(' ')[-1]
    wallet_address = text
    # Check address if is valid.
    params = {"address": wallet_address}
    # define request URL
    url = WALLET_URL + "/v1/get_transactions"
    # POST
    response = requests.get(url, params=params)
    
    return_message = "empty transactions record."
    
    # check resp status code
    if response.status_code == 200:
        # parse JSON
        data = response.json()

        # check resp code
        if data["code"] == 0:
            print("get address transactions successsed.")
            # get transactions info here.
            return_message = data["data"]
        else:
            print(f"get address transactions failed, err code: {data['code']}")
    else:
        return_message = f"request failed, status code: {response.status_code}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=return_message)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TG_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    subscribe_handler = CommandHandler('subscribe', subscribe_address)
    address_transactions_handler = CommandHandler('transactions', address_transactions)
    caps_handler = CommandHandler('caps', caps)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    inline_caps_handler = InlineQueryHandler(inline_caps)

    application.add_handler(start_handler)
    application.add_handler(subscribe_handler)
    application.add_handler(address_transactions_handler)
    # application.add_handler(echo_handler) // 造成群内消息复读
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)
    
    application.run_polling()