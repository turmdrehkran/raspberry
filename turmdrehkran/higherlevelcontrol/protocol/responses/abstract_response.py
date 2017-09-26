from turmdrehkran.higherlevelcontrol.protocol.codec import EncodeResponse


class ResponseMeaning:
    Informational, Success, ClientError, ServerError = range(4)
    map = {
        1: Informational,
        2: Success,
        4: ClientError,
        5: ServerError
    }


class AbstractResponse:
    def __init__(self, status_code, params, status_message):
        self.encoder = EncodeResponse()

        self.encoder.status_code = status_code
        self.encoder.status_message = status_message
        self.encoder.params = params

    def get_meaning(self):
        first_dig = self.encoder.status_code / 100
        return ResponseMeaning.map[first_dig]

    def encode(self):
        return self.encoder.encode()

    def __str__(self):
        return self.encode()

    def __repr__(self):
        return self.encode()