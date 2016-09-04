#!/usr/bin/perl

require 'lib.pl';
use strict;

# Get values
my $host = get_value('host');
my $datadir = get_value('udatadir');

my $low_cnt;
my $mid_cnt;
my $high_cnt;
my $t_high_cnt;
my $t_mid_cnt;
my $t_low_cnt;
my @deplist = dep_list();
my @files = `ls $datadir/*`;
my %hash;

### OUTPUT HTML ###
header("$host");

foreach my $ufile (@files) {
	my $items = parse_json($ufile);

	my $depname = $items->{skill}->[0]->{Depname};
	my $shift = $items->{skill}->[0]->{Shift};
	my $ansible = $items->{skill}->[0]->{Automation}->[0]->{Ansible};
	

	if($shift > 6){
		$hash{"$depname.high_cnt"}++;
	}elsif($shift =~ /4|5|6/){
		$hash{"$depname.mid_cnt"}++;
	}elsif($shift < 4){
		$hash{"$depname.low_cnt"}++;
	}
		
}

	print "<h3>Shift</h3>\n";
	print "<div onclick=\"obj=document.getElementById('dep').style; obj.display=(obj.display=='none')?'block':'none';\">\n";
	print "<a style=\"cursor:pointer;\"><h4 id=\"archive\">▼ 部毎 集計</h4><br></a>\n";
	print "</div>\n";
	print "<div id=\"dep\" style=\"display:none;clear:both;\">\n";
	print "<table class=\"simple\">\n";
	print "<tr><th>部署</th><th>レベル</th><th>カウント</th></tr>\n";
	foreach (@deplist){
		print "<tr><td>$_</td><td><b>コードが書ける</b></td><td id=\"r\"><b>$hash{\"$_.high_cnt\"}</b></td></tr>\n";
		$t_high_cnt += $hash{"$_.high_cnt"};
		print "<tr><td>$_</td><td>Shift を利用できる</td><td id=\"r\">$hash{\"$_.mid_cnt\"}</td></tr>\n";
		$t_mid_cnt += $hash{"$_.mid_cnt"};
		print "<tr><td>$_</td><td>Shift 未経験</td><td id=\"r\">$hash{\"$_.low_cnt\"}</td></tr>\n";
		$t_low_cnt += $hash{"$_.low_cnt"};
	}
	print "</table><p>\n";
	print "</div>\n";;

	print "<h4 id=\"archive\">レベル毎 集計</h4><br>\n";
	print "<table class=\"simple\">\n";
	print "<tr><th>レベル</th><th>合計カウント</th></tr>\n";
	print "<tr><td><b>コードが書ける</b></td><td id=\"r\"><b>$t_high_cnt</b></td></tr>\n";
	print "<tr><td>Shift を利用できる</td><td id=\"r\">$t_mid_cnt</td></tr>\n";
	print "<tr><td>Shift 未経験</td><td id=\"r\">$t_low_cnt</td></tr>\n";
	print "</table>\n";

        print "<p>\n";
        print "<hr>\n";
        print "<a href=\"./haas/top_skill.cgi\">[ Skill Top ]</a>\n";
        print "<a href=\"./haas/manage.cgi\">[ Manage Top ]</a>\n";

footer();

exit (0);
