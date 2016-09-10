#!/usr/bin/perl

require 'lib.pl';
use strict;
use feature ':5.10';

# Get values
my $host = get_value('host');
my $datadir = get_value('udatadir');

# From POST
my $form = CGI->new;
my $input_dep = $form->param('dep');

my $depfile = "./data/$input_dep.list";
my @files = `ls $datadir/*`;
my @shifts=(0,0,0,0,0,0,0,0,0);
my $total=0;
my $items;

# Initialize question
my @shift_level = (
        "インフラをコード化するツール/ソフトを聞いたことがない。",
        "インフラをコード化するツール/ソフトを1つでも聞いたことがある、名前は知ってる。",
        "インフラをコード化するツール/ソフトの資料やガイドを見ことがある or 社内・社外研修・勉強会を受けたことがある。",
        "インフラをコード化するツール/ソフトを1度でも利用したことがある。（検証や、個別利用等可）",
        "Shift 用のコードを案件へ利用したことがある。（部分的利用も可）",
        "Shift 用のコードの中で、パラメータを修正して利用できる。",
        "Shift 用のコードを自ら修正・カスタマイズできる or したことがある。",
        "Shift 用のコード or 個別に Ansible や Serverspec などインフラをコード化できる。",
        "Shift のデベロッパー or メンテナーである。"
);

foreach my $ufile (@files) {
	$items = parse_json($ufile);

	my $depname = $items->{skill}->[0]->{Depname};
	my $shift = $items->{skill}->[0]->{Shift};

	if ( $depname eq "$input_dep" ) {
	  given ($shift) {
            when ("1") { $shifts[0]++ }
            when ("2") { $shifts[1]++ }
            when ("3") { $shifts[2]++ }
            when ("4") { $shifts[3]++ }
            when ("5") { $shifts[4]++ }
            when ("6") { $shifts[5]++ }
            when ("7") { $shifts[6]++ }
            when ("8") { $shifts[7]++ }
            when ("9") { $shifts[8]++ }
          }
	$total++ if($ufile !~ /000000/);
	}
}

### OUTPUT HTML ###
header("$host");

print "<h3>$input_dep（$total）</h3>\n";
print "<p>\n";
print "<table class=\"simple\">\n";
print "<tr><th>レベル</th><th>カウント</th></tr>\n";
for (my $i=0;$i<9;$i++){
	my $level=$i+1;
	print "<tr><td id=\"naka\">$level</td><td id=\"r\"><b>$shifts[$i]</b> ";
	for (my $x=1;$x<=$shifts[$i];$x++) { print "*"; }
	print "</td></tr>\n";
}
print "</table><p>\n";

print "<div id=\"desc\"><b>レベル</b>\n";
print "<div id=\"comment\">\n";
for (my $i=1;$i<10;$i++){
	print "$i.　$shift_level[$i-1]<br>\n";
}
print "</div>\n";
print "</div>\n";
print "<p>\n";

print "オプションの集計はこちらから。\n";
my $auto = $items->{skill}->[0]->{Automation}->[0];
my $test = $items->{skill}->[0]->{Test}->[0];
my $cloud = $items->{skill}->[0]->{Cloud}->[0];

print "<div onclick=\"obj=document.getElementById('auto').style; obj.display=(obj.display=='none')?'block':'none';\">\n";
print "<a style=\"cursor:pointer;\"><h3>▼ Automation</h3></a>\n";
print "</div><p>\n";
print "<div id=\"auto\" style=\"display:none;clear:both;\">\n";
output_option_calc($auto,$input_dep,$datadir);
print "</div><p>\n";

print "<div onclick=\"obj=document.getElementById('test').style; obj.display=(obj.display=='none')?'block':'none';\">\n";
print "<a style=\"cursor:pointer;\"><h3>▼ Test</h3></a>\n";
print "</div><p>\n";
print "<div id=\"test\" style=\"display:none;clear:both;\">\n";
output_option_calc($test,$input_dep,$datadir);
print "</div><p>\n";

print "<div onclick=\"obj=document.getElementById('cloud').style; obj.display=(obj.display=='none')?'block':'none';\">\n";
print "<a style=\"cursor:pointer;\"><h3>▼ Cloud</h3></a>\n";
print "</div><p>\n";
print "<div id=\"cloud\" style=\"display:none;clear:both;\">\n";
output_option_calc($cloud,$input_dep,$datadir);
print "</div><p>\n";

print "<p>\n";
print "<hr>\n";
print "<a href=\"./haas/top_skill.cgi\">[ Skill Top ]</a>\n";
print "<a href=\"./haas/manage.cgi\">[ Manage Top ]</a>\n";
footer();

exit (0);

