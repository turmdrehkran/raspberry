
from abstract_response import AbstractResponse


class Response100(AbstractResponse):
    def __init__(self, params, status_message = "OPERATING"):
        AbstractResponse.__init__(self, 100, params, status_message)