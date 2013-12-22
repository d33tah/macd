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
import datetime
import logging

import locale
locale.setlocale(locale.LC_TIME, '')

import gettext
t = gettext.translation('macd', 'locale', fallback=True)
_ = t.ugettext
# xgettext -d macd -o macd.pot macd.py
# msgfmt -o locale/pl/LC_MESSAGES/macd.mo macd.pot

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "macd.settings")

from macd.models import Device, Mac, SeenEvent


NETWORK = "172.16.1.1/24"
INTERVAL = 60

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

def register_macs(macs):
    for mac_str in macs:
        macs = Mac.objects.filter(mac=mac_str)
        if len(macs) == 0:
            device = Device()
            device.ignored = False
            device.save()
            mac = Mac()
            mac.device = device
            mac.mac = mac_str
            mac.save()
        else:
            assert(len(macs) == 1)
            mac = macs[0]
        event = SeenEvent()
        event.mac = mac
        event.date = datetime.datetime.now()
        event.save()

def main():
    FORMAT = "%(asctime)-15s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    while True:
        macs = get_macs(NETWORK)
        logging.info("%s" % macs)
        register_macs(macs)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
