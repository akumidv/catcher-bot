"""
Mosck strategy module
"""
from catcher_bot.model.module.strategy import Strategy
from catcher_bot.model.namespace import MarketType, InstrumentType


class MockStrategy(Strategy):
    """
    Mock strategy for testing
    """

    name = 'Mock strategy' # TODO Does it really needed?
    market_type = [MarketType.CRYPTO, MarketType.EQUITY, MarketType.COMMODITIES] # TODO check when import module
    instrument_type = [InstrumentType.STOCK, InstrumentType.FUTURE] # TODO check when import module

    def __init__(self):
        print('#### Mock Strategy INIT')

    def next(self):
        print('#### NEXT')

    def init(self):
        pass