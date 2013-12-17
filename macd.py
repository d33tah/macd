#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""macd - periodically ARP-pings the network and creates a document which lists
names of all the machines that responded."""

# This file is part of tibiaproxy.
#
# tibiaproxy is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Joggertester is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

import subprocess
import time
import logging

import locale
locale.setlocale(locale.LC_TIME, '')

import gettext
t = gettext.translation('macd', 'locale', fallback=True)
_ = t.ugettext
# xgettext -d macd -o macd.pot macd.py
# msgfmt -o locale/pl/LC_MESSAGES/macd.mo macd.pot


NETWORK = "172.16.1.1/24"
OUTFILE = "index.html"
INTERVAL = 60
TIMEOUT = 60 * 5

def get_macs(network, do_sudo=True):
    ret = []
    sudo = ["sudo"] if do_sudo else []
    p = subprocess.Popen(sudo + ["nmap", network, "-sn", "-n"],
                         stdout=subprocess.PIPE)
    output = p.stdout.read()
    for line in output.split("\n"):
        if line.startswith("MAC"):
            mac = line.split()[2].lower()
            if mac not in ret:
                ret += [mac]
    return ret

def load_known():
    ret = {}
    with open("known.txt") as f:
        for line in f.readlines():
            line = line.rstrip("\r\n")
            mac, name = line.split("\t")
            mac = mac.lower()
            ret[mac] = name
    return ret

def load_ignored():
    ret = []
    try:
        with open("ignored.txt") as f:
            for mac in f.readlines():
                ret += [mac.rstrip("\r\n").lower()]
    except IOError:
        pass
    return ret

def get_since_time(since, mac):
    since_time = since[mac]
    if time.strftime("%x") == time.strftime("%x", since_time):
        return "(%s %s)" % (_("since"), time.strftime("%H:%M", since_time))
    else:
        return "(%s %s)" % (_("since"), time.strftime("%x %H:%M", since_time))

def generate_report(macs, known, since, ignored):
    ret = {'generated': time.strftime("%x %X"), 'items': []}
    empty = True
    for mac in set(macs + since.keys()):
        item = {}
        if mac in ignored:
            continue
        item['name'] = known.get(mac, "%s(?)" % mac)
        if mac not in macs:
            item['name'] = "(!) " + item['name']
        if mac not in since:
            since[mac] = time.localtime()
            item['since_msg'] = ""
        else:
            item['since_msg'] = get_since_time(since, mac)
        item['since'] = since[mac]

        found_later = False
        for i in range(len(ret['items'])):
            if ret['items'][i]['name'] != item['name']:
                continue
            if ret['items'][i]['since'] < since[mac]:
                ret['items'][i] = item
                found_later = True
                break
        if not found_later:
            ret['items'] += [item]
    return ret

def generate_html(report, filename=OUTFILE):
    with open(filename, "w") as f:
        f.write("<html><head><meta charset=\"utf-8\"/><title>mac</title>")
        f.write("<meta http-equiv=\"refresh\" content=\"%d\" />" % INTERVAL)
        f.write('<span class="generated">%s</span>\n' % report['generated'])
        wrote_ul = False
        for item in report['items']:
            if not wrote_ul:
                f.write("<ul>\n")
                wrote_ul = True
            f.write("<li>%s %s</li>\n" % (item['name'], item['since_msg']))
        if wrote_ul:
            f.write("</ul>\n")
        if len(report['items']) == 0:
            f.write('<p class="nobody">%s</p>' % _("Nobody was detected."))
        f.write("</body>\n</html>")

def cleanup_last_seen(macs, last_seen, since):
    for mac in set(macs + since.keys()):
        if mac in last_seen and time.time() - last_seen[mac] > TIMEOUT:
            if mac in since:
                del since[mac]
    for mac in macs:
        last_seen[mac] = time.time()

def main():
    FORMAT = "%(asctime)-15s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    since = {}
    last_seen = {}
    while True:
        known = load_known()
        ignored = load_ignored()
        macs = get_macs(NETWORK)
        cleanup_last_seen(macs, last_seen, since)
        logging.info("%s" % macs)
        report = generate_report(macs, known, since, ignored)
        generate_html(report)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
