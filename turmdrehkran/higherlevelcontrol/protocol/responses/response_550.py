
from abstract_response import AbstractResponse


class Response550(AbstractResponse):
    def __init__(self, params, status_message = "OUTOFBOUND"):
        AbstractResponse.__init__(self, 550, params, status_message)