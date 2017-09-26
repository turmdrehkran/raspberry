
import erbjungbluthevent


def Event(*args, **kwargs):
    """A factory function that returns a new event.

    Events manage a flag that can be set to true with the set() method and reset
    to false with the clear() method. The wait() method blocks until the flag is
    true.

    """
    return erbjungbluthevent.ErbJungbluthEvent(*args, **kwargs)