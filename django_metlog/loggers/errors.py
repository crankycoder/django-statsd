import logging

from django.conf import settings
metlog = settings.METLOG


class StatsdHandler(logging.Handler):
    """Send error to statsd"""

    def emit(self, record):
        if not record.exc_info:
            return

        metlog.incr('error.%s' % record.exc_info[0].__name__.lower())
