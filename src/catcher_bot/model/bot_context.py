"""
Bot components
"""
import os

from catcher_bot.core import logger
from catcher_bot.core import import_modules
from catcher_bot.core.component_configs import ComponentConfigs
from catcher_bot.model.namespace import ModuleType

class BotContext:
    """
    Bot crucial components
    """
    LOG_NAME = 'catcher_bot'

    def __init__(self, bot_cfg: dict, component_configs: ComponentConfigs):
        self.bot_cfg = bot_cfg
        self.logger = logger.get_logger(self.LOG_NAME, self.bot_cfg.get('logger'))
        self.log.info('Initializing bot')
        self.log.debug(f'[DEV TODO 2del] Bot CFG: {bot_cfg}')
        strategies_path = bot_cfg['path']['strategies'] if bot_cfg['path']['strategies'].startswith(os.path.sep) else \
            os.path.normpath(os.path.join(bot_cfg['path']['__working_dir'], bot_cfg['path']['strategies']))
        self.strategies = import_modules.process(strategies_path, ModuleType.STRATEGY, self.log)

        self.strategies_cfg = component_configs.strategy
        self.log.debug(f'[DEV TODO 2del] Components CFG Strategies: {component_configs.strategy}')
        self.portfolio_cfg = component_configs.portfolio
        self.log.debug(f'[DEV TODO 2del] Components CFG Portfolio: {component_configs.portfolio}')
        self.connector_cfg = component_configs.connector
        self.log.debug(f'[DEV TODO 2del] Components CFG Exchanges: {component_configs.connector}')

        self.log.info('Init completed')


    @property
    def log(self):
        """
        Ger logger
        """
        return self.logger
