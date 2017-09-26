from turmdrehkran.gpio.control.gpio_controller import GpioController
from turmdrehkran.higherlevelcontrol.server import Server

import argparse


def main():
    parser = argparse.ArgumentParser(description="Turmdrehkran Hardware Controller", epilog="This software was created as part of a course in the Master's program 'Computer Science and Communication Systems' at htw saar Saarland University of Applied Sciences.")
    parser.add_argument("gpioMode", help="Mode of operation: 'gpio' will use the Raspberry's GPIO. 'mock' will simulate the Pi's GPIO and print actions to the screen.", type=str, choices=["gpio", "mock"])
    parser.add_argument("sockType", help="Socket Type: 'bluetooth' will start a Bluetooth RFCOMM service. 'tcp' will start a single-threaded TCP Server on Port 5010.", type=str, choices=["bluetooth", "tcp"])
    args = parser.parse_args()

    if args.gpioMode == 'gpio':
        if args.sockType == 'bluetooth':
            mainBluetooth()
            return
        if args.sockType == 'tcp':
            mainTcp()
            return

    if args.gpioMode == 'mock':
        if args.sockType == 'bluetooth':
            mainMockGpioBluetooth()
            return
        if args.sockType == 'tcp':
            mainMockGpioTcp()
            return




def mainBluetooth():
    try:
        from turmdrehkran.gpio.handler.gpio_handler import GpioHandler
        from turmdrehkran.higherlevelcontrol.sock.bluetooth import get_server_socket

        handler = GpioHandler()
        ctrl = GpioController(handler)

        server = Server(get_server_socket(), ctrl)

        server.run()
    finally:
        from RPi import GPIO
        GPIO.cleanup()

def mainTcp():
    try:
        from turmdrehkran.gpio.handler.gpio_handler import GpioHandler
        from turmdrehkran.higherlevelcontrol.sock.ip import get_server_socket
        handler = GpioHandler()
        ctrl = GpioController(handler)

        server = Server(get_server_socket(), ctrl)

        server.run()
    finally:
        from RPi import GPIO
        GPIO.cleanup()

def mainMockGpioBluetooth():
    from turmdrehkran.gpio.handler.gpio_mock_handler import GpioMockHandler
    from turmdrehkran.higherlevelcontrol.sock.bluetooth import get_server_socket

    handler = GpioMockHandler()
    ctrl = GpioController(handler)

    server = Server(get_server_socket(), ctrl)

    server.run()

def mainMockGpioTcp():
    from turmdrehkran.gpio.handler.gpio_mock_handler import GpioMockHandler
    from turmdrehkran.higherlevelcontrol.sock.ip import get_server_socket


    handler = GpioMockHandler()
    ctrl = GpioController(handler)

    server = Server(get_server_socket(), ctrl)

    server.run()