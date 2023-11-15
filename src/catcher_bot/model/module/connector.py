"""
Module with base connectory class
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class Connector:
    """
    Base connector class
    """
    __metaclass__ = ABCMeta
    code = __name__
    description = __doc__
