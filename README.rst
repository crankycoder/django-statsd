Django Metlog
=============

Integration between django and django. This is a port of Django Statsd (http://github.com/andym/django-statsd)
that uses metlog instead of a statsd client to send metrics.

The code assumes that you have a METLOG client instantiated and
configured in your django.conf.settings file.

more see our docs at: http://django-metlog.readthedocs.org/
