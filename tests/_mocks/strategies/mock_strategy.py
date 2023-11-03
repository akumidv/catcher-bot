from model.strategy import Strategy

class MockStrategy(Strategy):
    name = 'Mock strategy'

    def __init__(self):
        print('#### Mock Strategy INIT')

    def next(self):
        print('#### NEXT')
        pass

