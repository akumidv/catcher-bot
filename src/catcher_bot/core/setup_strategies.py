from collections import namedtuple
import importlib
import logging
import os
import sys
import inspect
import yaml

from catcher_bot.model.strategy import Strategy
from catcher_bot.model.strategy_instance import StrategyInstance
from catcher_bot.model.strategy_config import StrategyConfig, get_empty_strategy_config

StrategyInitData = namedtuple("StrategyInitData", ['name', 'code', 'module'])

BOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

STRATEGY_NAME_ATTR = 'name'


def process(path: str, log: logging.Logger, dir_level: int = 0) -> list[StrategyInstance]:
    path = path if path.startswith('/') else os.path.normpath(os.path.join(BOT_DIR, path))
    strategy_dir_list = os.listdir(path)
    strategies = prepare_strategy_instances(path, strategy_dir_list, log)
    if strategies:
        sys.path.append(path)  # Possible unpredictable results if strategy will try to load modules that have the same name
    if dir_level == 0:
        sub_dirs = [os.path.normpath(os.path.join(path, dir_name)) for dir_name in strategy_dir_list if os.path.isdir(dir_name)]
        for dir_name in sub_dirs:
            dir_strategies = process(dir_name, log, dir_level + 1)
            if dir_strategies:
                strategies.extend(dir_strategies)
    return strategies


def prepare_strategy_instances(path: str, strategy_dir_list: list[str], log: logging.Logger) -> list[StrategyInstance]:
    modules_fn = [fn for fn in strategy_dir_list if fn.endswith('.py')]
    strategies = []
    for module_fn in modules_fn:
        module_path = os.path.normpath(os.path.join(path, module_fn))
        strategy_init = get_strategy_init_data(module_path, log)
        if not isinstance(strategy_init, StrategyInitData):
            continue
        strategy_configs_fn = [fn for fn in strategy_dir_list if module_fn.endswith('.yaml') and \
                               module_fn.startswith(module_fn[:-3])]
        strategy_configs = []
        if strategy_configs_fn:
            for strategy_cfg_fn in strategy_configs_fn:
                strategy_config = get_strategy_configuration(strategy_cfg_fn, strategy_init.code, log)
                strategy_configs.append(strategy_config)
        else:
            cfg_name = f'{strategy_init.code}_default'
            log.warning(f'Strategy {strategy_init.name} do not have configs, used empty config: {cfg_name}')
            strategy_configs.append(get_empty_strategy_config(cfg_name))
        strategy_inst = StrategyInstance(module=strategy_init.module, filepath=module_path,
                                         name=strategy_init.name, code=strategy_init.code, configs=strategy_configs)
        strategies.append(strategy_inst)
        log.info(f'Found strategy "{strategy_init.name}" [class "{strategy_init.code}"] from file {module_path} '
            f'with {len(strategy_configs)}')
    return strategies


def get_strategy_init_data(module_path: str, log: logging.Logger) -> StrategyInitData:
    module_name = os.path.basename(module_path)[:-3]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    _strategy_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = _strategy_module
    spec.loader.exec_module(_strategy_module)
    module_attributes = dir(_strategy_module)
    strategy_init = None
    for attr_name in module_attributes:
        attribute_instance = _strategy_module.__getattribute__(attr_name)
        if attr_name != 'Strategy' and inspect.isclass(attribute_instance) and issubclass(attribute_instance, Strategy):
            strategy_name = attr_name
            if STRATEGY_NAME_ATTR in dir(attribute_instance):
                strategy_name = getattr(attribute_instance, STRATEGY_NAME_ATTR)
            strategy_init = StrategyInitData(name=strategy_name, code=attr_name, module=attribute_instance)
            break
    return strategy_init


def get_strategy_configuration(config_fn: str, strategy_code: str, log: logging.Logger) -> StrategyConfig:
    print('###', config_fn)
    if os.path.isfile(config_fn):
        with open(config_fn, 'r') as file:
            strategy_cfg_dict = yaml.safe_load(file)
        strategy_cfg = StrategyConfig(**strategy_cfg_dict)
        log.info(f'For strategy "{strategy_code}" added config: {strategy_cfg.code}')
    else:
        cfg_name = f'{strategy_code}_default'
        log.warning(f'Strategy {strategy_code} do not have config with path {config_fn}, used empty config with name {cfg_name}')
        strategy_cfg = get_empty_strategy_config(cfg_name)
    return strategy_cfg

