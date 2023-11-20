"""
Different types that used everywhere
"""
from enum import Enum
from typing import Union


def get_names(type_class: type[Enum]):
    return [type_val.name for type_val in type_class]


class BasedType(Enum):
    """
    Base class of types
    """
    def __str__(self):
        return str(self.value)

    def is_equal_name(self, name: str):
        """
        Compare by name
        """
        return str(self.name).upper() == name.upper()

    @classmethod
    def is_valid_name(cls, id_val: str):
        """
        Compare by name
        """
        return hasattr(cls, id_val.upper())

    @classmethod
    def get_by_id(cls, id_val: Union[int, str, object]):
        """
        Init type from value or name
        """
        if isinstance(id_val, cls):
            return id_val

        type_instance = None
        if isinstance(id_val, str):
            if hasattr(cls, id_val):
                type_instance = cls[id_val]
            elif hasattr(cls, id_val.upper()):
                type_instance = cls[id_val.upper()]
        if type_instance is None: # Init by value
            type_instances = [type_instance for type_instance in cls if type_instance.value == id_val]
            if len(type_instances) > 0:
                type_instance = type_instances[0]
            else:
                type_instance = cls[id_val] # raise KeyError
        return type_instance


class ModuleType(BasedType):
    """
    Loaded and configured nodule types
    """
    PORTFOLIO = 0
    CONNECTOR = 1
    STRATEGY = 2


class InstrumentType(BasedType):
    """
    Instrument types
    """
    # Name, Code
    STOCK = 0
    FUTURE_PERPETUAL = 1
    FUTURE = 2
    OPTION = 3


class MarketType(BasedType):
    """
    MarketTypes
    """

    # Name          Code
    EQUITY = 0
    COMMODITIES = 1
    CRYPTO = 2


class ConnectorType(BasedType):
    """
    Conntector types
    """

    # Name          Code
    EXCHANGE = 0



class ExpirationDistance(BasedType):
    """
    Expirations for futures and options in sequence from nearest to far
    """
    ALL = None  # null in yaml or absent field
    # PERPETUAL = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5


class StrikeDistance(BasedType):
    """
    Strikes distance from strike at price
    """
    ALL = None  # null in yaml or absent field
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
