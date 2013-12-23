#!/bin/bash

# Displays a list of unknown MAC addresses found in the macd.log, along with
# the number of entries in the log and the MAC vendor. The list is sorted by
# the number of entries.
#
# Usage:
#
# ./show-unknown.sh

for mac in `cat macd.log | \
            tr "'" '\n' | \
            grep '^..:..:..:..:..:..$' | \
            tr 'A-Z' 'a-z' | \
            uniq | \
            sort | \
            uniq | \
            grep -vi -F -f <( awk '{ print $1}' < known.txt )`; do

        MAC_NMAP=`echo $mac | tr a-z A-Z | tr -d ':' | cut -b1-6`
        VENDOR=`grep $MAC_NMAP /usr/share/nmap/nmap-mac-prefixes`
        echo -e "${mac}:\t`grep $mac macd.log | wc -l`\t$VENDOR"
    done | sort -n -k2 -r
