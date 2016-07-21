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

untie %h;

### OUTPUT HTML ###
header("$host");

# Registration List
userlist(%h);

# out logfile
log_page();

# out at
my $at_out = `sudo at -l`;
print "<h3>AT</h3><br>";
print "$at_out";

# out docker
my $docker_out = `docker ps -a`;
print "<h3>Docker</h3><br>";
print "$docker_out";

footer();

exit (0);
