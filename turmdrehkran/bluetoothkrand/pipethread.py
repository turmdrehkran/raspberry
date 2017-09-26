import threading
import socket


class PipeThread(threading.Thread):
    pipes = []

    def __init__(self, source, sink):
        threading.Thread.__init__(self)
        self.source = source
        self.sink = sink

    def run(self):
        while 1:
            try:
                data = self.source.recv(1024)
                if not data:
                    break
                self.sink.send(data)
            except:
                break
        self.sink.shutdown(socket.SHUT_WR)  # close the socket on the write side