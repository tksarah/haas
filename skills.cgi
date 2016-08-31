#!/usr/bin/perl

require './lib.pl';
use strict;
use CGI;

# Get values
my $host = get_value('host');

### OUTPUT HTML ###
header("$host");

output_html();

footer();

exit (0);

sub output_html{
	print <<HTML_OUT;

	<h3>新規登録・既存編集</h3>
        <ul id="list">
           <li>新規の場合も既に登録されている場合も自身のIDを入力します</li>
           <li>新規の場合は、すべての項目は初期値が「1」でフォームが出現します</li>
           <li>登録済みの場合は、設定済みの値がチェック済みの状態でフォームが出現します</li>
        </ul>
        <form action="./haas/input_skill.cgi" method="post">
        <h4 id="archive">社員番号を入力（例：123456）</h4>
        <p>
        <input type="text" name="name" size="6">
        <input type="submit" value="Registration">
        </form>

HTML_OUT

}
