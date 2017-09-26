from turmdrehkran.exceptions import *


class DecodeRequest:
    def __init__(self, request):
        self.request = request
        self.request_stack = []

        self._parameters = {}

        self.__read()
        self.__cleanup_request_stack()
        self.__analyze()

    def __read(self):
        lines = self.request.splitlines(True)

        for line in lines:
            self.request_stack.append(line)

        if self.request_stack[-1] != "\n":
            raise CodecDecodeException("Missing Terminator symbol")

    def __cleanup_request_stack(self):
        """
        Entfernt alle Eintraege die genau ein Newline-Zeichen sind und entfernt alle Newline-Zeichen, die sich am Ende eiens strings befinden.
        :return:
        """
        current_stack = self.request_stack
        new_stack = []

        for el in current_stack:
            if el[-1] == "\n" and len(el) > 1:
                new_stack.append(el[:-1])

        self.request_stack = new_stack

    def __analyze(self):
        """
        Evaluates the previously recorded request
        :return:
        """
        if len(self.request_stack) < 1:
            raise CodecDecodeException("Invalid Request Format.")

        current_stack = self.request_stack

        method_parts = current_stack.pop(0).split(" ")
        self._request_method = method_parts.pop(0)
        self._request_method_args = method_parts

        for params in current_stack:
            # Split on first occurence
            parts = params.split(":", 1)

            # Parameters sind fehlerhaft
            if len(parts) != 2:
                raise CodecDecodeException("Parameter Syntax incorrect")

            key = parts[0].strip()
            value = parts[1].strip()

            if not key or not value:
                raise CodecDecodeException()

            self._parameters[key] = value

    @property
    def method(self):
        return self._request_method

    @property
    def method_args(self):
        return self._request_method_args

    @property
    def params(self):
        return self._parameters

    def __str__(self):
        return "Request["+self.method + " " + str(self.method_args) + " " + str(self.params)+"]"

    def __repr__(self):
        return self.__str__()


class DecodeResponse:
    def __init__(self, request):
        self.request = request
        self._parameters = {}
        self.request_stack = []

        self.__read()
        self.__cleanup_request_stack()
        self.__analyze()

    def __read(self):
        lines = self.request.splitlines(True)

        for line in lines:
            self.request_stack.append(line)  #

        if self.request_stack[-1] != "\n":
            raise CodecDecodeException("Missing Terminator symbol")

    def __cleanup_request_stack(self):
        """
        Entfernt alle Eintraege die genau ein Newline-Zeichen sind und entfernt alle Newline-Zeichen, die sich am Ende eiens strings befinden.
        :return:
        """
        current_stack = self.request_stack
        new_stack = []

        for el in current_stack:
            if el[-1] == "\n" and len(el) > 1:
                new_stack.append(el[:-1])

        self.request_stack = new_stack

    def __analyze(self):
        """
        Evaluates the previously recorded request
        :return:
        """
        if len(self.request_stack) < 1:
            raise CodecDecodeException("Invalid Request Format. Line Endings seem to be missing!")

        current_stack = self.request_stack

        status_parts = current_stack.pop(0).split(" ")
        self._status_code = int(status_parts.pop(0))
        self._status_message = ' '.join(status_parts)

        for params in current_stack:
            # Split on first occurence
            parts = params.split(":", 1)

            # Parameters sind fehlerhaft
            if len(parts) != 2:
                raise CodecDecodeException()

            key = parts[0].strip()
            value = parts[1].strip()

            if not key or not value:
                raise CodecDecodeException()

            self._parameters[key] = value

    @property
    def status_code(self):
        return self._status_code
    @property
    def status_message(self):
        return self._status_message

    @property
    def params(self):
        return self._parameters


class EncodeRequest:
    def __init__(self):
        self._method = None
        self._method_args = []
        self._params = {}

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, val):
        if not isinstance(val, str):
            raise ValueError()
        self._method = val

    @property
    def method_args(self):
        return self._method_args

    @method_args.setter
    def method_args(self, val):
        if not isinstance(val, list):
            raise ValueError()
        self._method_args = val

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, val):
        if not isinstance(val, dict):
            raise ValueError()
        self._params = val

    def encode(self):
        buffer = ""

        buffer += self.method + " " + str.join(" ", self.method_args) + "\n"
        for key, value in self.params.iteritems():
            buffer += str(key) + ": " + str(value) + "\n"

        return buffer + "\n"

    def __str__(self):
        return self.encode()

    def __repr__(self):
        return self.__str__()


class EncodeResponse:
    def __init__(self):
        self._status_code = 100
        self._status_message = ""
        self._params = {}

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, val):
        if not isinstance(val, int):
            raise ValueError()
        self._status_code = val

    @property
    def status_message(self):
        return self._status_message

    @status_message.setter
    def status_message(self, val):
        if not isinstance(val, str):
            raise ValueError()
        self._status_message = val

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, val):
        if not isinstance(val, dict):
            raise ValueError()
        self._params = val

    def encode(self):
        buffer = ""

        buffer += str(self.status_code) + " " + self.status_message + "\n"
        for key, value in self.params.iteritems():
            buffer += str(key) + ": " + str(value) + "\n"

        return buffer + "\n"

    def __str__(self):
        return self.encode()

    def __repr__(self):
        return self.__str__()