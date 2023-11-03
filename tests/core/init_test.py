import pytest
from core import init

from tests.context import bc
import logging
from tests.model.strategy_instance_test import check_strategy_instance
from tests.model.strategy_config_test import check_strategy_config
from tests.context import MOCKS_DIR
import os


STRATEGIES_MOCK_PATH = f'{MOCKS_DIR}/strategies'

log = logging.getLogger(os.path.basename(__file__)[:-3])

def test_init_strategies():
    strategies = init.init_strategies(STRATEGIES_MOCK_PATH, log)
    assert isinstance(strategies, list)
    strategy_inst = strategies[0]
    check_strategy_instance(strategy_inst)


@pytest.mark.parametrize(("strategy_fn"), [("mock_strategy.py"), ("mock_strategy_wrong_name.py"),])
def test_get_strategy_configurations(strategy_fn):
    strategy_fn = f'{STRATEGIES_MOCK_PATH}/{strategy_fn}'
    strategy_configs = init.get_strategy_configurations(strategy_fn, 'mock', 'mock strategy', log)
    assert isinstance(strategy_configs, list)
    assert len(strategy_configs) >= 1
    check_strategy_config(strategy_configs[0])


