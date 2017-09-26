
from abstract_response import AbstractResponse


class Response500(AbstractResponse):
    def __init__(self, params, status_message="INTERNAL SERVER ERROR"):
        AbstractResponse.__init__(self, 500, params, status_message)