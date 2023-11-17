#pylint: disable=C0111,protected-access

import os
from dataclasses import is_dataclass
import logging
import pytest
import yaml
from catcher_bot.model.config.portfolio import PortfolioConfig, CompositionConfig, ActionConfig, SourceConfig
from tests.conftest import WORKING_FOLDER, CONFIGS_FOLDER, CONFIG_PORTFOLIO_FN
from tests.unit.model.config.base_test import check_configurations_dict, check_config

log = logging.getLogger(os.path.basename(__file__)[:-3])


@pytest.fixture()
def portfolio_cfg_dict() -> dict:
    fn = f'{WORKING_FOLDER}/{CONFIGS_FOLDER}/{CONFIG_PORTFOLIO_FN}'
    with open(fn, 'r', encoding='utf-8') as file:
        strategy_cfg_d = yaml.safe_load(file)
    strategy_cfg_d['filepath'] = fn
    return strategy_cfg_d

########################
# Sources
#######################
def check_source_config_dict(source_dict):
    assert 'connector_config_code' in source_dict
    assert isinstance(source_dict['connector_config_code'], str)
    assert 'assets' in source_dict
    assert isinstance(source_dict['assets'], list)


def test_source_config_dict(portfolio_cfg_dict):
    source_dict = portfolio_cfg_dict['composition'][0]['sources'][0]
    check_source_config_dict(source_dict)


def check_source_config(source_dict: SourceConfig):
    assert hasattr(source_dict, 'connector_config_code')
    assert isinstance(source_dict.connector_config_code, str)
    assert hasattr(source_dict, 'assets')
    assert isinstance(source_dict.assets, list)
    assert len(source_dict.assets) > 0
    assert hasattr(source_dict, 'common')
    assert source_dict.black_list is None or isinstance(source_dict.common, dict)
    assert hasattr(source_dict, 'black_list')
    assert source_dict.black_list is None or isinstance(source_dict.black_list, list)


def test_source_config_class(portfolio_cfg_dict):
    source_dict = portfolio_cfg_dict['composition'][0]['sources'][0]
    source_cfg = SourceConfig(**source_dict)
    check_source_config(source_cfg)

    source_dict = portfolio_cfg_dict['composition'][0]['sources'][0]
    del source_dict['black_list']
    source_cfg = SourceConfig(**source_dict)
    check_source_config(source_cfg)

    del source_dict['common']
    source_cfg = SourceConfig(**source_dict)
    check_source_config(source_cfg)

########################
# Actions
#######################

def check_action_config(action_cfg: ActionConfig):
    assert hasattr(action_cfg, 'connector_config_code')
    assert isinstance(action_cfg.connector_config_code, str)


def test_action_config_class(portfolio_cfg_dict):
    action_dict = portfolio_cfg_dict['composition'][0]['actions'][0]
    action_cfg = ActionConfig(**action_dict)
    check_action_config(action_cfg)



########################
# Composition
#######################

def check_composition_config(composition_cfg):
    assert hasattr(composition_cfg, 'strategy_config_code')
    assert isinstance(composition_cfg.strategy_config_code, str)
    assert hasattr(composition_cfg, 'ratio')
    assert isinstance(composition_cfg.ratio, float)
    assert hasattr(composition_cfg, 'sources')
    assert isinstance(composition_cfg.sources, list)
    assert len(composition_cfg.sources) > 0
    assert hasattr(composition_cfg, 'actions')
    assert len(composition_cfg.actions) > 0
    for source_cfg in composition_cfg.sources:
        check_source_config(source_cfg)
    for action_cfg in composition_cfg.actions:
        check_action_config(action_cfg)


def test_composition_config_class(portfolio_cfg_dict):
    composition_dict = portfolio_cfg_dict['composition'][0]
    composition_cfg = CompositionConfig(**composition_dict)
    check_composition_config(composition_cfg)


########################
# Portfolio
#######################

@pytest.fixture()
def portfolio_cfg_mock(portfolio_cfg_dict) -> PortfolioConfig:
    return PortfolioConfig(**portfolio_cfg_dict)


def check_portfolio_configurations_dict(portfolio_cfg_d: dict):
    check_configurations_dict(portfolio_cfg_d)
    assert 'composition' in portfolio_cfg_d
    source_dict = portfolio_cfg_d['composition'][0]['sources'][0]
    check_source_config_dict(source_dict)


def check_portfolio_config(portfolio_cfg: PortfolioConfig):
    check_config(portfolio_cfg)
    assert isinstance(portfolio_cfg, PortfolioConfig)
    assert isinstance(portfolio_cfg.composition, list)
    assert len(portfolio_cfg.composition) > 0
    for composition_cfg in portfolio_cfg.composition:
        check_composition_config(composition_cfg)


def test_portfolio_instance(portfolio_cfg_dict):
    check_portfolio_configurations_dict(portfolio_cfg_dict)
    portfolio_cfg = PortfolioConfig(**portfolio_cfg_dict)
    check_portfolio_config(portfolio_cfg)


def test_to_yaml(portfolio_cfg_mock):
    yaml_str = portfolio_cfg_mock.to_yaml()
    assert isinstance(yaml_str, str)
    portfolio_cfg_dict_restored = yaml.safe_load(yaml_str)
    assert portfolio_cfg_dict_restored['code'] == portfolio_cfg_mock.code
    assert 'description' in portfolio_cfg_dict_restored
    assert 'composition' in portfolio_cfg_dict_restored
    assert len(portfolio_cfg_dict_restored['composition']) == len(portfolio_cfg_mock.composition)



