import time
from threading import Lock

from turmdrehkran.exceptions import MotorOutOfBoundException

print_lock = Lock()


def save_print(*args):
    with print_lock:
        print "GpioMockHandler: ",args


class GpioMockHandler:
    def __init__(self):
        pass

    def _callback(self, pin):
        save_print("_callback", pin)

    def _edge_event(self, edge, pin):
        save_print("_edge_event", edge, pin)

    def _check_output(self, pin):
        save_print("_check_output", pin)

    def registerRisingObserver(self, pin, observer):
        save_print("registerRisingObserver", pin, observer)

    def registerFallingObserver(self, pin, observer):
        save_print("registerFallingObserver", pin, observer)

    def setupInput(self, pin):
        save_print("setupInput", pin)

    def setupOutput(self, pin):
        save_print("setupOutput", pin)

    def writeOutput(self, pin, value):
        save_print("writeOutput", pin, value)

    def genPWMOutput(self, pin, frequency, duration, duty_cycle=50.0):
        save_print("genPWMOutput", pin, frequency, duration, duty_cycle)
        time.sleep(duration)

    def startPWMOutput(self, pin, frequency, duty_cycle=50.0):
        save_print("startPWMOutput", pin, frequency, duty_cycle)

    def stopPWMOutput(self, pin, error=True):
        save_print("stopPWMOutput", pin, error)

    @staticmethod
    def _register_input(nr, callback):
        pass




