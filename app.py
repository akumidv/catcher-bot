
from core.bot_context import BotContext
from controller.strategy_dispatcher import StrategyDispatcher


def run():
    bc = BotContext()
    sd = StrategyDispatcher(bc)

    sd.run()




if __name__ == '__main__':
    run()


