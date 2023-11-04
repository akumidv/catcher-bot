import os.path
from dataclasses import is_dataclass
import pytest
from model.strategy_config import StrategyConfig, ExchangeConfig, get_empty_strategy_config
import yaml
from tests.context import MOCKS_DIR
import logging


log = logging.getLogger(os.path.basename(__file__)[:-3])


@pytest.fixture()
def strategy_cfg_dict():
    with open(f'{MOCKS_DIR}/strategies/mock_strategy.yaml', 'r') as file:
        strategy_cfg_d = yaml.safe_load(file)
    return strategy_cfg_d

def check_strategy_configurations_dict(strategy_cfg_d: dict):
    assert isinstance(strategy_cfg_d, dict)
    assert 'code' in strategy_cfg_d


@pytest.fixture()
def strategy_cfg_mock(strategy_cfg_dict) -> StrategyConfig:
    return StrategyConfig(**strategy_cfg_dict)


def check_strategy_config(strategy_cfg: StrategyConfig):
    assert is_dataclass(strategy_cfg)
    assert not isinstance(strategy_cfg, type)
    assert isinstance(strategy_cfg, StrategyConfig)
    assert isinstance(strategy_cfg.code, str)
    assert isinstance(strategy_cfg.parameters, dict) or strategy_cfg.parameters is None
    assert isinstance(strategy_cfg.exchanges_symbols, list)
    assert len(strategy_cfg.exchanges_symbols) >= 0
    exchange_cfg = strategy_cfg.exchanges_symbols[0]
    assert is_dataclass(exchange_cfg)
    assert isinstance(exchange_cfg, ExchangeConfig)


def test_strategy_instance(strategy_cfg_dict):
    check_strategy_configurations_dict(strategy_cfg_dict)
    strategy_cfg = StrategyConfig(**strategy_cfg_dict)
    check_strategy_config(strategy_cfg)


def test_to_yaml(strategy_cfg_mock):
    yaml_str = strategy_cfg_mock.to_yaml()
    assert isinstance(yaml_str, str)
    strategy_cfg_dict_restored = yaml.safe_load(yaml_str)
    assert strategy_cfg_dict_restored['code'] == strategy_cfg_mock.code
    print(yaml_str)
    print(strategy_cfg_dict_restored)


def test_get_empty_strategy_config():
    strategy_cfg = get_empty_strategy_config('TEST')
    check_strategy_config(strategy_cfg)


