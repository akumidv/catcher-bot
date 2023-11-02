from abc import ABCMeta, abstractmethod, abstractproperty


class Strategy:
    __metaclass__ = ABCMeta

    __name__ = 'strategy'

    @abstractmethod
    def next(self):
        """Next tick"""

    @property
    @abstractmethod
    def init(self):
        """Init"""