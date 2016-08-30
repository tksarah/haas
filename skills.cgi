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
        <form action="./haas/input_skill.cgi" method="post">
        <h4 id="archive">社員番号を入力（例：123456）</h4>
        <p>
        <input type="text" name="name" size="10">
        <input type="submit" value="Registration">
        </form>

HTML_OUT

}
