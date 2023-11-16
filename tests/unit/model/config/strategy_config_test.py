#pylint: disable=C0111,protected-access

import os
from dataclasses import is_dataclass
import logging
import pytest
import yaml
from catcher_bot.model.config.strategy import StrategyConfig#, ExchangeConfig, get_empty_strategy_config
from tests.conftest import WORKING_FOLDER, CONFIGS_FOLDER, CONFIG_STRATEGY_FN
from tests.unit.model.config.base_test import check_configurations_dict, check_config

log = logging.getLogger(os.path.basename(__file__)[:-3])


@pytest.fixture()
def strategy_cfg_dict():
    fn = f'{WORKING_FOLDER}/{CONFIGS_FOLDER}/{CONFIG_STRATEGY_FN}'
    with open(fn, 'r', encoding='utf-8') as file:
        strategy_cfg_d = yaml.safe_load(file)
    strategy_cfg_d['filepath'] = fn
    return strategy_cfg_d


def check_strategy_configurations_dict(strategy_cfg_d: dict):
    check_configurations_dict(strategy_cfg_d)
    assert 'strategy_code' in strategy_cfg_d
    assert 'parameters' in strategy_cfg_d


@pytest.fixture()
def strategy_cfg_mock(strategy_cfg_dict) -> StrategyConfig:
    return StrategyConfig(**strategy_cfg_dict)


def check_strategy_config(strategy_cfg: StrategyConfig):
    check_config(strategy_cfg)
    assert isinstance(strategy_cfg, StrategyConfig)
    assert isinstance(strategy_cfg.strategy_code, str)
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
    assert strategy_cfg_dict_restored['strategy_code'] == strategy_cfg_mock.strategy_code
    assert strategy_cfg_dict_restored['config_type'] == strategy_cfg_mock.config_type
    assert 'parameters' in strategy_cfg_dict_restored
    assert 'description' in strategy_cfg_dict_restored


