

from bluetooth import *

import tcpserver
from pipethread import PipeThread

def main():

    while True:
        addr = [
            "B8:27:EB:0F:FD:E2",
            "20:17:03:29:18:18"
        ]


        # search for the SampleServer service
        uuid = [
            "94f39d29-7d6d-437d-973b-fba39e49d4ee",
            "00001101-0000-1000-8000-00805F9B34FB"
            ]



        print("Suche Controller...")

        print("Suche Raspberry")
        service_matches = find_service(uuid=uuid[0], address=addr[0])

        if len(service_matches) == 0:
            print("Konnte Raspberry Pi nicht finden. Versuche Arduino zu erreichen...")
            service_matches = find_service(uuid=uuid[1], address=addr[1])

            if len(service_matches) == 0:
                print("Konnte Arduino nicht finden.")
                sys.exit(0)

        print "Device gefunden."
        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]


        server = tcpserver.get_server_socket()
        serversock, addr = server.accept()
        print "Accepted Incoming connection on Server Socket"
        print "Establishing BT connection. Please wait.."
        print("connecting to \"%s\" on %s" % (name, host))

        # Create the client socket
        sock = BluetoothSocket(RFCOMM)
        sock.connect((host, port))

        print("BT connected.")

        print "Bridging connections"


        # Two-Way Bridge
        a = PipeThread(serversock, sock)
        b = PipeThread(sock, serversock)

        a.start()
        b.start()

        a.join()
        b.join()

        server.close()
