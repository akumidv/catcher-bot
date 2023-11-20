#pylint: disable=C0111,protected-access
import os
import logging

from catcher_bot.model.module.loader import ModuleLoader
from catcher_bot.model.module.strategy import Strategy
from tests.resources.strategies.mock_strategy import MockStrategy

log = logging.getLogger(os.path.basename(__file__)[:-3])


def check_module(strategy_inst: ModuleLoader, class_type: type = Strategy):
    assert isinstance(strategy_inst, ModuleLoader)
    assert isinstance(strategy_inst.filepath, str)
    assert issubclass(strategy_inst.class_instance, class_type)
    assert isinstance(strategy_inst.code, str)


def test_strategy_module():
    strategy_inst = ModuleLoader(class_instance=MockStrategy, filepath=__file__, code='MockStrategy')
    check_module(strategy_inst)
