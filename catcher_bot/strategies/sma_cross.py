from catcher_bot.model.strategy import Strategy

class SMA(Strategy):
    name = 'SMA Cross'

    def __init__(self):
        print('#### SMA STRATEGY INIT')

    def next(self):
        print('#### NEXT')
        pass