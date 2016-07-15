#!/usr/bin/perl

require './lib.pl';
use strict ;
use CGI;
use BerkeleyDB;
use vars qw( %h $k $v );

# Get values
my $form = CGI->new;
my $id = $form->param('name');

my $filename = "db.dat";
my @list;

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $filename,
        -Flags    => DB_CREATE
    or die "Cannot open file $filename: $! $BerkeleyDB::Error\n";

# Delete 
delete $h{$id};

# Main
print <<HEADER;
Content-type: text/html

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="html://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
 <head>
  <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8"/>
  <title>Handson as a Service</title>
  <base href="http://192.168.166.210/"/>
  <link rel="stylesheet" type="text/css" href="default.css"/>
 </head>

<body>

<div id="header">
  <h2>Handson as a Service</h2>
</div>

<div id="content">
HEADER

print "Delete";
userlist(%h);
untie %h;


print <<FOOTER;
</div>

<div id="footer">
  <em>
  <font size="2" color="#508090">
  COPYRIGHT(C) 2016 「Hands on as a Service」 version 0.1<BR>
  ALL RIGHTS RESERVED<BR>
  Author:TK<BR>
  </FONT>
  </em>
</div>

</body>
</html>
FOOTER

exit (0);
