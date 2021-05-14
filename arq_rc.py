#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pywikibot
import difflib
import re
from pywikibot.comms.eventstreams import site_rc_listener
from sseclient import SSEClient as EventSource
import json

site = pywikibot.Site("pt", "wikipedia")


class arquivo():
    def __init__(self, site):
        self.site = site

    def stream(self, origin=False):
        if origin == "rcstream":
            try:

                for entry in site_rc_listener(self.site, ):
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
                        yield entry


                elif event.event == 'error':
                    print('--- Encountered error', event.data)
                    pass

    def has_url(self, string):

        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, string)
        return [x[0] for x in url]

    def compare_edits(self, entry):
        self.new = entry['revision']['new']
        self.old = entry['revision']['old']

        new_text = self.page.getOldVersion(self.new)
        old_text = self.page.getOldVersion(self.old)

        d = difflib.Differ()
        diff_info = list(d.compare(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True)))

        for i in diff_info:

            # print(self.has_url(i), i)
            if self.has_url(i) and i.startswith('+'):
                for k in self.has_url(i):

                    try:

                        if entry['url']:
                            entry['url'] = entry['url'].append(k)
                    except:
                        entry['url'] = k

                msg = entry['title'], entry['timestamp'], entry['url'], entry['revision']['old'], entry['revision'][
                    'new'], entry[
                          'namespace'], entry['comment'], entry['user'], entry
                m = str(msg) + "\n"
                with open("links.txt", 'a') as file:
                    file.write(m)

    def run(self):
        for entry in self.stream(site):

            if (entry['type'] == 'edit') and (not entry['bot']) and (
                    entry['wiki'] == 'ptwiki'):
                # print("------", entry['title'], entry['timestamp'], entry['revision']['old'], entry['revision']['new'],
                #       entry['namespace'], entry['comment'], entry['user'], entry)

                self.page = pywikibot.Page(self.site, entry['title'])

                self.compare_edits(entry)


if __name__ == '__main__':
    arquivo = arquivo(site)
    arquivo.run()
