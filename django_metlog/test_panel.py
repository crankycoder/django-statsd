# ***** BEGIN LICENSE BLOCK *****
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# The Initial Developer of the Original Code is the Mozilla Foundation.
# Portions created by the Initial Developer are Copyright (C) 2012
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Victor Ng (vng@mozilla.com)
#
# ***** END LICENSE BLOCK *****
import threading
from mock import Mock
from metlog.client import MetlogClient
from metlog.senders import DebugCaptureSender
from nose.tools import eq_, ok_
from pprint import pprint
import json

def munge(msgs):
    # Munge the stats back into something easy for a template.
    results = []

    msgs = [json.loads(m) for m in msgs]
    msgs.sort(lambda x, y: cmp(x['fields']['name'], y['fields']['name']))

    collector = {}
    for msg in msgs:
        name = msg['fields']['name']
        type_ = msg['type']
        total = float(msg['payload']) * msg['fields']['rate'] 

        if name not in collector:
            collector[name] = {}
        if type_ not in collector[name]:
            collector[name][type_] = {'count': 0,
                'values': []}

        collector[name][type_]['values'].append(
                (float(msg['payload']), msg['fields']['rate']))


    for name in collector:
        for type_ in collector[name]:
            values = collector[name][type_]['values']
            total = sum([x * y for x, y in values])

            collector[name][type_]['total'] = total
            results.append({'name': name,
                            'type': type_,
                            'count': len(values),
                            'total': total,
                            'values': values})

    return results

class TestMetlogClient(object):
    logger = 'tests'
    timer_name = 'test'

    def setUp(self):
        self.mock_sender = DebugCaptureSender()
        self.client = MetlogClient(self.mock_sender, self.logger)
        # overwrite the class-wide threadlocal w/ an instance one
        # so values won't persist btn tests
        self.timer_ob = self.client.timer(self.timer_name)
        self.timer_ob.__dict__['_local'] = threading.local()

    def _extract_full_msg(self):
        return self.mock_sender.msgs[0]

    def test_panel(self):
        name = 'incr'
        self.client.incr('foo')
        self.client.incr('foo')
        self.client.incr('bar', rate=5)
        self.client.incr('batz', rate=2)
        self.client.incr('batz', rate=3)

        results = munge(self.client.sender.msgs)
        expected = [
                {'count': 2,
                    'name': u'foo',
                    'total': 2.0,
                    'type': u'counter',
                    'values': [(1.0, 1.0), (1.0, 1.0)]},
                {'count': 1,
                    'name': u'bar',
                    'total': 5.0,
                    'type': u'counter',
                    'values': [(1.0, 5)]},
                {'count': 2,
                    'name': u'batz',
                    'total': 5.0,
                    'type': u'counter',
                    'values': [(1.0, 2), (1.0, 3)]}
                ]
        eq_(results, expected)
