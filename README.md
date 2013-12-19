macd
====

An application I wrote for Fab Lab Łódź to keep track of who's in the building.
It periodically ARP-pings the network and creates a document which lists names
all the machines that responded.

Usage
=====

1. Create the known.txt file, which contains a tab-separated table. The first
row should contain the known MAC address, the second row is the label for the
MAC.
2. Edit macd.py by setting NETWORK to the IP/network mask of the network you
want to be scanned,
3. Run macd.py and point the user to the index.html file that macd generates.
