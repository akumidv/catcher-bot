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
from catcher_bot.core import logger
from catcher_bot.model.module.loader import ModuleLoader
from catcher_bot.model.namespace import ModuleType
from catcher_bot.model.module.type import MODULE_CLASSES

ModuleInitData = namedtuple("ModuleInitData", ['code', 'module', 'filepath'])

modules_types = ('strategy', 'portfolio', 'connector')
Modules = namedtuple('Modules', modules_types)

MODULE_FOLDER_MAX_DEPTH = 2
LOG_NAME = 'init modules'

log = logger.get_def_logger(LOG_NAME)

def import_base_modules(bot_root: str) -> Modules:
    loaded_modules = Modules(strategy=load_modules(f"{bot_root}/strategies", ModuleType.STRATEGY),
                             connector=load_modules(f"{bot_root}/interface", ModuleType.CONNECTOR),
                             portfolio=load_modules(f"{bot_root}/portfolio", ModuleType.PORTFOLIO))
    return loaded_modules


def import_modules(modules_path: dict) -> Modules:
    """
    Importing modules
    """

    strategies_path = modules_path.get('strategies') if modules_path.get('strategies') is None or \
                                                        modules_path['strategies'].startswith(os.path.sep) else \
                      os.path.normpath(os.path.join(modules_path['__working_dir'], modules_path['strategies']))
    portfolio_path = modules_path.get('portfolio') if modules_path.get('portfolio') is None or \
                                                      modules_path['portfolio'].startswith(os.path.sep) else \
                     os.path.normpath(os.path.join(modules_path['__working_dir'], modules_path['portfolio']))
    connector_path = modules_path.get('connector') if modules_path.get('connector') is None or \
                                                      modules_path['connector'].startswith(os.path.sep) else \
                     os.path.normpath(os.path.join(modules_path['__working_dir'], modules_path['connector']))


    loaded_modules = Modules(strategy=load_modules(strategies_path, ModuleType.STRATEGY) if strategies_path else None,
                             portfolio=load_modules(portfolio_path, ModuleType.PORTFOLIO) if portfolio_path else None,
                             connector=load_modules(connector_path, ModuleType.CONNECTOR) if connector_path else None)

    return loaded_modules


def load_modules(modules_path: str, module_type: ModuleType) -> list[ModuleLoader]:
    """
    Load modules by type from dirrectory
    """
    modules = []
    print(module_type.name, modules_path)
    modules_fn = _prepare_modules_file_names_list(modules_path)
    for module_fn in modules_fn:
        print(module_fn)
        module_instance = _get_module_instance(module_fn, module_type)
        if module_instance is not None:
            modules.append(module_instance)
            log.info(f"Found {module_type.name} \"{module_instance.code}\" from "
                     f"file {module_instance.filepath}")
    return modules

def _prepare_modules_file_names_list(modules_path: str) -> list:
    modules_fn = []
    for root, _, files in os.walk(modules_path, topdown=True):
        if root[len(modules_path):].count(os.sep) >= MODULE_FOLDER_MAX_DEPTH:
            break
        level_modules_fn = [os.path.join(root, fn) for fn in files if fn.endswith('.py')]
        modules_fn.extend(level_modules_fn)
    return modules_fn


def _get_module_instance(module_path: str, module_type: ModuleType) -> Union[ModuleLoader, None]:
    module_class = MODULE_CLASSES.get(module_type)
    if module_class is None:
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
        if not module_type.is_equal_name(attr_name) and inspect.isclass(attribute_instance) and \
           issubclass(attribute_instance, module_class):
            module_instance = ModuleLoader(code=attr_name, class_instance=attribute_instance,
                                           filepath=module_path)
            break
    return module_instance
