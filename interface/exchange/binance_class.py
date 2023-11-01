import asyncio
from binance.client import AsyncClient, BinanceAPIException, Client

# from binance.client import AsyncClient, BinanceAPIException
from binance.streams import BinanceSocketManager

from interface.exchange import exchange_class
import logging


class Binance(exchange_class.Exchange):
    def __init__(self, credential: dict, log: logging.Logger):
        super(Binance, self).__init__('binance', credential, log)
        # self.api_key = credential['api_key']
        # self.api_secret = credential['api_secret']
        # self.client = None

    async def connect(self):
        self.client = await AsyncClient.create(self.api_key, self.api_secret)

    async def disconnect(self):
        await self.client.close_connection()

    async def get_symbol_list(self):
        self.log.info('[DEV] TEST')
        exch_info = await self.client.get_exchange_info()
        # print(exch_info)
        # /api/v3/exchangeInfo
        return exch_info['symbols']


class BinanceSocket(exchange_class.ExchangeSocket):
    def __init__(self, credential):
        super(BinanceSocket, self).__init__('binance')
        self.socket = None
        self.client = None
        self.api_key = credential['api_key']
        self.api_secret = credential['api_secret']

    async def connect(self):
        self.client = await AsyncClient.create(self.api_key, self.api_secret)
        self.socket = BinanceSocketManager(self.client, user_timeout=30)

    async def disconnect(self):
        await self.client.close_connection()
