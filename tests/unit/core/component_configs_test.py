#pylint: disable=C0111,protected-access
import logging

from catcher_bot.core import component_configs
from catcher_bot.model.config.strategy import StrategyConfig
from catcher_bot.model.namespace import ModuleType, get_names

from tests.conftest import CONFIG_STRATEGY_FN
from tests.unit.model.config.strategy_config_test import strategy_cfg_dict

LOGGER = logging.getLogger(__name__)


def test_load_configs(bot_config):
    components_cfg = component_configs.load_configs(bot_config['path'])
    assert sorted([name.lower() for name in get_names(ModuleType)]) == sorted(list(component_configs.components_types))

    assert isinstance(getattr(components_cfg, 'strategy'), dict)
    assert isinstance(getattr(components_cfg, 'portfolio'), dict)
    assert isinstance(getattr(components_cfg, 'connector'), dict)


def test__init_configs(strategy_cfg_dict):
    configs_dict = {}
    configs_dict[strategy_cfg_dict['code']] = strategy_cfg_dict
    cfg = component_configs._process_configs_fabric(configs_dict, ModuleType.STRATEGY)
    instance_key = list(cfg.keys())[0]
    assert isinstance(cfg[instance_key], StrategyConfig)



def test__update_components_cfg(caplog, comp_strategy_config):
    components_cfg = component_configs.ComponentConfigs({}, {}, {})
    component_configs._update_components_cfg(components_cfg, comp_strategy_config, CONFIG_STRATEGY_FN)
    strategies = getattr(components_cfg, 'strategy')
    strategy_code = comp_strategy_config['code']
    assert strategy_code in strategies
    assert 'filepath' in strategies[strategy_code]
    assert CONFIG_STRATEGY_FN == strategies[strategy_code]['filepath']
    with caplog.at_level(logging.WARNING):
        component_configs._update_components_cfg(components_cfg, comp_strategy_config, CONFIG_STRATEGY_FN)
    assert f"with code \"{strategy_code}\" from" in caplog.text


def test__check_configuration_structure(caplog, comp_strategy_config):
    component_configs._check_configuration_structure(comp_strategy_config, CONFIG_STRATEGY_FN)
    wrong_strategy_config_fn = '__mock_strategy_filepath.yaml'
    with caplog.at_level(logging.WARNING):
        component_configs._check_configuration_structure([comp_strategy_config], wrong_strategy_config_fn)
    assert "should be dictionary, not the" in caplog.text
    with caplog.at_level(logging.WARNING):
        component_configs._check_configuration_structure({'config_type_wrong': 'strategy'}, wrong_strategy_config_fn)
    assert "should have \"config_type\"" in caplog.text
    with caplog.at_level(logging.WARNING):
        component_configs._check_configuration_structure({'config_type': 'strategy_wrong'}, wrong_strategy_config_fn)
    assert "config type should be one of " in caplog.text
    with caplog.at_level(logging.WARNING):
        component_configs._check_configuration_structure({'config_type': 'strategy', 'code_wrong': 'CODE'},
                                                         wrong_strategy_config_fn)
    assert "should have \"code\" field" in caplog.text


def test__enrich_config(strategy_cfg_dict):
    comp_cfg = strategy_cfg_dict.copy()
    del comp_cfg['description']
    comp_cfg = component_configs._enrich_config(comp_cfg, CONFIG_STRATEGY_FN)
    assert 'description' in comp_cfg
    comp_cfg = strategy_cfg_dict.copy()
    del comp_cfg['filepath']
    comp_cfg = component_configs._enrich_config(comp_cfg, CONFIG_STRATEGY_FN)
    assert 'filepath' in comp_cfg and comp_cfg['filepath'] == CONFIG_STRATEGY_FN


def test_process_configs_fabric(strategy_cfg_dict):
    instances = component_configs._process_configs_fabric({f"{strategy_cfg_dict['code']}": strategy_cfg_dict},
                                                          ModuleType.STRATEGY)
    assert isinstance(instances, dict)
    assert strategy_cfg_dict['code'] in instances
    assert isinstance(instances[strategy_cfg_dict['code']], StrategyConfig)


def test_process_configs_fabric_wrong(caplog, strategy_cfg_dict):
    strategy_cfg_dict['__wrong_attribute'] = 'WRONG ATTRIBUTE VALUE'
    with caplog.at_level(logging.WARNING):
        component_configs._process_configs_fabric({f"{strategy_cfg_dict['code']}": strategy_cfg_dict},
                                                  ModuleType.STRATEGY)
    assert "contain unknown attributes" in caplog.text
    assert "__wrong_attribute" in caplog.text

