#pylint: disable=C0111,protected-access
import os
from dataclasses import is_dataclass
import logging
import pytest
import yaml
from catcher_bot.model.config.base import BaseConfig


log = logging.getLogger(os.path.basename(__file__)[:-3])


@pytest.fixture()
def cfg_dict():
    config_dict = {
        'code': 'CONFIG_MOCK',
        'config_type': 'mock_type',
        'description': 'MOCK description',
        'filepath': 'none.yaml'
    }
    return config_dict

def check_configurations_dict(strategy_cfg_d: dict):
    assert isinstance(strategy_cfg_d, dict)
    assert 'code' in strategy_cfg_d
    assert 'config_type' in strategy_cfg_d
    assert 'description' in strategy_cfg_d
    assert 'filepath' in strategy_cfg_d


@pytest.fixture()
def cfg_mock(cfg_dict) -> BaseConfig:
    return BaseConfig(**cfg_dict)


def check_config(strategy_cfg: BaseConfig):
    assert is_dataclass(strategy_cfg)
    assert not isinstance(strategy_cfg, type)
    assert isinstance(strategy_cfg, BaseConfig)
    assert isinstance(strategy_cfg.code, str)
    assert isinstance(strategy_cfg.config_type, str)


def test_config_instance(cfg_dict):
    check_configurations_dict(cfg_dict)
    strategy_cfg = BaseConfig(**cfg_dict)
    check_config(strategy_cfg)


def test_to_yaml(cfg_mock):
    yaml_str = cfg_mock.to_yaml()
    assert isinstance(yaml_str, str)
    strategy_cfg_dict_restored = yaml.safe_load(yaml_str)
    assert strategy_cfg_dict_restored['code'] == cfg_mock.code
    print(yaml_str)
    print(strategy_cfg_dict_restored)

