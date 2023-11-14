#pylint: disable=C0111,protected-access

import os
from dataclasses import is_dataclass
import logging
import pytest
import yaml
from catcher_bot.model.config.strategy import StrategyConfig#, ExchangeConfig, get_empty_strategy_config
from tests.conftest import WORKING_FOLDER, CONFIGS_FOLDER, STRATEGY_FOLDER


log = logging.getLogger(os.path.basename(__file__)[:-3])


@pytest.fixture()
def strategy_cfg_dict():
    fn = f'{WORKING_FOLDER}/{CONFIGS_FOLDER}/mock_strategy.yaml'
    with open(fn, 'r', encoding='utf-8') as file:
        strategy_cfg_d = yaml.safe_load(file)
    strategy_cfg_d['filepath'] = fn
    return strategy_cfg_d

def check_strategy_configurations_dict(strategy_cfg_d: dict):
    assert isinstance(strategy_cfg_d, dict)
    assert 'code' in strategy_cfg_d
    assert 'config_type' in strategy_cfg_d
    assert 'description' in strategy_cfg_d
    assert 'filepath' in strategy_cfg_d


@pytest.fixture()
def strategy_cfg_mock(strategy_cfg_dict) -> StrategyConfig:
    return StrategyConfig(**strategy_cfg_dict)


def check_strategy_config(strategy_cfg: StrategyConfig):
    assert is_dataclass(strategy_cfg)
    assert not isinstance(strategy_cfg, type)
    assert isinstance(strategy_cfg, StrategyConfig)
    assert isinstance(strategy_cfg.code, str)
    assert isinstance(strategy_cfg.config_type, str)
    assert isinstance(strategy_cfg.parameters, dict) or strategy_cfg.parameters is None



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

