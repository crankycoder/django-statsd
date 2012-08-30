from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _, ungettext

from debug_toolbar.panels import DebugPanel
metlog = settings.METLOG


def munge(stats):
    # Munge the stats back into something easy for a template.
    results = []
    for stat in sorted(stats.keys()):
        values = stats[stat]
        name, type_ = stat.split('|')
        total = sum([x * y for x, y in values])
        data = {'name': name, 'type': type_,
                'count': len(values),
                'total': total,
                'values': values}
        results.append(data)
    return results


def times(stats):
    results = []
    start = stats[0][1]
    end = max([t[3] for t in stats])
    length = end - start
    for stat in stats:
        results.append([stat[0].split('|')[0],
                        # % start from left.
                        ((stat[1] - start - stat[2]) / float(length)) * 100,
                        # % width.
                        max(1, (stat[2] / float(length)) * 100),
                        stat[2],
                        ])
    return results


class MetlogPanel(DebugPanel):
    """
    TODO: (vng) This panel is broken 
    """

    name = 'Metlog'
    has_content = True

    def __init__(self, *args, **kw):
        super(MetlogPanel, self).__init__(*args, **kw)
        self.metlog = metlog

    def nav_title(self):
        return _('metlog')

    def nav_subtitle(self):
        length = len(self.metlog.cache) + len(self.metlog.timings)
        return ungettext('%s record', '%s records', length) % length

    def title(self):
        return _('Statsd')

    def url(self):
        return ''

    def content(self):
        context = self.context.copy()
        config = getattr(settings, 'TOOLBAR_METLOG', {})
        if 'roots' in config:
            for key in ['timers', 'counts']:
                context[key] = config['roots'][key]

        # TODO(vng): this needs to dip into the DebugCaptureSender
        # to extract all the properties
        # The existing code assumes that the statsd client is using
        # the django_statsd.clients.toolbar.StatsClient instance which
        # just captures timers and stores them for the toolbar
        context['graphite'] = config.get('graphite')

        # cache is a dictionary of statname -> [(count, rate), ...]
        context['statsd'] = munge(self.metlog.cache)

        # timings is a list of [(stat, now, delta, now+delta), ...]
        # where now = time.time()*1000
        context['timings'] = times(self.metlog.timings)
        return render_to_string('toolbar_statsd/statsd.html', context)

