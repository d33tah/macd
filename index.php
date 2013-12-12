<?php

# Reads the MAC -> machine name dictionary from known.txt and displays the
# names of machines found in mac.txt.

$known = array();

foreach(file("known.txt") as $line) {
    $split = explode("\t", $line);
    $mac = strtolower($split[0]);
    $known[$mac] = $split[1];
}

foreach(file("mac.txt") as $line) {
    $mac = chop(strtolower($line));
    echo $known[$mac] . "<br />";
}
