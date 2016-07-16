#!/usr/bin/perl

require './lib.pl';
use strict ;
use CGI;
use BerkeleyDB;
use vars qw( %h $k $v );

my $filename = "db.dat";
my $url = get_value('url');

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $filename,
        -Flags    => DB_CREATE
    or die "Cannot open file $filename: $! $BerkeleyDB::Error\n";


# Main
header("$url");

# Registration List
userlist(%h);


print "<br>\n";
print "<div id=\"content\">\n";
print "<h3>利用方法</h3>";
print "<ul id=\"list\">\n";
print "<li>■ <b>社員番号を入力</b>します</li>\n";
print "<li>■ <b>ハンズオンの種類を選択</b>します</li>\n";
print "<li>■ 「ハンズオンビルド」ボタンを押すと、ハンズオンの環境が作られます</li>\n";
print "<li>■ ハンズオンの環境の情報ページに沿って<b>環境にアクセスし実施</b>します</li>\n";
print "<li>■ ハンズオン実施の工数は<u>各部の教育工数としてカウント</u>されるようトレースされます</li>\n";
print "</ul>\n";

print "<h4>前提および、保持スキル</h4>";
print "<ul id=\"list\">\n";
print "<li>■ 社内で開催している<b>「 Ansible or Serverspec の概要編 」</b>を受講済み、または同等の知識を保持</li>\n";
print "<li>■ Unix/Linuxオペレーション1年以上の経験、またはLPIC Level 1 同等以上の知識を保持</li>\n";
print "<li>■ 最低限、viによるファイル編集、基本的なUnix/Linuxオペレーション、公開鍵認証の基本を保持</li>\n";
print "</ul>\n";

print "<h4>注意と制限</h4>";
print "<ul id=\"list\">\n";
print "<li>■ ハンズオンの環境は<font color=red><b>60分</b></font>で自動的に削除されます</li>\n";
print "<li>■ 同じ社員が同時に2つ以上のハンズオンを実行できません</li>\n";
print "<li>■ <font color=red>10社員</font>までが同時に本サービスを利用可能です</li>\n";
print "</ul>\n";
print "</div>\n";

# Registration
if (keys %h < 10){ input_form(); }

untie %h;

footer();

exit(0);
