#pylint: disable=C0111,protected-access
import os
import logging

import pytest

from catcher_bot.core import import_strategies
from catcher_bot.model.strategy import Strategy

from tests.unit.model.strategy_module_test import  check_strategy_module
from tests.conftest import WORKING_FOLDER, STRATEGY_FOLDER, STRATEGY_FN


STRATEGIES_MOCK_PATH = f'{WORKING_FOLDER}/{STRATEGY_FOLDER}'

log = logging.getLogger(os.path.basename(__file__)[:-3])


def test_process():
    strategies = import_strategies.process(STRATEGIES_MOCK_PATH, log)
    assert isinstance(strategies, list)
    assert len(strategies) > 0
    strategy_inst = strategies[0]
    check_strategy_module(strategy_inst)


def test__prepare_modules_file_names_list():
    modules_fn = import_strategies._prepare_modules_file_names_list(WORKING_FOLDER)
    assert isinstance(modules_fn, list)
    assert len(modules_fn) > 0
    for module_fn in modules_fn:
        assert WORKING_FOLDER in module_fn
        assert module_fn[len(WORKING_FOLDER):].count(os.sep) <= import_strategies.MODULE_FOLDER_MAX_DEPTH

def test__prepare_strategy_instance():
    strategy_instance = import_strategies._get_module_instance(f"{STRATEGIES_MOCK_PATH}/{STRATEGY_FN}")
    check_strategy_module(strategy_instance)


def test__prepare_strategy_instance_wrong():
    strategy_instance = import_strategies._get_module_instance(__file__)
    assert strategy_instance is None


@pytest.mark.parametrize(("module_fn"), [("mock_strategy.py")])
def test_get_strategy_init_data(module_fn):
    module_path = f'{STRATEGIES_MOCK_PATH}/{module_fn}'
    strategy_init = import_strategies._get_strategy_init_data(module_path)
    assert isinstance(strategy_init, import_strategies.ModuleInitData)
    assert hasattr(strategy_init, 'name')
    assert hasattr(strategy_init, 'code')
    assert hasattr(strategy_init, 'module')
    assert isinstance(strategy_init.module, type)
    assert issubclass(strategy_init.module, Strategy)
