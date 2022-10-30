import os

import yaml
import argparse
from typing import Dict, Tuple
import logging
import logger

ENV_PREFIX = 'BOT'
LOG_NAME = 'init'
log = logger.get_def_logger(LOG_NAME)


def configure_bot() -> Dict:
    args = _get_args()
    bot_cfg = _get_bot_config_from_args(args)
    _log_init(bot_cfg)
    bot_cfg = _update_config_form_args(bot_cfg, args)
    bot_cfg = _update_config_from_env(bot_cfg) # TODO
    return bot_cfg


def _log_init(bot_cfg: Dict):
    global log
    log = logger.get_logger(LOG_NAME, bot_cfg.get('logger'))


def _get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='Catching bot', description='The trades catching bot description',
                                     epilog='Please send issues https://github.com/akumidv/catching-bot/issues')

    parser.add_argument('--cfg', default='./bot_config.yaml', type=argparse.FileType('r'),
                        help='The bot configuration in YAML format. See default "bot_config.yaml" file')
    parser.add_argument('--exchanges', default=['binance'], nargs='*', choices=['binance'],
                        help='List of exchanges')  # , 'kucoin'
    args = parser.parse_args()
    return args


def _get_bot_config_from_args(args: argparse.Namespace) -> Dict:
    bot_cfg = yaml.load(args.cfg, Loader=yaml.FullLoader)
    return bot_cfg


def _update_config_from_env(bot_cfg):     # TODO update some congig values from environment
    #  os.getenv('')
    log.debug('Config updated by environment arguments')
    return bot_cfg


def _update_config_form_args(bot_cfg: Dict, args: argparse.Namespace) -> Dict:
    for name in vars(args):
        if name in ['cfg']:
            continue
        if name not in ['exchanges']:
            continue
        print(name, getattr(args, name))
        bot_cfg[name] = getattr(args, name)
    log.debug('Config updated by app arguments')
    return bot_cfg

