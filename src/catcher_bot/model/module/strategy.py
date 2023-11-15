"""
Module with base strategy class
"""
from abc import ABCMeta, abstractmethod, abstractproperty
from dataclasses import dataclass


class Strategy:
    """
    Strategy base class
    """

    __metaclass__ = ABCMeta
    code = __name__
    description = __doc__

    @abstractmethod
    def next(self):
        """Next tick"""

    @abstractmethod
    def init(self):
        """Init"""
