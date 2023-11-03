
import importlib
import logging
import os
import sys
from typing import List, Type, Union

# from core.bot_context import BotContext
from model.strategy import Strategy
from model.strategy_instance import StrategyInstance
from model.strategy_config import StrategyConfig, get_empty_strategy_config
import inspect
import yaml

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



def init_strategies(path: str, log: logging.Logger) -> list[StrategyInstance]:
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
            attribute_instance = _strategy_module.__getattribute__(attr_name)
            if attr_name != 'Strategy' and inspect.isclass(attribute_instance) and issubclass(attribute_instance, Strategy):
                strategy_name = attr_name
                if STRATEGY_NAME_ATTR in dir(attribute_instance):
                    strategy_name = getattr(attribute_instance, STRATEGY_NAME_ATTR)

                strategy_configs = get_strategy_configurations(fn, attr_name, strategy_name, log)
                strategies.append(StrategyInstance(module=attribute_instance, filepath=fn, name=strategy_name,
                                                   code=attr_name, configs=strategy_configs))
                log.info(f'Added strategy "{strategy_name}" [class "{attr_name}"] from file {fn}')
    return strategies


def get_strategy_configurations(strategy_fn: str, attr_name: str, strategy_name: str, log: logging.Logger) -> list:
    config_fn = f'{strategy_fn[:-3]}.yaml'

    if os.path.isfile(config_fn):
        with open(config_fn, 'r') as file:
            cfg_list = yaml.safe_load(file)
        strategy_configs = [StrategyConfig(**strategy_cfg_dict) for strategy_cfg_dict in cfg_list]
        log.info(f'For strategy "{strategy_name}" found {len(strategy_configs)} configs: {[strategy_cfg.name for strategy_cfg in strategy_configs]}')
    else:
        cfg_name = f'{attr_name}_default'
        log.warning(f'Strategy {strategy_name} do not have config with path {config_fn}, used empty config with name {cfg_name}')
        strategy_configs = [get_empty_strategy_config(cfg_name)]
    return strategy_configs

