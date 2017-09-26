

class AbstractMethod:
    def __init__(self, request):
        self.request = request

    def execute(self, server):
        # type: (turmdrehkran.higherlevelcontrol.server.Server) -> turmdrehkran.higherlevelcontrol.responses.abstract_repsonse.AbstractResponse
        raise NotImplementedError()