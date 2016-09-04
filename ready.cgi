#!/usr/bin/perl

require 'lib.pl';
use strict;

# Get values
my $host = get_value('host');

### OUTPUT HTML ###
header("$host");

print "準備中。\n";

footer();

exit (0);
