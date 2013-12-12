#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import time
import logging

NETWORK = "172.16.1.1/24"

def get_macs(network, do_sudo=True):
    ret = []
    sudo = ["sudo"] if do_sudo else []
    p = subprocess.Popen(sudo + ["nmap", network, "-sn", "-n"],
                         stdout=subprocess.PIPE)
    output = p.stdout.read()
    for line in output.split("\n"):
        if line.startswith("MAC"):
            mac = line.split()[2]
            ret += [mac]
    return ret

def load_known():
    ret = {}
    with open("known.txt") as f:
        for line in f.readlines():
            line = line.rstrip("\r\n")
            mac, name = line.split("\t")
            ret[mac] = name
    return ret

def write_macs(macs, known, filename="index.html"):
    with open(filename, "w") as f:
        f.write(time.strftime("%x %X<br/>\n<br/>\n"))
        for mac in macs:
            if mac in known:
                f.write("%s<br/>\n" % known[mac])
            else:
                f.write("%s (?)<br/>\n" % mac)


def main():
    FORMAT = "%(asctime)-15s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    known = load_known()
    while True:
        macs = get_macs(NETWORK)
        logging.info("%s" % macs)
        write_macs(macs, known)
        time.sleep(60)

if __name__ == "__main__":
    main()
