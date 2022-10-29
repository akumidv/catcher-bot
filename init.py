import yaml
import argparse
import logging


def configure_bot():
    parser = argparse.ArgumentParser(prog='Catching bot', description='The trades catching bot description',
                                     epilog='Please send issues https://github.com/akumidv/catching-bot/issues' )

    parser.add_argument('--cfg', default='./bot_config.yaml', type=argparse.FileType('r'), help='The bot configuration in YAML format. See default "bot_config.yaml" file')
    parser.add_argument('--exchanges', default=['binance'], nargs='*', choices=['binance'], help='List of exchanges') # , 'kucoin'
    args = parser.parse_args()

    print(args)
    config = yaml.load(args.cfg, Loader=yaml.FullLoader)
    print('###', config)
    for name in vars(args):
        if name in ['cfg']:
            continue
        print(name, getattr(args, name))
    # args.
    # config
