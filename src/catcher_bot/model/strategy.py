from abc import ABCMeta, abstractmethod, abstractproperty
from dataclasses import dataclass



class Strategy:
    __metaclass__ = ABCMeta
    code = __name__
    description = __doc__
    name = 'Strategy interface' # TODO Does it really needed?

    @abstractmethod
    def next(self):
        """Next tick"""

    @abstractmethod
    def init(self):
        """Init"""

