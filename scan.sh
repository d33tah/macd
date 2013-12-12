#!/bin/sh
#
# scan.sh
#
# Scans the FLL network, saving the MAC addresses of hosts that are up to
# mac.txt file.

NETWORK="192.168.88.84/24"

while sleep 60; do
    # perform a verbose discovery scan on the network without rDNS queries
    # filter 3rd column of the output if 1st is "MAC"
    sudo nmap $NETWORK -sn -v -n | \
        awk '$1 == "MAC" { print $3 }' > mac.txt
done
