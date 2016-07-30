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
my $host = get_value('host');
my $dbfilename = get_value('dbfilename');
my @list;

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $dbfilename,
        -Flags    => DB_CREATE
    or die "Cannot open file $dbfilename: $! $BerkeleyDB::Error\n";

@list = split(/,/,$h{$id});
untie %h;

### OUTPUT HTML ###
header("$host");
handsref($host,$list[0],$list[3],$list[4],$list[5],$list[2],$id);
print "<br><br><br>完了したら以下の「 終了 」ボタンを押してください。環境がクリアされます。";
print "<center><form action=\"./haas/delete.cgi\" method=\"post\"><input type=\"hidden\" name=\"name\" value=\"$id\"><input id=\"button\" type=\"submit\" value=\"終了\"></form></center>\n";

howto();
footer();

exit (0);
