#!/bin/bash

# Displays a list of unknown MAC addresses found in the macd.log.
#
# Usage:
#
# ./show-unknown.sh

cat macd.log | \
    tr "'" '\n' | \
    grep '^..:..:..:..:..:..$' | \
    tr 'A-Z' 'a-z' | \
    uniq | \
    sort | \
    uniq | \
    grep -vi -F -f <( awk '{ print $1}' < known.txt )
