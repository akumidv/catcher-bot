"""
Configure module. Loading and parsing configs from bot configs and folder with bot configure
"""
import os

from collections import namedtuple

import yaml

from catcher_bot.core import logger

ENV_PREFIX = 'BOT'
LOG_NAME = 'init'

log = logger.get_def_logger(LOG_NAME)
components_types = ('strategy', 'portfolio', 'exchange')
ComponentConfigs = namedtuple('ComponentConfigs', components_types)


def load_configs(bot_cfg: dict) -> ComponentConfigs:
    """
    Load all component configurations from path that set in bot config yaml
    """
    root_config_path = os.path.join(bot_cfg['__working_dir'], bot_cfg['path']['config'])
    log.debug(f"Path to load component configs: {root_config_path}")
    components_cfg = ComponentConfigs(strategy={}, portfolio={}, exchange={})
    for path, _, files in os.walk(root_config_path):
        for fn in files:
            print(fn)
            if not str(fn).endswith('.yaml'):
                continue
            cfg_path = os.path.join(path, fn)
            with open(cfg_path, 'r', encoding='utf-8') as fd:
                cfg = yaml.safe_load(fd)
            if isinstance(cfg, list):
                for cfg_item in cfg:
                    components_cfg = _update_components_cfg(components_cfg, cfg_item, cfg_path)
            else:
                components_cfg = _update_components_cfg(components_cfg, cfg, cfg_path)
    return components_cfg

def _update_components_cfg(components_cfg: ComponentConfigs, comp_cfg: dict, cfg_path: str, ) -> ComponentConfigs:
    if _check_configuration_structure(comp_cfg, cfg_path):
        if comp_cfg['code'] in getattr(components_cfg, comp_cfg['config_type']):
            log.warning(f"Component config type \"{comp_cfg['config_type']}\" with code \"{comp_cfg['code']}\" "
                        f"from {cfg_path} already loaded. Skipped")
        else:
            comp_cfg['__filepath'] = cfg_path
            components_cfg.__getattribute__(comp_cfg['config_type'])[comp_cfg['code']] = comp_cfg
            log.debug(f"Loading component config \"{comp_cfg['config_type']}\" \"{comp_cfg['code']}\" from {cfg_path}")
    return components_cfg

def _check_configuration_structure(comp_cfg: dict, cfg_path: str) -> bool:
    if not isinstance(comp_cfg, dict):
        log.warning(f"Component config {cfg_path} should be dictionary, not the {type(comp_cfg)}")
    elif 'config_type' not in comp_cfg:
        log.warning(f"Component config {cfg_path} should have \"config_type\" field")
    elif comp_cfg['config_type'] not in components_types:
        log.warning(f"{cfg_path} config type should be one of \"{components_types}\", "
                   f"current config type is \"{comp_cfg['config_type']}\"")
    elif 'code' not in comp_cfg:
        log.warning(f"Component config {cfg_path} should have \"code\" field")

    # TODO config structure verification for diff types
    return True
