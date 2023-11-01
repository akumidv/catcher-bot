
import importlib
import logging
import os
import sys
from core.bot_context import BotContext
from model.strategy import Strategy


BOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


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


def init_strategies(bc: BotContext, path: str) -> list[Strategy]:
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
        try:
            class_name = _strategy_module.__getattribute__('__strategy_name__')
            try:
                _strategy_class = _strategy_module.__getattribute__(class_name)
                strategies.append(_strategy_class)
            except AttributeError:
                bc.log.error(
                    f'The strategy module {module_name} from file {fn} do not have class name {class_name}" that set '
                    f'in the module __strategy_name__" parameter '
                    f'Strategy loading is skipped')
        except AttributeError:
            bc.log.error(f'The strategy module {module_name} from file {fn} do not have "__strategy_name__" parameter '
                         f'that contain strategy class name or the class itself. Strategy loading is skipped')

    return strategies