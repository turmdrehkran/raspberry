import sock
import protocol.codec as codec
import protocol.method_provider as method_provider
from protocol.responses.abstract_response import ResponseMeaning
from protocol.responses import Response400, Response500

from turmdrehkran.exceptions import TurmdrehkranException, CodecDecodeException, ConnectionTerminatedException

from turmdrehkran.gpio.handler.gpio_mock_handler import GpioMockHandler
from turmdrehkran.gpio.control.gpio_controller import GpioController

try:
    from bluetooth.btcommon import BluetoothError
except:
    class BluetoothError(Exception):
        pass


class Server:
    def __init__(self, sockmodule, gpiocontroller):
        self.gpiocontroller = gpiocontroller
        self.socket = sockmodule
        self.running = True
        self.accepts_requests = True

        self.client_sock = None
        self.client_info = None

        self.client_payload = None
        self.client_request = None
        self.client_method = None

    def get_controller(self):
        return self.gpiocontroller

    def run(self):
        while self.running:
                self.client_sock, self.client_info = self.socket.accept()

                # Signal connection
                self.accepts_requests = True
                self.gpiocontroller.handsteuerung_lock()
                self.handle()
                self.client_sock.close()
                self.gpiocontroller.handsteuerung_enable()

    @staticmethod
    def payload_reader(client_sock):
        try:
            buffer = ''
            while True:
                read = client_sock.recv(1024)
                buffer += read

                if read == '':
                    raise ConnectionTerminatedException("Connection Resetter")

                if buffer[-2:] == '\n\n': # Terminator seen
                    break

            return buffer
        except BluetoothError as e:
            raise ConnectionTerminatedException(e.message)

    def send_intermittent_response(self, response):
        """
        Sendet eine informative zwischenzeitliche Antwort auf eine Anfrage
        :param response:
        :return:
        """
        # type: (turmdrehkran.higherlevelcontrol.protocol.responses.abstract_response.AbstractResponse) -> None
        if response.get_meaning() != ResponseMeaning.Informational:
            raise TurmdrehkranException("Intermittent Response can only be informational.")
        self.client_sock.sendall(str(response))

    def send_final_response(self, response):
        """
        Sendet die finale Antwort auf eine Anfrage
        :param response:
        :return:
        """
        if response.get_meaning() == ResponseMeaning.Informational:
            raise TurmdrehkranException("Final Response can not be informational.")
        self.client_sock.sendall(str(response))

    def handle(self):
        while self.accepts_requests:
            try:
                # Read Message from wire
                payload = self.payload_reader(self.client_sock)

                # Deserialize
                request = codec.DecodeRequest(payload)

                # Match to known methods
                method = method_provider.get_method(request)

                # Evaluate Method
                final_response = method.execute(self)

                # Send Response
                self.send_final_response(final_response)

            except CodecDecodeException as e:
                self.send_final_response(Response400({"Message": e.message}))

            except ConnectionTerminatedException:
                self.accepts_requests = False

            except Exception as e:
                self.send_final_response(Response500({"Message"}))
                print e
