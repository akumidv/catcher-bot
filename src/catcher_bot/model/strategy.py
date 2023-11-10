from abc import ABCMeta, abstractmethod, abstractproperty
from dataclasses import dataclass



class Strategy:
    __metaclass__ = ABCMeta

    name = 'Strategy interface'

    @abstractmethod
    def next(self):
        """Next tick"""

    @abstractmethod
    def init(self):
        """Init"""

