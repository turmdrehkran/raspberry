

from threading import Thread
import socket
from pipethread import PipeThread


class Pinhole(Thread):
    def __init__(self, port, blue):
        Thread.__init__(self)
        self.blue = blue
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))
        self.sock.listen(1)

    def stop(self):
        self.sock.close()
        self.blue.close()

    def run(self):
        while 1:
            newsock, address = self.sock.accept()
            a = PipeThread(newsock, self.blue)
            b = PipeThread(self.blue, newsock)

            a.start()
            b.start()

            a.join()
            b.join()

            self.sock.close()
