#!/usr/bin/perl

require 'lib.pl';
use strict;

# Get values
my $host = get_value('host');
my $datadir = get_value('udatadir');

my $total=0;
my $low_cnt;
my $mid_cnt;
my $high_cnt;
my $t_high_cnt;
my $t_mid_cnt;
my $t_low_cnt;
my @deplist = dep_list();
my @files = `ls $datadir/*`;
my $items;
my %hash;

# Initialize question
my @shift_level = (
        "インフラをコード化するツール/ソフトを聞いたことがない。",
        "インフラをコード化するツール/ソフトを1つでも聞いたことがある、名前は知ってる。",
        "インフラをコード化するツール/ソフトの資料やガイドを見ことがある or 社内・社外研修・勉強会を受けたことがある。",
        "インフラをコード化するツール/ソフトを1度でも利用したことがある。（検証や、個別利用等可）",
        "SHIFT 用のコードを案件へ利用したことがある。（部分的利用も可）",
        "SHIFT 用のコードの中で、パラメータを修正して利用できる。",
        "SHIFT 用のコードを自ら修正・カスタマイズできる or したことがある。",
        "SHIFT 用のコード or 個別に Ansible や Serverspec などインフラをコード化できる。",
        "SHIFT のデベロッパー or メンテナーである。"
);

foreach my $ufile (@files) {
	$items = parse_json($ufile);

	my $depname = $items->{skill}->[0]->{Depname};
	my $shift = $items->{skill}->[0]->{Shift};

	if($shift > 6){
		$hash{"$depname.high_cnt"}++;
	}elsif($shift =~ /4|5|6/){
		$hash{"$depname.mid_cnt"}++;
	}elsif($shift < 4){
		$hash{"$depname.low_cnt"}++;
	}
		
	$total++ if($ufile !~ /000000/);
}

### OUTPUT HTML ###
header("$host");

print "<h3>SHIFT</h3>\n";
print "<h4 id=\"archive\">部毎 集計</h4><br>\n";
print "<table class=\"simple\">\n";
print "<tr><th>部署</th><th>レベル</th><th>カウント</th></tr>\n";
foreach (@deplist){
	my $dep_t_cnt = $hash{"$_.high_cnt"} + $hash{"$_.mid_cnt"} + $hash{"$_.low_cnt"};
	print "<tr><td rowspan=\"3\"><a href=\"./haas/result_dep_skill.cgi?dep=$_\">▼ $_</a>（$dep_t_cnt） </td>\n";
	print "<td><b>インフラをコード化できる</b></td><td id=\"r\"><b>$hash{\"$_.high_cnt\"}</b></td></tr>\n";
	$t_high_cnt += $hash{"$_.high_cnt"};
	print "<tr><td>インフラコードを利用できる</td><td id=\"r\">$hash{\"$_.mid_cnt\"}</td></tr>\n";
	$t_mid_cnt += $hash{"$_.mid_cnt"};
	print "<tr><td>インフラコード技術未経験</td><td id=\"r\">$hash{\"$_.low_cnt\"}</td></tr>\n";
	$t_low_cnt += $hash{"$_.low_cnt"};
}
print "</table><p>\n";

print "<h4 id=\"archive\">レベル毎 集計（Total $total）</h4><br>\n";
print "<table class=\"simple\">\n";
print "<tr><th>熟練度</th><th>レベル</th><th>合計カウント</th></tr>\n";
print "<tr><td><b>インフラをコード化できる</b></td><td id=\"naka\"> <b>7～9</b> </td></b></td><td id=\"r\"><b>$t_high_cnt</b></td></tr>\n";
print "<tr><td>インフラコードを利用できる</td><td id=\"naka\"> 4～6 </td><td id=\"r\">$t_mid_cnt</td></tr>\n";
print "<tr><td>インフラコード技術未経験</td><td id=\"naka\"> 1～3 </td><td id=\"r\">$t_low_cnt</td></tr>\n";
print "</table>\n";
print "<p>\n";
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
output_option_calc($auto,"",$datadir);
print "</div><p>\n";

print "<div onclick=\"obj=document.getElementById('test').style; obj.display=(obj.display=='none')?'block':'none';\">\n";
print "<a style=\"cursor:pointer;\"><h3>▼ Test</h3></a>\n";
print "</div><p>\n";
print "<div id=\"test\" style=\"display:none;clear:both;\">\n";
output_option_calc($test,"",$datadir);
print "</div><p>\n";

print "<div onclick=\"obj=document.getElementById('cloud').style; obj.display=(obj.display=='none')?'block':'none';\">\n";
print "<a style=\"cursor:pointer;\"><h3>▼ Cloud</h3></a>\n";
print "</div><p>\n";
print "<div id=\"cloud\" style=\"display:none;clear:both;\">\n";
output_option_calc($cloud,"",$datadir);
print "</div><p>\n";


print "<p>\n";
print "<hr>\n";
print "<a href=\"./haas/top_skill.cgi\">[ Skill Top ]</a>\n";
print "<a href=\"./haas/manage.cgi\">[ Manage Top ]</a>\n";
footer();

exit (0);
