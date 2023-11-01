from core import logger
from core import config
import os


class BotContext:
    LOG_NAME = 'catcher_bot'

    def __init__(self, bot_cfg: dict):
        self.bot_cfg = bot_cfg
        self.logger = logger.get_logger(self.LOG_NAME, self.bot_cfg.get('logger'))
        # self.logger = logger.get_logger(module_name='app')
        self.log.info('Init completed')
        print(self.bot_cfg)



    @property
    def log(self):
        return self.logger

