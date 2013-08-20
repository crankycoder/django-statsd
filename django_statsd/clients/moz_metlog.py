# This module exists only as a backwards compatible namespace until
# all Mozilla apps using django-statsd using Metlog have been upgraded
# to using Heka.
from django_statsd.clients.moz_heka import StatsClient
