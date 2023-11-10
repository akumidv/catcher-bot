#pylint: disable=C0111,protected-access
import os
import logging

from catcher_bot.model.strategy_module import StrategyModule
from catcher_bot.model.strategy import Strategy
from tests.resources.strategies.mock_strategy import MockStrategy

log = logging.getLogger(os.path.basename(__file__)[:-3])


def check_strategy_module(strategy_inst: StrategyModule):
    assert isinstance(strategy_inst, StrategyModule)
    assert isinstance(strategy_inst.filepath, str)
    assert issubclass(strategy_inst.module, Strategy)
    assert isinstance(strategy_inst.name, str)
    assert isinstance(strategy_inst.code, str)


def test_strategy_module():
    strategy_inst = StrategyModule(module=MockStrategy, filepath=__file__, name='Mock strategy',
                                   code='MockStrategy')
    check_strategy_module(strategy_inst)
