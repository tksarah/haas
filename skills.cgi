#!/usr/bin/perl

require './lib.pl';
use strict;
use CGI;
use DateTime;
use BerkeleyDB;
use File::Basename;
use vars qw( %h $k $v );

# From POST
my $form = CGI->new;
my $user = $form->param('user');


# Get values
my $host = get_value('host');
#my $logfile = get_value('logfile');
my $datadir = "./data";
my $usersfile = "$datadir/USERS.list";
my $dbfilename = "$datadir/users.dat";


# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $dbfilename,
        -Flags    => DB_CREATE
    or die "Cannot open file $dbfilename: $! $BerkeleyDB::Error\n";


### OUTPUT HTML ###
header("$host");

while (($k, $v) = each %h) {
        print "<b>$k</b> : $h{$k}<br>\n";
}
untie %h;

print <<FOOTER;
<p>
<hr>
</div>

<div id="footer">
  <em>
  <font size="2" color="#508090">
  COPYRIGHT(C) 2016 「Hands on as a Service」<BR>
  ALL RIGHTS RESERVED<BR>
  Author:TK<BR>
  </FONT>
  </em>
</div>

</body>
</html>
FOOTER

exit (0);

