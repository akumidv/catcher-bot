from core import logger
from core import init


class BotContext:
    LOG_NAME = 'catcher_bot'

    def __init__(self):
        self.bot_cfg = init.configure_bot()
        self.logger = logger.get_logger(self.LOG_NAME, self.bot_cfg.get('logger'))
        # self.logger = logger.get_logger(module_name='app')
        self.logger.info('Init completed')
        print(self.bot_cfg)


    @property
    def log(self):
        return self.logger

