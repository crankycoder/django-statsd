from django.conf import settings
metlog = settings.METLOG
from functools import partial


def wrapped(method, key, *args, **kw):
    with metlog.timer(key):
        return method(*args, **kw)


def wrap(method, key, *args, **kw):
    return partial(wrapped, method, key, *args, **kw)
