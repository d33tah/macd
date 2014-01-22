macd
====

An application I wrote for Fab Lab Łódź hackerspace to keep track of who's in
the building. It periodically ARP-pings the network and creates a document
which lists names all the machines that responded.

Usage
=====

1. Create the known.txt file, which contains a tab-separated table. The first
row should contain the known MAC address, the second row is the label for the
MAC.
2. Edit macd.py by setting NETWORK to the IP/network mask of the network you
want to be scanned,
3. Run macd.py and point the user to the index.html file that macd generates.

TODO
====

1. Make the admin panel more convenient.

2. Create a mobile version of the website.

Author, license
===============

This application was written by Jacek Wielemborek <d33tah@gmail.com>. My blog
can be found here: http://deetah.jogger.pl/kategoria/english/

If you're not a viagra vendor, feel free to write me an e-mail, I'd be happy
to hear that you use this program!

This program is Free Software and is protected by GNU General Public License
version 3. Basically, it gives you four freedoms:


Freedom 0: The freedom to run the program for any purpose.

Freedom 1: The freedom to study how the program works, and change it to make
    it do what you wish.

Freedom 2: The freedom to redistribute copies so you can help your neighbor.

Freedom 3: The freedom to improve the program, and release your improvements
    (and modified versions in general) to the public, so that the whole
     community benefits.

In order to protect that freedom, you must share any changes you did to the
program with me, under the same license. For details, read the COPYING.txt
file attached to the program.
