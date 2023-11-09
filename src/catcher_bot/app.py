"""
Main bot starting module
"""
import os
from catcher_bot.core.bot_configurator import prepare_bot_config
from catcher_bot.core.component_configs import load_configs, ComponentConfigs
from catcher_bot.core.bot_context import BotContext
from catcher_bot.controller.dispatcher import root


def init() -> BotContext:
    """
    Base bot init workflow
    """
    bot_root_path = os.path.abspath(os.path.dirname(__file__))
    bot_cfg: dict = prepare_bot_config(bot_root_path)
    # component_configs: ComponentConfigs = get_configs(bot_cfg['path'])
    # bc: BotContext = BotContext(bot_cfg, component_configs)
    bc = None
    return bc


def run(bc: BotContext):
    """
    Bot run after init
    """
    root.run(bc)


if __name__ == '__main__':
    bot_context: BotContext = init()
    run(bot_context)
