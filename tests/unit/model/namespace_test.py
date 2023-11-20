#pylint: disable=C0111,protected-access
import pytest

from catcher_bot.model import namespace as ns


def test_get_by_id():
    assert ns.ModuleType['STRATEGY'] == ns.ModuleType.get_by_id('strategy')
    assert ns.ModuleType['PORTFOLIO'] == ns.ModuleType.get_by_id(ns.ModuleType['PORTFOLIO'].value)
    assert ns.ModuleType['CONNECTOR'] == ns.ModuleType.get_by_id(ns.ModuleType['CONNECTOR'])
    with pytest.raises(KeyError):
        _ = ns.ModuleType['WRONG_TYPE']
    with pytest.raises(KeyError):
        _ = ns.ModuleType.get_by_id('WRONG_TYPE')
    with pytest.raises(KeyError):
        _ = ns.ModuleType.get_by_id(-1)


def test_get_names():
    type_names = [type_val.name for type_val in ns.ModuleType]
    assert type_names == ns.get_names(ns.ModuleType)


def test_is_valid_name():
    assert ns.ModuleType.is_valid_name('STRATEGY')
    assert not ns.ModuleType.is_valid_name('WRONG_TYPE')


def test_is_equal_name():
    strategy_type = ns.ModuleType['STRATEGY']
    assert strategy_type.is_equal_name('Strategy')
    assert not strategy_type.is_equal_name('WRONG_TYPE')


def test_module_type_valid():
    assert ns.ModuleType.PORTFOLIO
    assert ns.ModuleType['PORTFOLIO']
    assert ns.ModuleType.CONNECTOR
    assert ns.ModuleType['CONNECTOR']
    assert ns.ModuleType.STRATEGY
    assert ns.ModuleType['STRATEGY']


def test_module_type_names():
    """
    If changed there should be changes everywhere
    """
    names = sorted({'CONNECTOR', 'PORTFOLIO', 'STRATEGY'})
    assert len(ns.ModuleType) == len(names)
    current_names = sorted([code for code in dir(ns.ModuleType) if not code.startswith('_')])
    assert current_names == names


def test_module_type_invalid():
    with pytest.raises(AttributeError):
        assert ns.ModuleType.WRONG_MODULE_TYPE
    with pytest.raises(KeyError):
        assert ns.ModuleType['WRONG_MODULE_TYPE']


def test_instrument_type_valid():
    assert ns.InstrumentType.STOCK
    assert ns.InstrumentType['STOCK']
    assert ns.InstrumentType.FUTURE
    assert ns.InstrumentType['FUTURE']
    assert ns.InstrumentType.OPTION
    assert ns.InstrumentType['OPTION']


def test_instrument_type_names():
    """
    If changed there should be changes everywhere
    """
    names = sorted({'STOCK', 'FUTURE_PERPETUAL', 'FUTURE', 'OPTION'})
    assert len(ns.InstrumentType) == len(names)
    current_names = sorted([code for code in dir(ns.InstrumentType) if not code.startswith('_')])
    assert current_names == names


def test_instrument_type_invalid():
    with pytest.raises(AttributeError):
        assert ns.InstrumentType.WRONG_TYPE
    with pytest.raises(KeyError):
        assert ns.InstrumentType['WRONG_TYPE']


def test_market_type_valid():
    assert ns.MarketType.EQUITY
    assert ns.MarketType['EQUITY']
    assert ns.MarketType.COMMODITIES
    assert ns.MarketType['COMMODITIES']
    assert ns.MarketType.CRYPTO
    assert ns.MarketType['CRYPTO']


def test_market_type_names():
    """
    If changed there should be changes everywhere
    """
    names = sorted({'EQUITY', 'COMMODITIES', 'CRYPTO'})
    assert len(ns.MarketType) == len(names)
    current_names = sorted([code for code in dir(ns.MarketType) if not code.startswith('_')])
    assert current_names == names


def test_market_type_invalid():
    with pytest.raises(AttributeError):
        assert ns.MarketType.WRONG_TYPE
    with pytest.raises(KeyError):
        assert ns.MarketType['WRONG_TYPE']



def test_expiration_distance_valid():
    assert ns.ExpirationDistance.ALL
    assert ns.ExpirationDistance['ALL']
    assert ns.ExpirationDistance.ALL.value is None
    # assert ns.ExpirationDistance.PERPETUAL
    # assert ns.ExpirationDistance['PERPETUAL']
    assert ns.ExpirationDistance.FIRST
    assert ns.ExpirationDistance['FIRST']
    assert ns.ExpirationDistance.SECOND
    assert ns.ExpirationDistance['SECOND']
    assert ns.ExpirationDistance.THIRD
    assert ns.ExpirationDistance['THIRD']
    assert ns.ExpirationDistance.FOURTH
    assert ns.ExpirationDistance['FOURTH']
    assert ns.ExpirationDistance.FIFTH
    assert ns.ExpirationDistance['FIFTH']


def test_expiration_distance_names():
    """
    If changed there should be changes everywhere
    """
    names = sorted({'ALL', 'FIRST', 'SECOND', 'THIRD', 'FOURTH', 'FIFTH'}) # 'PERPETUAL',
    assert len(ns.ExpirationDistance) == len(names)
    current_names = sorted([code for code in dir(ns.ExpirationDistance) if not code.startswith('_')])
    assert current_names == names


def test_expiration_distance_invalid():
    with pytest.raises(AttributeError):
        assert ns.ExpirationDistance.WRONG_TYPE
    with pytest.raises(KeyError):
        assert ns.ExpirationDistance['WRONG_TYPE']


def test_strike_distance_valid():
    assert ns.StrikeDistance.ALL
    assert ns.StrikeDistance['ALL']
    assert ns.StrikeDistance.ALL.value is None
    assert ns.StrikeDistance.FIRST
    assert ns.StrikeDistance['FIRST']
    assert ns.StrikeDistance.SECOND
    assert ns.StrikeDistance['SECOND']
    assert ns.StrikeDistance.THIRD
    assert ns.StrikeDistance['THIRD']
    assert ns.StrikeDistance.FOURTH
    assert ns.StrikeDistance['FOURTH']
    assert ns.StrikeDistance.FIFTH
    assert ns.StrikeDistance['FIFTH']


def test_expiration_distance_names():
    """
    If changed there should be changes everywhere
    """
    names = sorted({'ALL', 'FIRST', 'SECOND', 'THIRD', 'FOURTH', 'FIFTH'})
    assert len(ns.StrikeDistance) == len(names)
    current_names = sorted([code for code in dir(ns.StrikeDistance) if not code.startswith('_')])
    assert current_names == names


def test_expiration_distance_invalid():
    with pytest.raises(AttributeError):
        assert ns.ExpirationDistance.WRONG_TYPE
    with pytest.raises(KeyError):
        assert ns.ExpirationDistance['WRONG_TYPE']

