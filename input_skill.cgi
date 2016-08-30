#!/usr/bin/perl

require './lib.pl';
use strict;
use CGI;
use DateTime;
use File::Basename;
use JSON;

# From POST
my $form = CGI->new;
my $user = $form->param('id');
$user = "000000" if ($user eq "");

# Get values
my $host = get_value('host');
my $datadir = "../testdata";
my $userdata = "$datadir/$user";

### OUTPUT HTML ###
header("$host");

my $items = parse_json($userdata);
input_func($items);

print <<FOOTER;
<p>
<hr>
<a href="./haas/manage.cgi">[ Manage Top ]</a>
<p>
</div>

<div id="footer">
  <em>
  <font size="2" color="#508090">
  COPYRIGHT(C) 2016 「Hands on as a Service」<BR>
  ALL RIGHTS RESERVED<BR>
  Author:TK<BR>
  </FONT>
  </em>
</div>

</body>
</html>
FOOTER

exit (0);

sub input_func{

	$items = shift;
        my $shift = $items->{skill}->[0]->{Shift};
	my $auto = $items->{skill}->[0]->{Automation}->[0];
	my $test = $items->{skill}->[0]->{Test}->[0];
	my $cloud = $items->{skill}->[0]->{Cloud}->[0];

	my $i;

	print <<HTML_1;

	<h3>スキルレベルを登録</h3><p>
        <form action="./haas/reg_skill.cgi" method="post">

        <h4 id="archive">社員番号を入力（例：123456）</h4>
	<p>
        <input type="text" name="name" size="10">
HTML_1

	print "<h4 id=\"archive\">Shift</h4>\n";
	print "<p>\n";
	for ($i=1;$i<6;$i++){
		if($shift == $i){
			print "<input type=\"radio\" name=\"Shift\" value=\"$i\" checked>$i\n";
		}else{
			print "<input type=\"radio\" name=\"Shift\" value=\"$i\">$i\n";
		}
	}

	print "<h4 id=\"archive\">Automation</h4>\n";
	print "<dl>\n";
	foreach my $k (sort keys $auto){
		my $item = $items->{skill}->[0]->{Automation}->[0]->{$k};
		print "<dt><b>$k</b></dt>\n";
		print "<dd>\n";
		for ($i=1;$i<6;$i++){
			if($item == $i){
				print "<input type=\"radio\" name=\"$k\" value=\"$i\" checked>$i\n";
			}else{
				print "<input type=\"radio\" name=\"$k\" value=\"$i\">$i\n";
			}
		}
	}

	print "</dl>\n";
	print "<h4 id=\"archive\">Test</h4>\n";
	print "<dl>\n";
	foreach my $k (sort keys $test){
		my $item = $items->{skill}->[0]->{Test}->[0]->{$k};
		print "<dt><b>$k</b></dt>\n";
		print "<dd>\n";
		for ($i=1;$i<6;$i++){
			if($item == $i){
				print "<input type=\"radio\" name=\"$k\" value=\"$i\" checked>$i\n";
			}else{
				print "<input type=\"radio\" name=\"$k\" value=\"$i\">$i\n";
			}
		}
	}

	print "</dl>\n";
	print "<h4 id=\"archive\">Cloud</h4>\n";
	print "<dl>\n";
	foreach my $k (sort keys $cloud){
		my $item = $items->{skill}->[0]->{Cloud}->[0]->{$k};
		print "<dt><b>$k</b></dt>\n";
		print "<dd>\n";
		for ($i=1;$i<6;$i++){
			if($item == $i){
				print "<input type=\"radio\" name=\"$k\" value=\"$i\" checked>$i\n";
			}else{
				print "<input type=\"radio\" name=\"$k\" value=\"$i\">$i\n";
			}
		}
	}

	print <<HTML_2;
	</dl>

	<input type="submit" value="Registration">
	</form>
HTML_2
}


sub parse_json{

        my $filepath = shift;
        my $json_data;
        my $ref_hash;

        open(R,"<$filepath");
        $json_data = <R>;
        close(R);
        $ref_hash = JSON->new()->decode($json_data);

        return $ref_hash;
}
