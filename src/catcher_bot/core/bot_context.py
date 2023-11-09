import os
from catcher_bot.core import logger
#from catcher_bot.core import config
from catcher_bot.core import setup_strategies
from catcher_bot.core.component_configs import ComponentConfigs


class BotContext:
    LOG_NAME = 'catcher_bot'

    def __init__(self, bot_cfg: dict, component_configs: ComponentConfigs):
        self.bot_cfg = bot_cfg
        self.logger = logger.get_logger(self.LOG_NAME, self.bot_cfg.get('logger'))
        self.log.debug(f'[DEV TODO 2del] Bot CFG: {bot_cfg}')
        self.strategies = setup_strategies.process(bot_cfg['strategy']['path'], self.log)
        self.log.info('Init completed')

    @property
    def log(self):
        return self.logger

