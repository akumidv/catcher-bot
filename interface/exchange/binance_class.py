import asyncio
from binance.client import AsyncClient, BinanceAPIException, Client

# from binance.client import AsyncClient, BinanceAPIException
from binance.streams import BinanceSocketManager

from . import exchange_class


class Binance(exchange_class.Exchange):
    def __init__(self, credential):
        super(Binance, self).__init__('binance')
        self.api_key = credential['api_key']
        self.api_secret = credential['api_secret']
        self.client = None

    async def create(self):
        self.client = await AsyncClient.create(self.api_key, self.api_secret)


class BinanceSocket(exchange_class.ExchangeSocket):
    def __init__(self, credential):
        super(BinanceSocket, self).__init__('binance')
        self.socket = None
        self.client = None
        self.api_key = credential['api_key']
        self.api_secret = credential['api_secret']

    async def create(self):
        self.client = await AsyncClient.create(self.api_key, self.api_secret)
        self.socket = BinanceSocketManager(self.client, user_timeout=30)

