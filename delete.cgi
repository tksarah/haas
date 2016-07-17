#!/usr/bin/perl

require './lib.pl';
use strict ;
use CGI;
use BerkeleyDB;
use vars qw( %h $k $v );

# From POST
my $form = CGI->new;
my $id = $form->param('name');

# Get values
my $url = get_value('url');
my $playhome = get_value('playhome');
my $inventory = get_value('inventory');
my $inventoryfile = "$playhome/$inventory";
my $playbook = get_value('playbook');
my $playbookfile = "$playhome/$playbook";
my $dbfilename = get_value('dbfilename');
my $logfile = get_value('logfile');

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $dbfilename,
        -Flags    => DB_CREATE
    or die "Cannot open file $dbfilename: $! $BerkeleyDB::Error\n";


# Check HTTP
my @list = split(/,/,$h{$id});
my $status = check_http($url,$list[3]);
# Logging
logging($id,@list,$status,$logfile);

# K/V Delete 
delete $h{$id};

# Destroy id
destroy($id,$inventoryfile,$playbookfile);
untie %h;

### OUTPUT HTML ###
header("$url");
print "お疲れ様でした。\n";
footer();

exit (0);
