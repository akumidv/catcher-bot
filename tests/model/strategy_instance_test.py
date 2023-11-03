import pytest
from model.strategy_instance import StrategyInstance
from model.strategy import Strategy
from tests.model.strategy_config_test import strategy_cfg_mock, strategy_cfg_dict, strategy_cfg_list
from tests._mocks.strategies.mock_strategy import MockStrategy
import yaml
import logging
import os


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


