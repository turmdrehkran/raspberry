
from abc import ABCMeta, abstractmethod


class GpioObserver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, pin, **kwargs): raise NotImplementedError