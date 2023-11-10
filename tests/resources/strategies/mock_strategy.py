"""
Mosck strategy module
"""
from catcher_bot.model.strategy import Strategy


class MockStrategy(Strategy):
    """
    Mock strategy for testing
    """
    name = 'Mock strategy'

    def __init__(self):
        print('#### Mock Strategy INIT')

    def next(self):
        print('#### NEXT')

    def init(self):
        pass