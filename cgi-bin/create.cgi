#!/usr/bin/perl

require './lib.pl';
use strict ;
use CGI;
use BerkeleyDB;
use vars qw( %h $k $v );


# Get values
my $form = CGI->new;
my $id = $form->param('name');
my $type = $form->param('type');

# Variables
my $playhome = "/home/apache/haas";
my $filename = "db.dat";
my @list;

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $filename,
        -Flags    => DB_CREATE
    or die "Cannot open file $filename: $! $BerkeleyDB::Error\n";


# Check name,type exists/name duplicated
if($id eq ""){
	error_page(1);
        exit(1);
}elsif($type eq ""){
	error_page(2);
        exit(1);
}elsif($h{$id}){
	error_page(3);
        exit(1);
}

# Get time
my $btime = `TIMEZONE=Tokyo/Asia /bin/date '+%Y/%m/%d %H:%M:%S'`; chomp $btime;
my $atime = `TIMEZONE=Tokyo/Asia /bin/date '+%Y/%m/%d %H:%M:%S' -d '60 min'`; chomp $atime;

# Create ports
my $num = keys %h;
my $blog = 8081 + $num;
my $htty = 3000 + $num + 1;
my $ttty = $htty + 10;

# Check Open port
my $ret = system("ss -ltn | grep $blog");
if(!$ret){
	my $add = int(rand(99));
	$blog = $blog + $add;
	$htty = $htty + $add;
	$ttty = $ttty + $add;
}
	
# Generate portlist
my $port = "$blog,$htty,$ttty";

# Make string
my $string = "$type,$btime,$atime,$port";

## Run ansible
# ansible-playbook -i hosts -e "lesson=ansible-1 userid=tie304410 port=8080 htty=3001 ttty=3002" site.yml
## Crear
# ansible-playbook -i hosts -e "lesson=destroy userid=tie304410" site.yml

# Run Playbook
system("ansible-playbook -i $playhome/hosts -e \"lesson=$type userid=$id port=$blog htty=$htty ttty=$ttty\" $playhome/site.yml >& /dev/null &");

# Set k/v
$h{"$id"} = $string;

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

print "Create\n";
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
