
from abstract_method import AbstractMethod
from turmdrehkran.higherlevelcontrol.protocol.responses import Response410


class UnknownMethod(AbstractMethod):

    def execute(self, server):
        # type: (turmdrehkran.higherlevelcontrol.server.Server) -> turmdrehkran.higherlevelcontrol.responses.abstract_repsonse.AbstractResponse
        return Response410({"Message": "Unknown Method Name '"+ self.request.method +"'"})