django-metlog
=============

Django Metlog
=============

Integration between metlog and django. It allows you to use metlog to create 
timing or counter measurements with Metlog. Integrates with Django
middleware and Django Debug Toolbar.

Credits:

- andym, robhudson, jbalogh and jsocol for statsd, commonware,
  django-statsd and django-debug-toolbar

Changes
-------

0.1:

- Initial port of django-statsd to use metlog


Installation
------------

From pypi::

        pip install django-metlog-mozilla

Because there is already a pystatsd on pypi. This will be automatically added
when you install django-statsd-mozilla.

To use the Django debug toolbar, you must set the Metlog sender to use
the DebugCaptureSender.  All other metlog senders will not capture
data so the debug-toolbar will not function properly.

Usage
-----

To send timings from your code, use just like metlog, but change your imports
to read::

        from django.conf import settings
        metlog = settings.METLOG

To send timings or counts with every request, add in some middleware::

        MIDDLEWARE_CLASSES = (
                'django_metlog.middleware.GraphiteRequestTimingMiddleware',
                'django_metlog.middleware.GraphiteMiddleware',
                ) + MIDDLEWARE_CLASSES

To get timings for your database or your cache, put in some monkeypatches::

        STATSD_PATCHES = [
                'django_metlog.patches.db',
                'django_metlog.patches.cache',
        ]

Toolbar integration
-------------------

Make sure `django_statsd` is installed::

        INSTALLED_APPS = (
                ..
                'django_statsd',
        )

This will show you the statsd timings in the toolbar::

        MIDDLEWARE_CLASSES = (
                'debug_toolbar.middleware.DebugToolbarMiddleware',
                ) + MIDDLEWARE_CLASSES

Note: this must go before the GraphiteMiddleware so that we've got the timing
data in before we show the toolbar panel.

Add in the panel::

        DEBUG_TOOLBAR_PANELS = (
             ...
             'django_metlog.panel.StatsdPanel',
        )

You *must* set the metlog sender to use
`metlog.senders.DebugCaptureSender`.  See Metlog documentation on how
to do this. http://metlog-py.readthedocs.org/

Finally if you have production data coming into a graphite server, you can
show data from that server. If you have one, link it up::

Here's the configuration we use on AMO. Because triggers and counts go
to different spots, you can configure them differently::

        TOOLBAR_STATSD = {
                'graphite': 'https://graphite-phx.mozilla.org/render/',
                'roots': {
                        'timers': ['stats.timers.addons-dev', 'stats.timers.addons'],
                        'counts': ['stats.addons-dev', 'stats.addons']
                }
        }

The key is added on to the root. So if you've got a key of `view.GET` this
would look that up on the graphite server with the key::

        stats.addons.view.GET

Front end timing integration
----------------------------

New browsers come with an API to provide timing information, see:

http://w3c-test.org/webperf/specs/NavigationTiming/

To record this in metlog you need a JavaScript lib on the front end to send
data to the server. You then use the server to record the information. This
library provides a view to hook that up for different libraries.

First, make sure you can record the timings in your Django site urls. This
could be done by pointing straight to the view or including the URL for
example::

        from django_metlog.urls import urlpatterns as metlog_patterns

        urlpatterns = patterns('',
                ('^services/timing/', include(metlog_patterns)),
        )

In this case the URL to the record view will be `/services/timing/record`.

Second, hook up the client. There is a un-sophisticated client called `stick`
included in the static directory. This requires no configuration on your part,
just make sure that the file `django_metlog/static/stick.js` is in your sites
JS.

Then call it in the following manner::

        stick.send('/services/timing/record');

We also include support for `boomerang`, a sophisticated client from Yahoo:

http://yahoo.github.com/boomerang

To hook this up, first add in boomerang to your site, make sure you use the web
timing enabled version, as discussed here:

http://yahoo.github.com/boomerang/doc/howtos/howto-9.html

When the script is added to your site, add the following JS::

        BOOMR.init({
                beacon_url: '/services/timing/record'
        }).addVar('client', 'boomerang');

Once you've installed either boomerang or stick, you'll see the following keys
sent::

        window.performance.timing.domComplete 5309|ms
        window.performance.timing.domInteractive 3819|ms
        window.performance.timing.domLoading 1780|ms
        window.performance.navigation.redirectCount 0|c
        window.performance.navigation.type.reload 1|c

There's a couple of options with this you can set in settings::

STATSD_RECORD_KEYS (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A list of the keys you want to record, there's quite a few in the timing api
and you likely don't want to record them all. Here's the default::

        STATSD_RECORD_KEYS = [
                'window.performance.timing.domComplete',
                'window.performance.timing.domInteractive',
                'window.performance.timing.domLoading',
                'window.performance.navigation.redirectCount',
                'window.performance.navigation.type',
        ]

Override this to get different ones.

STATSD_RECORD_GUARD (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There's only limited ways to stop people posting junk to your URLs. By defining
this function you can do some work to allow requests to your needs. If the
function returns None, the request is allowed through. If you don't want to
allow the request, return any valid Django HTTP response. For example to deny
everyone not in INTERNAL_IPS::

        from django.http import HttpResponseForbidden

        def internal_only(request):
            if request.META['REMOTE_ADDR'] not in INTERNAL_IPS:
                return HttpResponseForbidden()

        STATSD_RECORD_GUARD = internal_only

Logging errors
~~~~~~~~~~~~~~

If you want to log a count of the errors in your application to statsd, you can
do this by adding in the handler. For example in your logging configuration::

    'handlers': {
        'test_statsd_handler': {
            'class': 'django_metlog.loggers.errors.StatsdHandler',
        },
    }

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

