from abstract_method import AbstractMethod
from turmdrehkran.higherlevelcontrol.protocol.responses import Response100, Response150, Response200, Response410, Response550
from turmdrehkran.gpio.control.gpio_step_motor import MotorCommand
from turmdrehkran.exceptions import MotorOutOfBoundException

import threading


class RunMethod(AbstractMethod):

    def __init__(self, request):
        AbstractMethod.__init__(self, request)

        self.motor_ids = []
        self.direction = []
        self.speed = []
        self.numsteps = []

        self.commands = {}

        self.threads = []

    def execute(self, server):

        valid_motor_ids = [0, 1, 2]
        valid_directions = ['L', 'R']
        valid_speeds = range(1, 1000)
        valid_numsteps = range(1, 100000)

        in_error_state = threading.Event()


        # Motor IDs

        self.motor_ids = self.request.method_args

        if len(self.motor_ids) < 1:
            return Response410({"Message": "No Motor IDs provided"})

        try:
            self.motor_ids = [int(x) for x in self.motor_ids]
        except ValueError as e:
            return Response410({"Message": "Motor IDs must be integers"})

        if len(self.motor_ids) != len(set(self.motor_ids)):
            return Response410({"Message": "Motor IDs contain duplicate elements"})

        if not (set(self.motor_ids) <= set(valid_motor_ids)):
            return Response410({"Message": "Motor IDs contain invalid Motor IDs"})


        # Direction

        if "Direction" not in self.request.params:
            return Response410({"Message": "Direction Parameter missing"})

        self.direction = str.split(self.request.params["Direction"])

        for x in self.direction:
            if x not in valid_directions:
                return Response410({"Message": "Invalid Direction Value: '"+ x + "'"})


        # Speed

        if "Speed" not in self.request.params:
            return Response410({"Message": "Speed Parameter missing"})

        self.speed = str.split(self.request.params["Speed"])

        try:
            self.speed = [int(x) for x in self.speed]
        except ValueError as e:
            return Response410({"Message": "Speed must be integers"})

        for x in self.speed:
            if x not in valid_speeds:
                return Response410({"Message": "Invalid Speed Value: '" + str(x) + "'"})

        # Num Steps

        if "NumSteps" not in self.request.params:
            return Response410({"Message": "NumSteps Parameter missing"})

        self.numsteps = str.split(self.request.params["NumSteps"])

        try:
            self.numsteps = [int(x) for x in self.numsteps]
        except ValueError as e:
            return Response410({"Message": "Numsteps must be integers"})

        for x in self.numsteps:
            if x not in valid_numsteps:
                return Response410({"Message": "Invalid NumSteps Value: '" + str(x) + "'"})

        # Length

        if len(self.motor_ids) != len(self.direction):
            return Response410({"Message": "Length mismatch between Motor IDs and Direction Paramters"})

        if len(self.motor_ids) != len(self.speed):
            return Response410({"Message": "Length mismatch between Motor IDs and Speed Paramters"})

        if len(self.motor_ids) != len(self.numsteps):
            return Response410({"Message": "Length mismatch between Motor IDs and NumStep Paramters"})

        # Build Motor Commands

        for count, id in enumerate(self.motor_ids, start=0):
            self.commands[id] = MotorCommand(
                "forward" if self.direction[count] == "L" else "backward",
                self.numsteps[count],
                self.speed[count]
            )

        # Execute Motor Commands in seperate Threads in wait until they all have completed...

        def exec_motor(id):
            server.send_intermittent_response(Response100({"Motor": id}))
            try:
                server.get_controller().motor(id).move_command(self.commands[id])
            except MotorOutOfBoundException as e:
                in_error_state.set()
                server.send_intermittent_response(Response150({"Motor": id}))
                for i in range(0, 3):
                        server.get_controller().motor(i).move_stop_no_error()

        # Create Thread
        for id in self.commands:
            self.threads.append(threading.Thread(target=exec_motor, args=(id,)))

        # Start Thread
        for t in self.threads:
            t.start()

        # Wait for all Threads to finish
        for t in self.threads:
            t.join()

        # Signal Finish
        if not in_error_state.isSet():
            return Response200({})
        else:
            return Response550({})
