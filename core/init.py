
import importlib
import logging
import os
import sys
from typing import List, Type

from core.bot_context import BotContext
from model.strategy import Strategy
import inspect

BOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

STRATEGY_NAME_ATTR = 'name'

def init_exchange(exchange_name, credential, is_socket: bool = False, market_type: str = 'stock'):
    exchange_module = importlib.import_module(f'interface.exchange.{exchange_name}_class', exchange_name) #'subscriber')#'interface/exchange', name)
    class_name = exchange_name[0].upper() + exchange_name[1:].lower()
    if is_socket:
        class_name += 'Socket'
    if market_type == 'futures':
        class_name += 'Futures'
    exchange = exchange_module.__getattribute__(class_name)(credential, logging.getLogger(exchange_name))
    # TODO
    return exchange


def init_strategies(bc: BotContext, path: str) -> list[Type[Strategy]]:
    path = path if path.startswith('/') else os.path.normpath(os.path.join(BOT_DIR, path))
    sys.path.append(path)
    modules_fn = [os.path.normpath(os.path.join(path, fn)) for fn in os.listdir(path) if fn.endswith('.py')]
    strategies = []
    for fn in modules_fn:
        module_name = fn[:-3]
        spec = importlib.util.spec_from_file_location(fn[:-3], fn)
        _strategy_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = _strategy_module
        spec.loader.exec_module(_strategy_module)

        module_attributes = dir(_strategy_module)
        for attr_name in module_attributes:
            module_attr = _strategy_module.__getattribute__(attr_name)
            if attr_name != 'Strategy' and inspect.isclass(module_attr) and issubclass(module_attr, Strategy):
                strategy_name = attr_name
                if STRATEGY_NAME_ATTR in dir(module_attr):
                    strategy_name = getattr(module_attr, STRATEGY_NAME_ATTR)
                bc.log.info(f'Added strategy "{strategy_name}" [class "{attr_name}"] from strategy module {module_name}')
                strategies.append(module_attr)
    return strategies

