#!/usr/bin/perl
use utf8;
use lib '/home/lisp-trpg';

print "Content-type: text/html \n\n";

foreach (@INC) {
    print;
    print "<br>";
}

