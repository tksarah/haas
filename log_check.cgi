#!/usr/bin/perl

require './lib.pl';
use strict ;
use CGI;

# Get values
my $host = get_value('host');
my $logfile = get_value('logfile');
my $log = `cat $logfile`;
my $x;


### OUTPUT HTML ###
header("$host");

print "<h3>log</h3><br>\n";
print "<table>\n";
print "<tr><th>ID</th><th>Type</th><th>Start</th><th>End</th><th>Blog</th><th>Htty</th><th>Ttty</th><th>Status</th><th>Finish</th><th>Duration(min)</th></tr>\n";

# out logfile
open(R,"<$logfile");
while (<R>) {
	print "<tr>";

	my @cols = split(/,/,$_);
	foreach $x (@cols){
	print "<td>$x</td>";
	}
	print "</tr>\n";
}
close(R);
print "</table>\n";
print "</p>\n";

# out at
my $atl_out = `sudo at -l`;
my $atq_out = `sudo atq`;
print "<h3>at list</h3>";
print "<h4>at -l</h4>";
print "<pre style=\"padding-left: 20px\">$atl_out</pre>";
print "<h4>atq</h4>";
print "<pre style=\"padding-left: 20px\">$atq_out</pre>";

# out docker
my $docker_out = `docker ps -a`;
print "<h3>container list</h3>";
print "<pre style=\"padding-left: 20px\">$docker_out</pre>";

footer();

exit (0);
