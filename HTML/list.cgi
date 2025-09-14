#!/usr/bin/perl

use strict;
use warnings;
use utf8;
use URI::Escape;


print "Content-type: text/html \n\n";
print '<html><head><meta charset="utf-8"/>';
print '<body>';

my $url;
my $file;

while(<*.html>){
    $file = $_;
    $url = uri_escape $file;
    print "<a href=$url>$file</a>"."<br>\n";
}
print '</body></html>';
