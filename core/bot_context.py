from core import logger
from core import config
import os
from core import init


class BotContext:
    LOG_NAME = 'catcher_bot'

    def __init__(self, bot_cfg: dict):
        self.bot_cfg = bot_cfg
        self.logger = logger.get_logger(self.LOG_NAME, self.bot_cfg.get('logger'))
        self.log.debug(f'[DEV TODO 2del] Bot CFG: {bot_cfg}')
        self.strategies = init.init_strategies(bot_cfg['strategy']['path'], self.log)
        self.log.info('Init completed')


    @property
    def log(self):
        return self.logger

