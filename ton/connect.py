import sys
import logging
import asyncio
import time
from io import BytesIO
import qrcode

import pytonconnect.exceptions
from pytoniq_core import Address
from pytonconnect import TonConnect

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
    )

from telegram.ext import (
    Application,
    CallbackQueryHandler, 
    CommandHandler,
    ConversationHandler,
    ContextTypes
    )

from config import (
    CHOOSING,
    reply_markup
    )
from ton.messages import get_comment_message
from ton.connector import get_connector


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def ton_wallet_connect_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_chat.id
    connector = get_connector(chat_id)
    connected = await connector.restore_connection()

    mk_b = []
    if connected:
        mk_b.append([InlineKeyboardButton("Send Transaction", callback_data='ton_wallet_send_tr')])
        mk_b.append([InlineKeyboardButton("Disconnect", callback_data='ton_wallet_disconnect')])
        await update.effective_message.reply_text("You are already connected!", reply_markup=InlineKeyboardMarkup(mk_b))

    else:
        wallets_list = TonConnect.get_wallets()

        for wallet in wallets_list:
            mk_b.append([InlineKeyboardButton(wallet['name'], callback_data=f'ton_wallet_connect:{wallet["name"]}')])
        # mk_b.adjust(1, )
        await update.effective_message.reply_text("Choose wallet to connect", reply_markup=InlineKeyboardMarkup(mk_b))

    return CHOOSING


async def send_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_chat.id
    connector = get_connector(chat_id)
    connected = await connector.restore_connection()
    if not connected:
        await update.effective_message.edit_message_text('Connect wallet first!')
        return 

    transaction = {
        'valid_until': int(time.time() + 3600),
        'messages': [
            get_comment_message(
                destination_address='0:0000000000000000000000000000000000000000000000000000000000000000',
                amount=int(0.01 * 10 ** 9),
                comment='hello world!'
            )
        ]
    }

    await update.callback_query.edit_message_text(text='Approve transaction in your wallet app!')

    asyncio.create_task(async_transactions(update, context, connector, transaction))

    return CHOOSING

async def async_transactions(update: Update, context: ContextTypes.DEFAULT_TYPE, connector: TonConnect, transaction: dict) -> int:
    try:
        await asyncio.wait_for(connector.send_transaction(
            transaction=transaction
        ), 300)
    except asyncio.TimeoutError:
        await update.callback_query.edit_message_text(text='Timeout error!')
    except pytonconnect.exceptions.UserRejectsError:
        await update.callback_query.edit_message_text(text='You rejected the transaction!')
    except Exception as e:
        await update.callback_query.edit_message_text(text=f'Unknown error: {e}')

    return CHOOSING

async def connect_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE, wallet_name: str):
    connector = get_connector(update.effective_chat.id)
    wallets_list = connector.get_wallets()
    wallet = None

    for w in wallets_list:
        if w['name'] == wallet_name:
            wallet = w

    if wallet is None:
        raise Exception(f'Unknown wallet: {wallet_name}')

    generated_url = await connector.connect(wallet)

    mk_b = []
    mk_b.append([InlineKeyboardButton("Connect", url=generated_url)])

    img = qrcode.make(generated_url)
    stream = BytesIO()
    img.save(stream)
    stream.seek(0)

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=stream,
        caption="Connect wallet within 3 minutes",
        reply_markup=InlineKeyboardMarkup(mk_b)
    )

    # create an async task to check wallet connection.
    asyncio.create_task(check_connection(update, context, connector))

    return CHOOSING

async def disconnect_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    connector = get_connector(update.effective_chat.id)
    await connector.restore_connection()
    await connector.disconnect()
    await update.callback_query.edit_message_text(f"You have been successfully disconnected!")

    return CHOOSING

async def check_connection(update: Update, context: ContextTypes.DEFAULT_TYPE, connector: TonConnect) -> int:
    
    mk_b = []
    mk_b.append([InlineKeyboardButton("Wallet", callback_data='ton_wallet_start')])

    for _ in range(180): # 3 minutes
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                wallet_address = Address(wallet_address).to_str(is_bounceable=False)
                
                await update.effective_message.reply_text(
                    f"You are connected with address <code>{wallet_address}</code>", 
                    parse_mode='HTML',
                    reply_markup=InlineKeyboardMarkup(mk_b))
                
                logger.info(f'Connected with address: {wallet_address}')
            
            return CHOOSING
        
        await asyncio.sleep(1)

    await update.effective_message.reply_text(
        "Timeout error", 
        reply_markup=InlineKeyboardMarkup(mk_b)
    )

    return CHOOSING

async def ton_wallet_connect_callback_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    await query.answer()
    data = query.data
    logger.info(f'[ton_wallet_connect_callback_handle]: {data}')

    if data == "ton_wallet_start":
        await ton_wallet_connect_handler(update, context)
    elif data == "ton_wallet_send_tr":
        await send_transaction(update, context)
    elif data == 'ton_wallet_disconnect':
        await disconnect_wallet(update, context)
    else:
        data = data.split(':')
        if data[0] == 'ton_wallet_connect':
            await connect_wallet(update, context, data[1])
    return CHOOSING