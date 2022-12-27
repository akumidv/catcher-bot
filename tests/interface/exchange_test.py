import pytest
from interface.exchange import exchange


def test_init_exchange():
    exchange_name = 'binance'
    binance = exchange.init_exchange(exchange_name, {'api_key': '', 'api_secret': ''})
    assert exchange_name.upper() == binance.get_name()


def test_init_exchange_wrong():
    exchange_name = 'NOT_EXIST_EXCHANGE'
    with pytest.raises(ModuleNotFoundError) as exc_info:
        not_exist_exchange = exchange.init_exchange(exchange_name, {})
    assert exc_info.type is ModuleNotFoundError


