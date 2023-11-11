"""
Importing modules from user directory
"""
from collections import namedtuple
import importlib
import logging
import os
import sys
import inspect
from typing import Union

from catcher_bot.model.strategy import Strategy
from catcher_bot.model.connector import Connector
from catcher_bot.model.portfolio import Portfolio
from catcher_bot.model.module import Module

ModuleInitData = namedtuple("ModuleInitData", ['code', 'module', 'filepath'])

MODULE_FOLDER_MAX_DEPTH = 2


def process(modules_path: str, module_type: str, log: logging.Logger) -> list[Module]:
    """
    Importing modules
    """
    modules = []
    modules_fn = _prepare_modules_file_names_list(modules_path)
    for module_fn in modules_fn:
        module_instance = _get_module_instance(module_fn, module_type)
        if module_fn is not None:
            modules.append(module_instance)
            log.info(f"Found {module_type} \"{module_instance.name}\" [class \"{module_instance.code}\"] from "
                     f"file {module_instance.filepath}")
    return modules


def _prepare_modules_file_names_list(strategies_path: str) -> list:
    modules_fn = []
    for root, _, files in os.walk(strategies_path, topdown=True):
        if root[len(strategies_path):].count(os.sep) >= MODULE_FOLDER_MAX_DEPTH:
            break
        level_modules_fn = [os.path.join(root, fn) for fn in files if fn.endswith('.py')]
        modules_fn.extend(level_modules_fn)
    return modules_fn


def _get_module_instance(module_path: str, module_type: str) -> Union[Module, None]:
    if module_type == 'Strategy':
        module_class = Strategy
    elif module_type == 'Connector':
        module_class = Connector
    elif module_type == 'Portfolio':
        module_class = Portfolio
    else:
        raise ValueError(f"Unknown importing module type: {module_type}")
    module_name = os.path.basename(module_path)[:-3]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    _strategy_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = _strategy_module
    spec.loader.exec_module(_strategy_module)
    module_attributes = dir(_strategy_module)
    module_instance = None
    for attr_name in module_attributes:
        attribute_instance = getattr(_strategy_module, attr_name)
        if attr_name != module_type and inspect.isclass(attribute_instance) and \
           issubclass(attribute_instance, module_class):
            module_instance = module_class(code=attr_name, class_instance=attribute_instance)
            break
    return module_instance
