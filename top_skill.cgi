#!/usr/bin/perl

require 'lib.pl';
use strict;

# Get values
my $host = get_value('host');

### OUTPUT HTML ###
header("$host");

print <<HTML;
	<h3>スキル熟練度</h3>
	<p>
	- <a href="./haas/skills.cgi" target="_blank">[ スキル登録/修正 ]</a><br>
	- <a href="./haas/result_skill.cgi" target="_blank">[ 全体・部 チェック ]</a><br>
	- <a href="./haas/user_skill.cgi" target="_blank">[ 個人 チェック ]</a><br>
	
        <p>
        <hr>
        <a href="./haas/manage.cgi">[ Manage Top ]</a>
HTML

footer();

exit (0);
