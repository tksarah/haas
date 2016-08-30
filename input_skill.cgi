#!/usr/bin/perl

require './lib.pl';
use strict;
use CGI;
use JSON;

# From POST
my $form = CGI->new;
my $user = $form->param('name');

# Get values
my $host = get_value('host');
my $datadir = "../testdata";
my $userdata = "$datadir/$user";

my $back_url = $ENV{'HTTP_REFERER'};
if(!$back_url){
        $back_url = "http://$host/haas/";
}

# Check name
if($user eq "000000" || $user eq "" ||  $user !~ /^[\w]+$/ ){
        error_page(1,$back_url);
        exit(0);
}

# Format Initialize
$userdata = "$datadir/000000" if (! -f $userdata);

### OUTPUT HTML ###
header("$host");

my $items = parse_json($userdata);
input_func($user,$items);

footer();

exit (0);

sub input_func{

	my $userid = shift;
	my $items = shift;
        my $shift = $items->{skill}->[0]->{Shift};
	my $auto = $items->{skill}->[0]->{Automation}->[0];
	my $test = $items->{skill}->[0]->{Test}->[0];
	my $cloud = $items->{skill}->[0]->{Cloud}->[0];
	my $i;

	print <<HTML_1;

	<h3>スキルレベルを登録 （$userid）</h3><p>
        <form action="./haas/reg_skill.cgi" method="post">
	<input type="hidden" name="name" value="$userid">
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
