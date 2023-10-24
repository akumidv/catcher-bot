import os

import yaml
import argparse
from typing import Dict, Tuple
from core import logger

ENV_PREFIX = 'BOT'
LOG_NAME = 'init'


ARGS_PARAM_NAMES_TO_CHANGE_CFG = ['exchanges', 'trade_type', 'telegram_chat_id', 'telegram_bot_token']
ARGS_PARAM_NAMES_WITH_LEVEL = ['telegram']
ARGS_PARAM_NAMES_FOR_BOT = ['cfg']

log = logger.get_def_logger(LOG_NAME) # logger.get_logger(LOG_NAME, bot_cfg.get('logger')) #


def configure_bot() -> Dict:
    args = _get_args()
    bot_cfg = _get_bot_config_from_args(args)
    bot_cfg = _update_config_from_args(bot_cfg, args)
    bot_cfg = _update_config_from_env(bot_cfg)
    _verify_config(bot_cfg)
    return bot_cfg

def _verify_config(bot_cfg):
    if 'credentials' not in bot_cfg:
        raise KeyError('credentials are not set in bot cfg')
    if 'exchanges' not in bot_cfg:
        raise KeyError('exchanges are not set in bot cfg')
    if 'market_types' not in bot_cfg:
        raise KeyError('market_types are not set in bot cfg')
    for exchange in bot_cfg['exchanges']:
        for market_type in bot_cfg['market_types']:
            if market_type not in bot_cfg['credentials']:
                raise KeyError(f'Market type {market_type} credentials are not set in bot cfg')
            if exchange not in bot_cfg['credentials'][market_type]:
                raise KeyError(f'{exchange} exchange credentials are not set in bot cfg')



def _get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='Catching bot', description='The trades catching bot description',
                                     epilog='Please send issues https://github.com/akumidv/catching-bot/issues')

    parser.add_argument('--cfg', default='./bot_config.yaml', type=argparse.FileType('r'),
                        help='The bot configuration in YAML format. See default "bot_config.yaml" file')
    parser.add_argument('--exchange', nargs='*', choices=['binance'], #  default=['binance'],
                        help='List of exchange')  # , 'kucoin'
    parser.add_argument('--trade_type', choices=['futures', 'market'], # default='futures',
                        help='Trade type')  # , 'kucoin'
    parser.add_argument('--telegram_chat_id', required=False,
                        help='Telegram chat id.')
    parser.add_argument('--telegram_bot_token', required=False,
                        help='Telegram bot token.')
    args = parser.parse_args()
    return args


def _get_bot_config_from_args(args: argparse.Namespace) -> Dict:
    bot_cfg = yaml.load(args.cfg, Loader=yaml.FullLoader)
    return bot_cfg


def _update_config_from_env(bot_cfg):     # TODO update some config values from environment
    """update some config values from environment"""
    if 'telegram' not in bot_cfg: bot_cfg['telegram'] = {'chat_id': '', 'bot_token': ''}
    if os.getenv('TG_CHAT_ID'): bot_cfg['telegram']['chat_id'] = os.getenv('TG_CHAT_ID')
    if os.getenv('TG_BOT_TOKEN'): bot_cfg['telegram']['bot_token'] = os.getenv('TG_BOT_TOKEN')

    if 'credentials' not in bot_cfg: bot_cfg['credentials'] = {'stock': {}, 'futures': {}}
    if 'binance' not in bot_cfg['credentials']: bot_cfg['credentials']['stock']['binance'] = {'api_key': '', 'secret_key': ''}
    if os.getenv('BINANCE_API_KEY'): bot_cfg['credentials']['stock']['binance']['secret_key'] = os.getenv('BINANCE_API_KEY')
    if os.getenv('BINANCE_SECRET_KEY'): bot_cfg['credentials']['stock']['binance']['secret_key'] = os.getenv('BINANCE_SECRET_KEY')

    log.debug('Config updated by environment arguments')
    return bot_cfg


def _update_config_from_args(bot_cfg: Dict, args: argparse.Namespace) -> Dict:
    changed_params = []
    for name in vars(args):
        if name in ARGS_PARAM_NAMES_FOR_BOT or name not in ARGS_PARAM_NAMES_TO_CHANGE_CFG:
            continue
        arg_value = getattr(args, name)
        if arg_value is None:
            continue
        changed_params.append(name)
        name_to_split = [split_name for split_name in ARGS_PARAM_NAMES_WITH_LEVEL if f'{name}_'.startswith(split_name)]
        if name_to_split:
            group_name = name_to_split[0]
            second_level_name = name[len(f'{group_name}_'):]
            if group_name not in bot_cfg:
                bot_cfg[group_name] = {}
            bot_cfg[group_name][second_level_name] = arg_value
        else:
            bot_cfg[name] = arg_value
    if len(changed_params):
        log.debug(f'Config updated by app arguments: {",".join(changed_params)}')
    return bot_cfg

