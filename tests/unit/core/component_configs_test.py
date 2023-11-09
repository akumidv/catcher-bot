#pylint: disable=C0111,protected-access
import logging
from catcher_bot.core import component_configs
from tests.conftest import CONFIG_STRATEGY_FN

LOGGER = logging.getLogger(__name__)

def test_load_configs(bot_config):
    components_cfg = component_configs.load_configs(bot_config)
    print(components_cfg)
    assert isinstance(getattr(components_cfg, 'strategy'), dict)
    assert isinstance(getattr(components_cfg, 'portfolio'), dict)
    assert isinstance(getattr(components_cfg, 'exchange'), dict)


def test__update_components_cfg(caplog, comp_strategy_config):
    components_cfg = component_configs.ComponentConfigs({}, {}, {})
    component_configs._update_components_cfg(components_cfg, comp_strategy_config, CONFIG_STRATEGY_FN)
    strategies = getattr(components_cfg, 'strategy')
    strategy_code = comp_strategy_config['code']
    assert strategy_code in strategies
    assert '__filepath' in strategies[strategy_code]
    assert CONFIG_STRATEGY_FN == strategies[strategy_code]['__filepath']
    with caplog.at_level(logging.WARNING):
        component_configs._update_components_cfg(components_cfg, comp_strategy_config, CONFIG_STRATEGY_FN)
    assert f"with code \"{strategy_code}\" from" in caplog.text


def test__check_configuration_structure(caplog, comp_strategy_config):
    component_configs._check_configuration_structure(comp_strategy_config, CONFIG_STRATEGY_FN)
    with caplog.at_level(logging.WARNING):
        component_configs._check_configuration_structure([comp_strategy_config], CONFIG_STRATEGY_FN)
    assert "should be dictionary, not the" in caplog.text
    with caplog.at_level(logging.WARNING):
        component_configs._check_configuration_structure({'config_type_wrong': 'strategy'}, CONFIG_STRATEGY_FN)
    assert "should have \"config_type\"" in caplog.text
    with caplog.at_level(logging.WARNING):
        component_configs._check_configuration_structure({'config_type': 'strategy_wrong'}, CONFIG_STRATEGY_FN)
    assert "config type should be one of " in caplog.text
    with caplog.at_level(logging.WARNING):
        component_configs._check_configuration_structure({'config_type': 'strategy', 'code_wrong': 'CODE'},
                                                         CONFIG_STRATEGY_FN)
    assert "should have \"code\" field" in caplog.text
