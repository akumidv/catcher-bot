from model.strategy import Strategy

__strategy_name__ = 'SMA' # Demanded class name to load strategy

class SMA(Strategy):
    def __init__(self):
        print('#### SMA STRATEGY INIT')

    def next(self):
        print('#### NEXT')
        pass