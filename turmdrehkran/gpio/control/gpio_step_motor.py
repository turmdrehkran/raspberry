
from turmdrehkran.exceptions.motor_out_of_bounds_exception import MotorOutOfBoundException

class GpioStepMotor(object):
    def __init__(self, gpiohandler, motor_pin_step, motor_pin_direction):
        self.gpiohandler = gpiohandler
        self.motor_pin_step = motor_pin_step
        self.motor_pin_direction = motor_pin_direction
        self._lock = 0
        self._init_motor()

    def _init_motor(self):
        self.gpiohandler.setupOutput(self.motor_pin_direction)
        self.gpiohandler.setupOutput(self.motor_pin_step)

    @property
    def lock(self):
        return self._lock

    @lock.setter
    def lock(self, val):
        if val != 0:
            self.move_stop()
        self._lock = val


    @staticmethod
    def lock_permits(lock, direction):

        logic = {
            "forward": [0, -1],
            "backward": [1, 0]
        }

        return lock in logic[direction]

    def move_command(self, motorcommand):
        if not isinstance(motorcommand, MotorCommand):
            raise TypeError("motorcommand must be of Type MotorCommand")

        self.move(
            direction=motorcommand.direction,
            steps=motorcommand.numberofsteps,
            speed=motorcommand.speed
        )

    def move(self, **kwargs):
        direction = kwargs['direction']
        steps = kwargs['steps']
        speed = kwargs['speed']

        if direction not in ['forward', 'backward']:
            raise ValueError("Invalid argument for direction supplied")

        #Checking the lock:
        if not self.lock_permits(self.lock, direction):
            raise MotorOutOfBoundException()

        # Setting Up the direction

        if direction == 'forward':
            self.gpiohandler.writeOutput(self.motor_pin_direction, 0)
        else:
            self.gpiohandler.writeOutput(self.motor_pin_direction, 1)

        # Performing the steps
        self.gpiohandler.genPWMOutput(
            self.motor_pin_step,
            speed,
            ((1.0/speed)*steps)
        )

    def move_start(self, **kwargs):
        speed = kwargs['speed']
        direction = kwargs['direction']

        if direction not in ['forward', 'backward']:
            raise ValueError("Invalid argument for direction supplied")

        # Checking the lock:
        if not self.lock_permits(self.lock, direction):
            raise MotorOutOfBoundException()

        if direction == 'forward':
            self.gpiohandler.writeOutput(self.motor_pin_direction, 0)
        else:
            self.gpiohandler.writeOutput(self.motor_pin_direction, 1)

        self.gpiohandler.startPWMOutput(self.motor_pin_step, speed)

    def move_stop(self):
        self.gpiohandler.stopPWMOutput(self.motor_pin_step)

    def move_stop_no_error(self):
        self.gpiohandler.stopPWMOutput(self.motor_pin_step, False)


class MotorCommand:
    def __init__(self, direction, numberofsteps, speed):
        self._direction = direction
        self._numberofsteps = numberofsteps
        self._speed = speed

    @property
    def direction(self):
        return self._direction

    @property
    def numberofsteps(self):
        return self._numberofsteps

    @property
    def speed(self):
        return self._speed
