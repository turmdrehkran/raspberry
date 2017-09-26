
from abstract_response import AbstractResponse


class Response200(AbstractResponse):
    def __init__(self, params, status_message="OK"):
        AbstractResponse.__init__(self, 200, params, status_message)