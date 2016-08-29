#!/usr/bin/perl

require '../lib.pl';
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
my $datadir = "../data";
my $usersfile = "$datadir/USERS.list";
my $dbfilename = "$datadir/users.dat";


# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $dbfilename,
        -Flags    => DB_CREATE
    or die "Cannot open file $dbfilename: $! $BerkeleyDB::Error\n";

open(R,"<$usersfile");
while (<R>) {
	my $id = (split/,/,$_)[0];
	my $value = (split/,/,$_)[1];
	chomp($value);
	# Set k/v
	$h{"$id"} = $value;
}

# output
while (($k, $v) = each %h) {
	print "$k : $h{$k}\n";
}

untie %h;
exit (0);

