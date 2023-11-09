"""
Configure module. Loading and parsing configs from bot configs and folder with bot configure
"""
from collections import namedtuple
from catcher_bot.core import logger

ENV_PREFIX = 'BOT'
LOG_NAME = 'init'

log = logger.get_def_logger(LOG_NAME)

ComponentConfigs = namedtuple('ComponentConfigs', ('strategy', 'portfolio', 'exchange'))


def get_configs(bot_cfg: dict) -> ComponentConfigs:
    configs_path = bot_cfg['path']['config']
    component_configs = ComponentConfigs(strategy={}, portfolio={}, exchange={})
    return component_configs

