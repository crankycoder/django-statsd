import logging

from django_statsd.clients import metlog_client


class StatsdHandler(logging.Handler):
    """Send error to statsd"""

    def emit(self, record):
        if not record.exc_info:
            return

        metlog_client.incr('error.%s' % record.exc_info[0].__name__.lower())
