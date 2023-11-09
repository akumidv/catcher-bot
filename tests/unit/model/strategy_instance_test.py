import os
import logging
import pytest
import yaml
from catcher_bot.model.strategy_instance import StrategyInstance
from catcher_bot.model.strategy import Strategy
from tests.model.strategy_config_test import strategy_cfg_mock, strategy_cfg_dict
from tests.resources.strategies.mock_strategy import MockStrategy


log = logging.getLogger(os.path.basename(__file__)[:-3])

def check_strategy_instance(strategy_inst: StrategyInstance):
    assert isinstance(strategy_inst, StrategyInstance)
    assert isinstance(strategy_inst.filepath, str)
    assert issubclass(strategy_inst.module, Strategy)
    assert isinstance(strategy_inst.name, str)
    assert isinstance(strategy_inst.code, str)
    assert isinstance(strategy_inst.configs, list)


def test_strategy_instance(strategy_cfg_mock):
    strategy_inst = StrategyInstance(module=MockStrategy, filepath=__file__, name='Mock strategy',
                                     code='MockStrategy', configs=[strategy_cfg_mock])
    check_strategy_instance(strategy_inst)
    print(strategy_inst)


