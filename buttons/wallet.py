from telegram import Update
from telegram.ext import ContextTypes
import requests

from config import (
    WALLET_URL,
    reply_markup,
    cancel_markup,
    CHOOSING, TYPING_SUBSCRIBED_ADDR, TYPING_ADDR_TRANS)

async def address_transactions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    await update.message.reply_text("Please enter Ethereum address:", reply_markup=cancel_markup)
    return TYPING_SUBSCRIBED_ADDR

async def subscribe_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    await update.message.reply_text("Please enter Ethereum address:", reply_markup=cancel_markup)
    return TYPING_ADDR_TRANS

async def address_transactions_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=return_message,
        reply_markup=reply_markup)
    return CHOOSING

async def subscribe_address_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=return_message,
        reply_markup=reply_markup)
    return CHOOSING