from abc import ABCMeta, abstractmethod, abstractproperty


class Strategy:
    __metaclass__ = ABCMeta

    @abstractmethod
    def next(self):
        """Next tick"""

    @property
    @abstractmethod
    def init(self):
        """Init"""