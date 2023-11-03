import os.path

import pytest
from model.strategy_config import StrategyConfig, get_empty_strategy_config
import yaml
from tests.context import MOCKS_DIR
import logging


log = logging.getLogger(os.path.basename(__file__)[:-3])


@pytest.fixture()
def strategy_cfg_list() -> list[dict]:
    with open(f'{MOCKS_DIR}/strategies/mock_strategy.yaml', 'r') as file:
        cfg_list = yaml.safe_load(file)
    return cfg_list


@pytest.fixture()
def strategy_cfg_dict(strategy_cfg_list):
    return strategy_cfg_list[0]


@pytest.fixture()
def strategy_cfg_mock(strategy_cfg_dict) -> StrategyConfig:
    return StrategyConfig(**strategy_cfg_dict)


def check_strategy_config(strategy_cfg: StrategyConfig):
    assert isinstance(strategy_cfg, StrategyConfig)
    assert isinstance(strategy_cfg.name, str)
    assert isinstance(strategy_cfg.parameters, dict) or strategy_cfg.parameters is None


def check_strategy_configurations_dict(strategy_cfg_list: list[StrategyConfig]):
    assert isinstance(strategy_cfg_list, list)
    assert len(strategy_cfg_list) > 0
    assert isinstance(strategy_cfg_list[0], dict)
    strategy_cfg = StrategyConfig(**strategy_cfg_list[0])
    check_strategy_config(strategy_cfg)


def test_strategy_instance(strategy_cfg_list):
    with open(f'{MOCKS_DIR}/strategies/mock_strategy.yaml', 'r') as file:
        strategy_cfg_list = yaml.safe_load(file)
    check_strategy_configurations_dict(strategy_cfg_list)


def test_to_yaml(strategy_cfg_mock):
    yaml_str = strategy_cfg_mock.to_yaml()
    assert isinstance(yaml_str, str)
    strategy_cfg_dict_restored = yaml.safe_load(yaml_str)
    assert strategy_cfg_dict_restored['name'] == strategy_cfg_mock.name


def test_get_empty_strategy_config():
    strategy_cfg = get_empty_strategy_config('TEST')
    check_strategy_config(strategy_cfg)


