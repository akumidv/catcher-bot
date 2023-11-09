#pylint: disable=C0111,protected-access
import logging
import os
import pytest
from catcher_bot.core import setup_strategies
from catcher_bot.model.strategy_config import StrategyConfig
from catcher_bot.model.strategy import Strategy
from tests.unit.model.strategy_instance_test import check_strategy_instance
from tests.unit.model.strategy_config_test import check_strategy_config
from tests.conftest import WORKING_FOLDER


STRATEGIES_MOCK_PATH = f'{WORKING_FOLDER}/strategies'

log = logging.getLogger(os.path.basename(__file__)[:-3])


def test_process():
    strategies = setup_strategies.process(STRATEGIES_MOCK_PATH, log)
    assert isinstance(strategies, list)
    strategy_inst = strategies[0]
    check_strategy_instance(strategy_inst)


@pytest.mark.parametrize(("config_fn"), [("mock_strategy.yaml"), ("mock_strategy_wrong_name.yaml"),])
def test_get_strategy_configurations(config_fn):
    config_fn = f'{STRATEGIES_MOCK_PATH}/{config_fn}'
    strategy_config = setup_strategies.get_strategy_configuration(config_fn, 'mock', log)
    assert isinstance(strategy_config, StrategyConfig)
    check_strategy_config(strategy_config)


@pytest.mark.parametrize(("module_fn"), [("mock_strategy.py")])
def test_get_strategy_init_data(module_fn):
    module_path = f'{STRATEGIES_MOCK_PATH}/{module_fn}'
    strategy_init = setup_strategies.get_strategy_init_data(module_path, log)
    assert isinstance(strategy_init, setup_strategies.StrategyInitData)
    assert hasattr(strategy_init, 'name')
    assert hasattr(strategy_init, 'code')
    assert hasattr(strategy_init, 'module')
    assert isinstance(strategy_init.module, type)
    assert issubclass(strategy_init.module, Strategy)


def test_prepare_strategy_instances():
    path = STRATEGIES_MOCK_PATH
    strategies = setup_strategies.prepare_strategy_instances(path, os.listdir(path), log)
    assert isinstance(strategies, list)
    strategy_inst = strategies[0]
    check_strategy_instance(strategy_inst)
