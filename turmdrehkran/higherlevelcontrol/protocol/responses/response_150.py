
from abstract_response import AbstractResponse


class Response150(AbstractResponse):
    def __init__(self, params, status_message = "OUTOFBOUND"):
        AbstractResponse.__init__(self, 150, params, status_message)