#!/usr/bin/perl

require './lib.pl';
use strict ;
use CGI;
use BerkeleyDB;
use vars qw( %h $k $v );

my $filename = "db.dat";
my @list;

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $filename,
        -Flags    => DB_CREATE
    or die "Cannot open file $filename: $! $BerkeleyDB::Error\n";


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

print "<h3>利用方法</h3>";
print "<ul id=\"list\">\n";
print "<li>■ <b>社員番号を入力</b>します</li>\n";
print "<li>■ <b>ハンズオンの種類を選択</b>します</li>\n";
print "<li>■ 「ハンズオンビルド」ボタンを押すと、ハンズオンの環境が作られます</li>\n";
print "<li>■ ハンズオンの環境の情報ページに沿って<b>環境にアクセスし実施</b>します</li>\n";
print "<li>■ ハンズオン実施の工数は<u>各部の教育工数としてカウント</u>されるようトレースされます</li>\n";
print "</ul>\n";

print "<h4>注意と制限</h4>";
print "<ul id=\"list\">\n";
print "<li>■ ハンズオンの環境は<font color=red><b>60分</b></font>で自動的に削除されます</li>\n";
print "<li>■ 同じ社員が同時に2つ以上のハンズオンを実行できません</li>\n";
print "<li>■ <font color=red>10社員</font>までが同時に本サービスを利用可能です</li>\n";
print "</ul>\n";

if (keys %h == 10){
	userlist(%h);
}else{
	input_form();
	userlist(%h);
}

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

exit(0);
