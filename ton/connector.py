from pytonconnect import TonConnect

from ton.tc_storage import TcStorage

import config


def get_connector(chat_id: int):
    return TonConnect(config.manifest_url, storage=TcStorage(chat_id))