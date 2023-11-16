#pylint: disable=C0111,protected-access
import os
import logging

import pytest

from catcher_bot.core import import_modules
from catcher_bot.model.module.strategy import Strategy
from catcher_bot.model.namespace import ModuleType

from tests.unit.model.module.loader_test import check_module
from tests.conftest import WORKING_FOLDER, STRATEGY_FOLDER, STRATEGY_FN


STRATEGIES_MOCK_PATH = f'{WORKING_FOLDER}/{STRATEGY_FOLDER}'

log = logging.getLogger(os.path.basename(__file__)[:-3])


def test_process_for_strategy():
    strategies = import_modules.process(STRATEGIES_MOCK_PATH, ModuleType.STRATEGY, log)
    assert isinstance(strategies, list)
    assert len(strategies) > 0
    strategy_inst = strategies[0]
    check_module(strategy_inst)


def test__prepare_modules_file_names_list():
    modules_fn = import_modules._prepare_modules_file_names_list(WORKING_FOLDER)
    assert isinstance(modules_fn, list)
    assert len(modules_fn) > 0
    for module_fn in modules_fn:
        assert WORKING_FOLDER in module_fn
        assert module_fn[len(WORKING_FOLDER):].count(os.sep) <= import_modules.MODULE_FOLDER_MAX_DEPTH


def test__prepare_strategy_instance():
    strategy_fn = f"{STRATEGIES_MOCK_PATH}/{STRATEGY_FN}"
    assert os.path.isfile(strategy_fn)
    strategy_instance = import_modules._get_module_instance(strategy_fn, ModuleType.STRATEGY)
    check_module(strategy_instance)


def test__prepare_strategy_instance_wrong():
    strategy_instance = import_modules._get_module_instance(__file__, ModuleType.STRATEGY)
    assert strategy_instance is None

