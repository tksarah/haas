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
my @list;

my $filename = "db.dat";

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $filename,
        -Flags    => DB_CREATE
    or die "Cannot open file $filename: $! $BerkeleyDB::Error\n";

# Main
header("$url");

@list = split(/,/,$h{$id});
handsref($url,$list[0],$list[3],$list[4],$list[5],$list[2]);

print "<br>完了したら以下の「 終了 」ボタンを押してください。環境がクリアされます。";
print "<center><form action=\"./cgi-bin/delete.cgi\" method=\"post\"><input type=\"hidden\" name=\"name\" value=\"$id\"><input type=\"submit\" value=\"終了\"></form></center>\n";

untie %h;
footer();

exit (0);
