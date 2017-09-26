
from abstract_response import AbstractResponse


class Response400(AbstractResponse):
    def __init__(self, params, status_message="SYNTAX ERROR"):
        AbstractResponse.__init__(self, 400, params, status_message)