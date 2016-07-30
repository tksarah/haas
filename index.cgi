#!/usr/bin/perl

require './lib.pl';
use strict ;
use CGI;
use BerkeleyDB;
use vars qw( %h $k $v );

# Get values
my $host = get_value('host');
my $dbfilename = get_value('dbfilename');

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $dbfilename,
        -Flags    => DB_CREATE
    or die "Cannot open file $dbfilename: $! $BerkeleyDB::Error\n";


### OUTPUT HTML ###
header("$host");

# Output usage
usage();

# Registration List
userlist(%h);

# Output Registration Form
if (keys %h < 10){ input_form(); }
untie %h;

footer();

exit(0);
