from turmdrehkran.higherlevelcontrol.protocol.methods.run import RunMethod
from turmdrehkran.higherlevelcontrol.protocol.methods.unknown import UnknownMethod
from turmdrehkran.higherlevelcontrol.protocol.codec import DecodeRequest


map = {
    "RUN": RunMethod
}


def get_method(request):
    try:
        return map[request.method](request)
    except KeyError:
        return UnknownMethod(request)

