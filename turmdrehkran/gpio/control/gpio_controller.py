from gpio_control_interface import GpioControlInterface
from turmdrehkran.gpio import pinout
from turmdrehkran.gpio.handler.gpio_observer import GpioObserver
from gpio_step_motor import GpioStepMotor

from turmdrehkran.exceptions.motor_out_of_bounds_exception import MotorOutOfBoundException


class GpioController(GpioControlInterface, GpioObserver):
    def __init__(self, gpiohandler):
        self.gpiohandler = gpiohandler

        # Mapping zwischen Pins und den zugehoerigen Methoden
        self.pinmap = {

            pinout.lichtschranke_1: ( # Ausleger Vorne
                self.lichtschranke1_triggered,
                self.lichtschranke1_released,
            ),

            pinout.lichtschranke_2: ( # Ausleger Hinten
                self.lichtschranke2_triggered,
                self.lichtschranke2_released,
            ),

            pinout.lichtschranke_3: ( # Haken Oben
                self.lichtschranke3_triggered,
                self.lichtschranke3_released,
            ),

            pinout.lichtschranke_4: ( # Turm Nullpunkt
                self.lichtschranke4_triggered,
                self.lichtschranke4_released
            ),

            pinout.handsteuerung_links: (
                self.handsteuerung_links_pressed,
                self.handsteuerung_links_released
            ),

            pinout.handsteuerung_rechts: (
                self.handsteuerung_rechts_pressed,
                self.handsteuerung_rechts_released
            ),

            pinout.handsteuerung_oben: (
                self.handsteuerung_oben_pressed,
                self.handsteuerung_oben_released
            ),

            pinout.handsteuerung_unten: (
                self.handsteuerung_unten_pressed,
                self.handsteuerung_unten_released
            ),

            pinout.handsteuerung_opt_links: (
                lambda: None,
                lambda: None
            ),

            pinout.handsteuerung_opt_rechts: (
                lambda: None,
                lambda: None
            ),

            pinout.handsteuerung_opt_oben: (
                self.handsteuerung_opt_oben_pressed,
                self.handsteuerung_opt_oben_released
            ),

            pinout.handsteuerung_opt_unten: (
                self.handsteuerung_opt_unten_pressed,
                self.handsteuerung_opt_unten_released
            )

        }

        self.motors = [
                GpioStepMotor(self.gpiohandler, pinout.motor1_step, pinout.motor1_direction), # Turm
                GpioStepMotor(self.gpiohandler, pinout.motor2_step, pinout.motor2_direction), # Laufkatze
                GpioStepMotor(self.gpiohandler, pinout.motor3_step, pinout.motor3_direction)  # Seilwinde
        ]

        self._registerAllInputs()
        self._registerAllOutputs()

        self._handsteuerung_lock = False

    def _registerAllInputs(self):
        for pin in self.pinmap:
            self.gpiohandler.setupInput(pin)
            self.gpiohandler.registerRisingObserver(pin, self)
            self.gpiohandler.registerFallingObserver(pin, self)

    def _registerAllOutputs(self):
        self.gpiohandler.setupOutput(pinout.connection_led)
        self.turn_connection_led_off()

    def motor(self, motorid):
        # type: (int) -> GpioStepMotor
        return self.motors[motorid]

    def get_motors(self):
        return self.motors

    def notify(self, pin, **kwargs):
        print pin, kwargs
        if kwargs["event"] == 'rising':
            self.pinmap[pin][0]()
            return

        if kwargs["event"] == 'falling':
            self.pinmap[pin][1]()
            return

    def turn_connection_led_on(self):
        self.gpiohandler.writeOutput(pinout.connection_led, 1)

    def turn_connection_led_off(self):
        self.gpiohandler.writeOutput(pinout.connection_led, 0)

    def handsteuerung_lock(self):
        self._handsteuerung_lock = True
        for el in self.get_motors():
            el.move_stop_no_error()
        self.turn_connection_led_on()

    def handsteuerung_enable(self):
        self._handsteuerung_lock = False
        self.turn_connection_led_off()

    def lichtschranke1_triggered(self):
        self.motor(1).lock = 1

    def lichtschranke1_released(self):
        self.motor(1).lock = 0

    def lichtschranke2_triggered(self):
        self.motor(1).lock = -1

    def lichtschranke2_released(self):
        self.motor(1).lock = 0

    def lichtschranke3_triggered(self):
        self.motor(2).lock = 1

    def lichtschranke3_released(self):
        self.motor(2).lock = 0

    def lichtschranke4_triggered(self):
        pass
        # self.motor(0).lock = 1

    def lichtschranke4_released(self):
        pass
        #self.motor(0).lock = 0

    def handsteuerung_links_pressed(self):
        if self._handsteuerung_lock:
            return

        self.motor(0).move_start(
            direction='forward',
            speed=200
        )

    def handsteuerung_links_released(self):
        if self._handsteuerung_lock:
            return
        self.motor(0).move_stop()

    def handsteuerung_rechts_pressed(self):
        if self._handsteuerung_lock:
            return
        self.motor(0).move_start(
            direction='backward',
            speed=200
        )

    def handsteuerung_rechts_released(self):
        if self._handsteuerung_lock:
            return
        self.motor(0).move_stop()

    def handsteuerung_unten_pressed(self):
        if self._handsteuerung_lock:
            return
        self.motor(1).move_start(
            direction='backward',
            speed=200
        )

    def handsteuerung_unten_released(self):
        if self._handsteuerung_lock:
            return
        self.motor(1).move_stop()

    def handsteuerung_oben_pressed(self):
        if self._handsteuerung_lock:
            return
        self.motor(1).move_start(
            direction='forward',
            speed=200
        )

    def handsteuerung_oben_released(self):
        if self._handsteuerung_lock:
            return
        self.motor(1).move_stop()

    def handsteuerung_opt_rechts_released(self):
        if self._handsteuerung_lock:
            return
        pass

    def handsteuerung_opt_oben_released(self):
        if self._handsteuerung_lock:
            return
        self.motor(2).move_stop()

    def handsteuerung_opt_oben_pressed(self):
        if self._handsteuerung_lock:
            return
        self.motor(2).move_start(
            speed=400,
            direction='forward'
        )

    def handsteuerung_opt_links_released(self):
        if self._handsteuerung_lock:
            return
        pass

    def handsteuerung_opt_unten_pressed(self):
        if self._handsteuerung_lock:
            return
        self.motor(2).move_start(
            speed=400,
            direction='backward'
        )

    def handsteuerung_opt_unten_released(self):
        if self._handsteuerung_lock:
            return
        self.motor(2).move_stop()

    def handsteuerung_opt_links_pressed(self):
        if self._handsteuerung_lock:
            return
        pass

    def handsteuerung_opt_rechts_pressed(self):
        if self._handsteuerung_lock:
            return
        pass






