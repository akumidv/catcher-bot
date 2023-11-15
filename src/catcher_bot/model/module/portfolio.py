"""
Module with portfolio class
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class Portfolio:
    """
    Porgolio base class
    """
    __metaclass__ = ABCMeta
    code = __name__
    description = __doc__
