from abc import ABCMeta, abstractmethod, abstractproperty


class Strategy:
    __metaclass__ = ABCMeta

    @abstractmethod
    def next(self):
        """Переместить объект"""
    @property
    @abstractmethod
    def speed(self):
        """Скорость объекта"""