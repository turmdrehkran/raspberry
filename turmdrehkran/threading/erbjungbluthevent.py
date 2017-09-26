
import threading


class ErbJungbluthEvent(threading._Event):

    def __init__(self, *args, **kwargs):
        super(ErbJungbluthEvent, self).__init__()
        self.param = False

    def set(self):
        self.param = False
        super(ErbJungbluthEvent, self).set()

    def paramSet(self, param):
        self.param = param
        super(ErbJungbluthEvent, self).set()

    def paramIsSet(self):
        return self.param