#!/usr/bin/perl

require './lib.pl';
# yum install perl-DateTime
use DateTime;
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

# Registration List
print "<h3>利用状況</h3><br>";
print "<table>\n";
print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th><th>Destroy</th></tr>\n";

while (($k, $v) = each %h) {
	my @list = split(/,/,$v);
	print "<tr>";
	print "<td><a href=\"./cgi-bin/myhandson.cgi?name=$k\">$k</a></td>";
	print "<td>$list[0]</td>";
	print "<td>$list[1]</td>";
	print "<td>$list[2]</td>";
	print "<td><form action=\"./cgi-bin/delete.cgi\" method=\"post\"><input type=\"hidden\" name=\"name\" value=\"$k\"><input type=\"submit\" value=\"Destroy\"></form></td>";
	print "</tr>\n";
	}

print "</table>\n";
print "</p>\n";
untie %h;

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
