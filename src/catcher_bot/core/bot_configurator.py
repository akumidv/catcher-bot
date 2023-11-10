"""
Configure module. Loading and parsing configs from bot configs and folder with bot configure
"""
import os
import argparse

import yaml

from catcher_bot.core import logger

ENV_PREFIX = 'BOT'
LOG_NAME = 'init'

ARGS_PARAM_NAMES_TO_CHANGE_CFG = ['telegram_chat_id', 'telegram_bot_token'] # 'exchanges','trade_type','strategies_path'
ARGS_PARAM_NAMES_WITH_LEVEL = ['telegram']  # , 'strategies'
ARGS_PARAM_NAMES_FOR_BOT = ['cfg']

log = logger.get_def_logger(LOG_NAME)  # logger.get_logger(LOG_NAME, bot_cfg.get('logger')) #


def prepare_bot_config(bot_root_path: str) -> dict:
    """
    Preparing configure bot dictionary
    """
    bot_working_dir = os.path.abspath(os.path.curdir)
    args = _get_args()
    bot_cfg = _load_bot_config(args.cfg, bot_working_dir)
    _check_loaded_bot_config(bot_cfg)
    bot_cfg = _update_config_from_args(bot_cfg, args)
    bot_cfg = _update_config_from_env(bot_cfg)
    bot_cfg['path']['__working_dir'] = bot_working_dir
    bot_cfg['path']['__bot_root_path'] = bot_root_path
    _verify_config(bot_cfg)
    return bot_cfg


def _get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='Catching bot', description='The trades catching bot description',
                                     epilog='Please send issues https://github.com/akumidv/catching-bot/issues')

    parser.add_argument('--cfg', default='./bot_config.yaml', type=str,# argparse.FileType('r'),
                        help='The bot configuration in YAML format. See default "bot_config.yaml" file')
    # parser.add_argument('--exchange', nargs='*', choices=['binance'], #  default=['binance'],
    #                     help='List of exchange')  # , 'kucoin'
    # parser.add_argument('--trade_type', choices=['futures', 'market'], # default='futures',
    #                     help='Trade type')
    parser.add_argument('--telegram_chat_id', required=False,
                        help='Telegram chat id.')
    parser.add_argument('--telegram_bot_token', required=False,
                        help='Telegram bot token.')
    # parser.add_argument('--strategies_path', required=False,
    #                     help='Strategies path')
    args = parser.parse_args()
    return args


def _load_bot_config(config_path: str, bot_working_dir: str) -> dict:
    """
    Loading bot configuration file
    """
    # bot_cfg = yaml.load(args.cfg, Loader=yaml.FullLoader)
    config_path = os.path.normpath(os.path.join(bot_working_dir, config_path))
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f'Config file "{config_path}" is not found from working(current) '
                                f'directory "{bot_working_dir}')

    with open(config_path, 'r', encoding='utf-8') as fd:
        bot_cfg = yaml.safe_load(fd)

    return bot_cfg


def _check_loaded_bot_config(bot_cfg: dict):
    if not isinstance(bot_cfg, dict):
        raise TypeError(f'Bot config should be dictionary, not the {type(bot_cfg)}')
    if 'config_type' not in bot_cfg:
        raise KeyError('Bot config should have "config_type" field')
    if bot_cfg['config_type'] != 'bot':
        raise ValueError(f'Bot config type should be equal "bot", current config is "{bot_cfg["config_type"]}"')


def _update_config_from_env(bot_cfg: dict) -> dict: # TODO update some config values from environment
    """
    Updating some config values from environment
    """
    if 'telegram' not in bot_cfg:
        bot_cfg['telegram'] = {'chat_id': '', 'bot_token': ''}
    if os.getenv('TG_CHAT_ID'):
        bot_cfg['telegram']['chat_id'] = os.getenv('TG_CHAT_ID')
    if os.getenv('TG_BOT_TOKEN'):
        bot_cfg['telegram']['bot_token'] = os.getenv('TG_BOT_TOKEN')

    # if 'credentials' not in bot_cfg: bot_cfg['credentials'] = {'stock': {}, 'futures': {}}
    # if 'binance' not in bot_cfg['credentials']:
    #   bot_cfg['credentials']['stock']['binance'] = {'api_key': '', 'secret_key': ''}
    # if os.getenv('BINANCE_API_KEY'):
    #   bot_cfg['credentials']['stock']['binance']['secret_key'] = os.getenv('BINANCE_API_KEY')
    # if os.getenv('BINANCE_SECRET_KEY'):
    #   bot_cfg['credentials']['stock']['binance']['secret_key'] = os.getenv('BINANCE_SECRET_KEY')

    log.debug('Config updated by environment arguments')
    return bot_cfg


def _update_config_from_args(bot_cfg: dict, args: argparse.Namespace) -> dict:
    """
    Updating some bot configure variables from args
    """
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
    if len(changed_params) != 0:
        log.debug(f'Config updated by app arguments: {",".join(changed_params)}')
    return bot_cfg


def _verify_config(bot_cfg: dict):
    """
    Verifying mandatory bot config structure
    """
    if not isinstance(bot_cfg, dict):
        raise TypeError('Bot config parameter "path" for components was not set')
    if 'path' not in bot_cfg:
        raise KeyError('Bot config parameter "path" for components was not set')
    if not isinstance(bot_cfg['path'], dict):
        raise TypeError('Bot config parameter "path" not content values of paths to components')
    if 'config' not in bot_cfg['path']:
        raise KeyError('Bot config parameter "path.config" for configurations was not set')
    if '__working_dir' not in bot_cfg['path']:
        raise KeyError('Bot config parameter "__working_dir" is not automatically set')
    if not os.path.isdir(bot_cfg['path']['__working_dir' ]):
        raise FileExistsError(f"Bot config working {bot_cfg['path']['__working_dir' ]} directory is not exist")
    # if 'credentials' not in bot_cfg:
    #     raise KeyError('credentials are not set in bot cfg')
    # if 'exchanges' not in bot_cfg:
    #     raise KeyError('exchanges are not set in bot cfg')
    # if 'market_types' not in bot_cfg:
    #     raise KeyError('market_types are not set in bot cfg')
    # if 'strategies' not in bot_cfg or 'path' not in bot_cfg['strategies']:
    #     raise KeyError('strategies path is not set in bot cfg')
    # for exchange in bot_cfg['exchanges']:
    #     for market_type in bot_cfg['market_types']:
    #         if market_type not in bot_cfg['credentials']:
    #             raise KeyError(f'Market type {market_type} credentials are not set in bot cfg')
    #         if exchange not in bot_cfg['credentials'][market_type]:
    #             raise KeyError(f'{exchange} exchange credentials are not set in bot cfg')
