#pylint: disable=C0111,protected-access

import os
from dataclasses import is_dataclass
import logging
import pytest
import yaml
from catcher_bot.model.config.connector import ConnectorConfig
from tests.conftest import WORKING_FOLDER, CONFIGS_FOLDER, CONFIG_CONNECTOR_STOCK_FN
from tests.unit.model.config.base_test import check_configurations_dict, check_config

log = logging.getLogger(os.path.basename(__file__)[:-3])


@pytest.fixture()
def connector_cfg_dict():
    fn = f'{WORKING_FOLDER}/{CONFIGS_FOLDER}/{CONFIG_CONNECTOR_STOCK_FN}'
    with open(fn, 'r', encoding='utf-8') as file:
        strategy_cfg_d = yaml.safe_load(file)
    strategy_cfg_d['filepath'] = fn
    return strategy_cfg_d


def check_connector_configurations_dict(connector_cfg_d: dict):
    check_configurations_dict(connector_cfg_d)
    assert 'connector_code' in connector_cfg_d


@pytest.fixture()
def connector_cfg_mock(connector_cfg_dict) -> ConnectorConfig:
    return ConnectorConfig(**connector_cfg_dict)


def check_connector_config(connector_cfg: ConnectorConfig):
    check_config(connector_cfg)
    assert isinstance(connector_cfg, ConnectorConfig)
    assert isinstance(connector_cfg.connector_code, str)
    # assert isinstance(connector_cfg.connector_type, str)
    # assert isinstance(connector_cfg.market_type, list)
    # assert isinstance(connector_cfg.instrument_type, str)
    assert isinstance(connector_cfg.credentials, dict) or connector_cfg.credentials is None


def test_strategy_instance(connector_cfg_dict):
    check_connector_configurations_dict(connector_cfg_dict)
    strategy_cfg = ConnectorConfig(**connector_cfg_dict)
    check_connector_config(strategy_cfg)


def test_to_yaml(connector_cfg_mock):
    yaml_str = connector_cfg_mock.to_yaml()
    assert isinstance(yaml_str, str)
    strategy_cfg_dict_restored = yaml.safe_load(yaml_str)
    assert strategy_cfg_dict_restored['code'] == connector_cfg_mock.code
    assert strategy_cfg_dict_restored['connector_code'] == connector_cfg_mock.connector_code
    # assert strategy_cfg_dict_restored['config_type'] == connector_cfg_mock.config_type
    # assert 'market_type' in strategy_cfg_dict_restored
    # assert 'instrument_type' in strategy_cfg_dict_restored
    assert 'credentials' in strategy_cfg_dict_restored
    assert 'description' in strategy_cfg_dict_restored


