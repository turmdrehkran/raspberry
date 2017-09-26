from RPi import GPIO


import turmdrehkran.threading

from turmdrehkran.exceptions import MotorOutOfBoundException


class GpioHandler:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.risingInputObservers = {}
        self.fallingInputObservers = {}
        self.outputs = set([])
        self.pwmoutputs = {}

        self.e = {}

    def _callback(self, pin):
        self._edge_event(GPIO.input(pin), pin)

    def _edge_event(self, edge, pin):
        if edge:
            for observer in self.risingInputObservers[pin]:
                observer.notify(pin, event='rising')
        else:
            for observer in self.fallingInputObservers[pin]:
                observer.notify(pin, event='falling')

    def _check_output(self, pin):
        if pin not in self.outputs:
            raise AssertionError("Pin "+pin+" was not properly intialized for OUT.")

    def _get_event(self, pin):
        try:
            return self.e[pin]
        except KeyError:
            self.e[pin] = turmdrehkran.threading.Event()
            return self.e[pin]

    def registerRisingObserver(self, pin, observer):
        self.risingInputObservers[pin].append(observer)

    def registerFallingObserver(self, pin, observer):
        self.fallingInputObservers[pin].append(observer)

    def setupInput(self, pin):
        GpioHandler._register_input(pin, self._callback)
        self.risingInputObservers[pin] = []
        self.fallingInputObservers[pin] = []

    def setupOutput(self, pin):
        print "output", pin
        GPIO.setup(pin, GPIO.OUT)
        self.outputs.add(pin)
        self.pwmoutputs[pin] = None

    def writeOutput(self, pin, value):
        self._check_output(pin)
        GPIO.output(pin, value)

    def genPWMOutput(self, pin, frequency, duration, duty_cycle=50.0):
        self._check_output(pin)
        self.pwmoutputs[pin] = GPIO.PWM(pin, frequency)
        self.pwmoutputs[pin].start(duty_cycle)

        self._get_event(pin).clear()
        self._get_event(pin).wait(duration)

        if self._get_event(pin).isSet() and self._get_event(pin).paramIsSet():
            raise MotorOutOfBoundException()

        self.pwmoutputs[pin].stop()

    def startPWMOutput(self, pin, frequency, duty_cycle=50.0):
        self._check_output(pin)
        self.pwmoutputs[pin] = GPIO.PWM(pin, frequency)
        self.pwmoutputs[pin].start(duty_cycle)

    def stopPWMOutput(self, pin, error=True):
        self._check_output(pin)
        self._get_event(pin).paramSet(error)
        try:
            self.pwmoutputs[pin].stop()
        except AttributeError:
            print "Motor Pin", pin, "not started yet."

    def stopPWMOutputOutOfBound(self, pin):
        self._check_output(pin)
        self._get_event(pin).set()

    @staticmethod
    def _register_input(nr, callback):
        GPIO.setup(nr, GPIO.IN)
        GPIO.add_event_detect(nr, GPIO.BOTH, callback=callback)




