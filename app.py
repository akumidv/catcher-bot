import logger
import init


def bot_init():
    bot_cfg = init.configure_bot()
    print('[DEV]', bot_cfg)
    log = logger.get_logger(module_name='app')
    log.info('Init completed')


if __name__ == '__main__':
    bot_init()


