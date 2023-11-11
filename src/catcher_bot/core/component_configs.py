"""
Configure module. Loading and parsing configs from bot configs and folder with bot configure
"""
import os
from collections import namedtuple

import yaml

from catcher_bot.core import logger
from catcher_bot.model.config.strategy import StrategyConfig
from catcher_bot.model.config.portfolio import PortfolioConfig
from catcher_bot.model.config.connector import ConnectorConfig
from catcher_bot.model.config.base import BaseConfig
from catcher_bot.model.namespace import ModuleType

LOG_NAME = 'init'
ENV_PREFIX = 'BOT'

log = logger.get_def_logger(LOG_NAME)

components_types = ('strategy', 'portfolio', 'exchange')
ComponentConfigs = namedtuple('ComponentConfigs', components_types)


def load_configs(bot_cfg: dict) -> ComponentConfigs:
    """
    Loading all component configurations from path that set in bot config yaml
    """
    root_config_path = os.path.join(bot_cfg['path']['__working_dir'], bot_cfg['path']['config'])
    log.debug(f"Path to load component configs: {root_config_path}")
    components_cfg = ComponentConfigs(strategy={}, portfolio={}, exchange={})
    for path, _, files in os.walk(root_config_path):
        for fn in files:
            if not str(fn).endswith('.yaml'):
                continue
            cfg_path = str(os.path.join(path, fn))
            with open(cfg_path, 'r', encoding='utf-8') as fd:
                cfg = yaml.safe_load(fd)
            if isinstance(cfg, list):
                for cfg_item in cfg:
                    components_cfg = _update_components_cfg(components_cfg, cfg_item, cfg_path)
            else:
                components_cfg = _update_components_cfg(components_cfg, cfg, cfg_path)
    components_config_instances = ComponentConfigs(strategy=_init_config(components_cfg.strategy, ModuleType.STRATEGY),
                                                   portfolio=_init_config(components_cfg.portfolio,
                                                                          ModuleType.PORTFOLIO),
                                                   connector=_init_config(components_cfg.exchange,
                                                                          ModuleType.CONNECTOR))
    return components_config_instances


def _init_config(configs_dict: dict, config_class_type: ModuleType) -> dict:
    """
    Initialization portfolio configs from dict
    """
    instances = {}
    for config_code in configs_dict:
        if config_class_type == ModuleType.STRATEGY:
            instances[config_code] = StrategyConfig(**configs_dict[config_code])
        elif config_class_type == ModuleType.PORTFOLIO:
            instances[config_code] = PortfolioConfig(**configs_dict[config_code])
        elif config_class_type == ModuleType.CONNECTOR:
            instances[config_code] = ConnectorConfig(**configs_dict[config_code])
        else:
            raise ValueError(f"Unknown config class type {ModuleType}")
    return instances


def _update_components_cfg(components_cfg: ComponentConfigs, comp_cfg: dict, cfg_path: str, ) -> ComponentConfigs:
    """
    Updating components configs by component type and code
    """
    if _check_configuration_structure(comp_cfg, cfg_path):
        if comp_cfg['code'] in getattr(components_cfg, comp_cfg['config_type']):
            log.warning(f"Component config type \"{comp_cfg['config_type']}\" with code \"{comp_cfg['code']}\" "
                        f"from {cfg_path} already loaded. Skipped")
        else:
            comp_cfg = _enrich_config(comp_cfg, cfg_path)
            getattr(components_cfg, comp_cfg['config_type'])[comp_cfg['code']] = comp_cfg
            log.debug(f"Loading component config \"{comp_cfg['config_type']}\" \"{comp_cfg['code']}\" from {cfg_path}")
    return components_cfg

def _enrich_config(comp_cfg: dict, cfg_path):
    comp_cfg['filepath'] = cfg_path
    if 'description' not in cfg_path:
        comp_cfg['description'] = ''
    return comp_cfg


def _check_configuration_structure(comp_cfg: dict, cfg_path: str) -> bool:
    """
    Verifying mandatory configuration structure

    """
    status = True
    if not isinstance(comp_cfg, dict):
        log.warning(f"Component config {cfg_path} should be dictionary, not the {type(comp_cfg)}")
        status = False
    elif 'config_type' not in comp_cfg:
        log.warning(f"Component config {cfg_path} should have \"config_type\" field")
        status = False
    elif comp_cfg['config_type'] not in components_types:
        log.warning(f"{cfg_path} config type should be one of \"{components_types}\", "
                   f"current config type is \"{comp_cfg['config_type']}\"")
        status = False
    elif 'code' not in comp_cfg:
        log.warning(f"Component config {cfg_path} should have \"code\" field")
        status = False
    return status
