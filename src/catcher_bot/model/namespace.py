"""
Different types that used everywhere
"""
from enum import Enum

# TODO tests

class BasedType(Enum):
    """
    Enum types contain 3 things about trade types: CODE, config value
    """
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, config_value: str):
        self._config_value = config_value

    def __str__(self):
        return self.value

    @property
    def config_value(self):
        return self._config_value

    @property
    def code(self):
        return self.value


class InstrumentType(BasedType):
    """
    Instrument types
    """

    # Name, Code, Config value
    STOCK = 0, 'stock'
    FUTURE = 1, 'future'
    OPTION = 2, 'option'


class MarketType(BasedType):
    """
    MarketTypes
    """

    # Name          Code
    EQUITY = 0, 'equity'
    COMMODITIES = 1, 'commodities'
    CRYPTO = 2, 'crypto'


class ExpirationDistance(BasedType):
    """
    Expirations for futures and options in sequence from nearest to far
    """
    ALL = None, None  # null in yaml or absent field
    PERPETUAL = 0, 'PERPETUAL'
    FIRST = 1, 1
    SECOND = 2, 2
    THIRD = 3, 3
    FOURTH = 4, 4
    FIFTH = 5, 5


class StrikeDistance(BasedType):
    """
    Strikes distance from strike at price
    """
    ALL = None, None  # null in yaml or absent field
    FIRST = 1, 1
    SECOND = 2, 2
    THIRD = 3, 3
    FOURTH = 4, 4
    FIFTH = 5, 5
