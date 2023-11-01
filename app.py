
from core.config import configure_bot
from core.bot_context import BotContext
from controller.strategy_dispatcher import StrategyDispatcher


def run():
    bot_cfg = configure_bot()
    bc = BotContext(bot_cfg)
    sd = StrategyDispatcher(bc)

    sd.run()




if __name__ == '__main__':
    run()


