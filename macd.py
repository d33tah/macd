#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
                ret += [mac.rstrip("\r\n")]
    except IOError:
        pass
    return ret

def get_since_time(since, mac):
    if mac not in since:
        since[mac] = time.localtime()
    since_time = since[mac]
    if time.strftime("%x") == time.strftime("%x", since_time):
        return "(%s %s)" % (_("since"), time.strftime("%H:%M", since_time))
    else:
        return "(%s %s)" % (_("since"), time.strftime("%x %H:%M", since_time))

def write_macs(macs, known, since, ignored, filename=OUTFILE):
    with open(filename, "w") as f:
        f.write("<html><head><meta charset=\"utf-8\"/><title>mac</title>")
        f.write("<meta http-equiv=\"refresh\" content=\"%d\" />" % INTERVAL)
        f.write(time.strftime("%x %X<br/>\n<br/>\n"))
        empty = True
        for mac in set(macs + since.keys()):
            if mac in ignored:
                continue
            name = known.get(mac, "%s(?)" % mac)
            if mac not in macs:
                name = "(!) " + name
            if mac not in since:
                since[mac] = time.localtime()
                since_msg = ""
            else:
                since_msg = get_since_time(since, mac)
            f.write("%s %s<br/>\n" % (name, since_msg))
            empty = False
        if empty:
            f.write(_("Nobody was detected."))
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
        write_macs(macs, known, since, ignored)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
