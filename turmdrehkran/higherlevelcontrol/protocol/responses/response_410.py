
from abstract_response import AbstractResponse


class Response410(AbstractResponse):
    def __init__(self, params, status_message="SEMANTIC ERROR"):
        AbstractResponse.__init__(self, 410, params, status_message)