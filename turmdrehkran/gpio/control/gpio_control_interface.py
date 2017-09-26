
from abc import ABCMeta, abstractmethod


class GpioControlInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def lichtschranke1_triggered(self): raise NotImplementedError

    @abstractmethod
    def lichtschranke2_triggered(self): raise NotImplementedError

    @abstractmethod
    def lichtschranke3_triggered(self): raise NotImplementedError

    @abstractmethod
    def lichtschranke4_triggered(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_oben_pressed(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_oben_released(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_unten_pressed(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_unten_released(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_links_pressed(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_links_released(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_rechts_pressed(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_rechts_released(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_oben_pressed(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_opt_oben_released(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_opt_unten_pressed(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_opt_unten_released(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_opt_links_pressed(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_opt_links_released(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_opt_rechts_pressed(self): raise NotImplementedError

    @abstractmethod
    def handsteuerung_opt_rechts_released(self): raise NotImplementedError
