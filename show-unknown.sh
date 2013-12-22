#!/bin/bash

# Displays a list of unknown MAC addresses found in the macd.log.
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
        echo "$mac: `grep $mac macd.log | wc -l`"
    done | sort -n -k2 -r
