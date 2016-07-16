#!/usr/bin/perl

require './lib.pl';
use strict ;
use CGI;
use BerkeleyDB;
use vars qw( %h $k $v );

# Get values
my $url = get_value('url');
my $form = CGI->new;
my $id = $form->param('name');

my $inventory = "/home/apache/haas/hosts";
my $playbook = "/home/apache/haas/site.yml";
my $filename = "db.dat";

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $filename,
        -Flags    => DB_CREATE
    or die "Cannot open file $filename: $! $BerkeleyDB::Error\n";

# K/V Delete 
delete $h{$id};

# Main
header("$url");
destroy($id,$inventory,$playbook);
print "お疲れ様でした。\n";
footer();

exit (0);
