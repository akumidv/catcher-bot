"""
Importing strategies modules from user directory
"""
from collections import namedtuple
import importlib
import logging
import os
import sys
import inspect
from typing import Union

from catcher_bot.model.strategy import Strategy
from catcher_bot.model.strategy_module import StrategyModule

StrategyInitData = namedtuple("StrategyInitData", ['name', 'code', 'module'])

STRATEGY_FOLDER_MAX_DEPTH = 2

STRATEGY_NAME_ATTR = 'name'

def process(strategies_path: str, log: logging.Logger) -> list[StrategyModule]:
    """
    Importing strategies modules
    """
    strategies = []
    modules_fn = _prepare_modules_file_names_list(strategies_path)
    for module_fn in modules_fn:
        strategy_instance = _prepare_strategy_instance(module_fn)
        if module_fn is not None:
            strategies.append(strategy_instance)
            log.info(f"Found strategy \"{strategy_instance.name}\" [class \"{strategy_instance.code}\"] from "
                     f"file {strategy_instance.filepath}")
    return strategies


def _prepare_modules_file_names_list(strategies_path: str) -> list:
    modules_fn = []
    for root, dirs, files in os.walk(strategies_path, topdown=True):
        if root[len(strategies_path):].count(os.sep) >= STRATEGY_FOLDER_MAX_DEPTH:
            break
        level_modules_fn = [os.path.join(root, fn) for fn in files if fn.endswith('.py')]
        modules_fn.extend(level_modules_fn)
    return modules_fn


def _prepare_strategy_instance(module_path: str) -> Union[StrategyModule, None]:
    strategy_init = _get_strategy_init_data(module_path)
    if not isinstance(strategy_init, StrategyInitData):
        return None
    strategy_instance = StrategyModule(module=strategy_init.module, filepath=module_path,
                                       name=strategy_init.name, code=strategy_init.code)
    return strategy_instance


def _get_strategy_init_data(module_path: str,) -> StrategyInitData:
    module_name = os.path.basename(module_path)[:-3]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    _strategy_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = _strategy_module
    spec.loader.exec_module(_strategy_module)
    module_attributes = dir(_strategy_module)
    strategy_init = None
    for attr_name in module_attributes:
        attribute_instance = getattr(_strategy_module, attr_name)
        if attr_name != 'Strategy' and inspect.isclass(attribute_instance) and issubclass(attribute_instance, Strategy):
            strategy_name = attr_name
            if hasattr(attribute_instance, STRATEGY_NAME_ATTR):
                strategy_name = getattr(attribute_instance, STRATEGY_NAME_ATTR)
            strategy_init = StrategyInitData(name=strategy_name, code=attr_name, module=attribute_instance)
            break
    return strategy_init
