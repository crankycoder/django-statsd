from django_statsd.clients import metlog_client
from functools import partial


def wrapped(method, key, *args, **kw):
    with metlog_client.timer(key):
        return method(*args, **kw)


def wrap(method, key, *args, **kw):
    return partial(wrapped, method, key, *args, **kw)
