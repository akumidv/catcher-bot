import logger
import init





def bot_init():
    init.configure_bot()
    logger.get_logger(module_name='app')


if __name__ == '__main__':
    bot_init()
    pass

