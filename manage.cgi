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
my $atl_out = `sudo at -l`;
my $atq_out = `sudo atq`;
print "<h3>at list</h3><br>";
print "<h4>at -l</h4><br>";
print "$atl_out";
print "<h4>atq</h4><br>";
print "$atq_out";

# out docker
my $docker_out = `docker ps -a`;
print "<h3>docker list</h3><br>";
print "$docker_out";

footer();

exit (0);
