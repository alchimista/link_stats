#!/usr/bin/env python3
"""
Copyright (C) 2016 alchimista alchimistawp@gmail.com
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from pywikibot.comms.eventstreams import site_rc_listener
from sseclient import SSEClient as EventSource
import json


def stream(site, origin=False):
    if origin == "rcstream":
        try:

            for entry in site_rc_listener(site, ):
                return entry
        except:
            pass
    else:
        url = 'https://stream.wikimedia.org/v2/stream/recentchange'
        for event in EventSource(url):
            if event.event == 'message' and event.data:
                entry = json.loads(event.data)
                if (entry['type'] == 'edit') and (not entry['bot']) and (
                            entry['wiki'] == 'ptwiki'):
                    print (entry)
                    yield entry


            elif event.event == 'error':
                print('--- Encountered error', event.data)
                pass
