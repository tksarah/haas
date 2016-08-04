#!/usr/bin/perl

require './lib.pl';
use strict;
use CGI;
use DateTime;
use BerkeleyDB;
use vars qw( %h $k $v );

# From POST
my $form = CGI->new;
my $bm = $form->param('bm');

# Get values
my $host = get_value('host');
my $dbfilename = get_value('dbfilename');
my $max_emp = get_value('max_emp');

# Get Date
my $dt = DateTime->now(time_zone => 'Asia/Tokyo');
my $year = $dt->year;
my $this_month = $dt->month;
my $set_month;
my $last_month;

if($bm == 1){
	$last_month = $this_month -1;
	$set_month = "$year-0$last_month";
}else{
	$set_month = "$year-0$this_month";
}


# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $dbfilename,
        -Flags    => DB_CREATE
    or die "Cannot open file $dbfilename: $! $BerkeleyDB::Error\n";

### OUTPUT HTML ###
header("$host");

# Registration List
print "<h3>利用状況</h3><br>";

if(keys %h == 0){
        print "利用者がいません。<p>\n";
}elsif(keys %h == $max_emp){
        print "現在<font color=\"red\">フル稼働</font>です。1時間以上お待ち下さい。\n";
        print "<table>\n";
	print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th><th>Destroy</th></tr>\n";

        while (($k, $v) = each %h) {
                my @list = split(/,/,$v);
                print "<tr>";
                print "<td><a href=\"./haas/myhandson.cgi?name=$k\">$k</a></td>";
                print "<td>$list[0]</td>";
                print "<td>$list[1]</td>";
                print "<td>$list[2]</td>";
		print "<td><form action=\"./haas/delete.cgi\" method=\"post\"><input type=\"hidden\" name=\"name\" value=\"$k\"><input type=\"submit\" value=\"Destroy\"></form></td>";
                print "</tr>\n";
                }
        print "</table>\n";
}else{
        print "<table>\n";
	print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th><th>Destroy</th></tr>\n";

        while (($k, $v) = each %h) {
                my @list = split(/,/,$v);
                print "<tr>";
                print "<td><a href=\"./haas/myhandson.cgi?name=$k\">$k</a></td>";
                print "<td>$list[0]</td>";
                print "<td>$list[1]</td>";
                print "<td>$list[2]</td>";
		print "<td><form action=\"./haas/delete.cgi\" method=\"post\"><input type=\"hidden\" name=\"name\" value=\"$k\"><input type=\"submit\" value=\"Destroy\"></form></td>";
                print "</tr>\n";
                }
        print "</table>\n";
        print "</p>\n";
}

untie %h;


# out logfile
statistics($set_month);

print <<FOOTER;
<p>
<a href="./haas/"  target="_blank">[ Top ]</a>
<a href="./haas/log_check.cgi"  target="_blank">[ Log & Check ]</a>
<a href="./haas/manage.cgi"  target="_blank">[ This Month ]</a>
<a href="./haas/manage.cgi?bm=1"  target="_blank">[ Last Month ]</a>
<a href="http://192.168.175.198:8080/#/"  target="_blank">[ Notebook ]</a>
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

### Log Page
## Statistics for month
sub statistics{

        my $month = shift;
        my $logfile = get_value('logfile');
        my $total=0;
        my $rec;
        my $ucnt;
        my $urec;
        my @ids;
        my @types;
	my @id_type;
	my %counts;
	my %over20_counts = (emp => 0, time => 0);
	my %under20_counts = (emp => 0, time => 0);;
	my $emp_m = 0;
	my $emp_m_o20 = 0;
	my $emp_m_u20 = 0;
	
        open(R,"<$logfile");
        while (<R>) {
	if( /$month/ ){

                my $id = (split/,/,$_)[0];
                my $type = (split/,/,$_)[1];
                my $status = (split/,/,$_)[7];
                my $time = (split/,/,$_)[9];

                $rec = "$id:$type";
                push(@ids,$id);
                push(@id_type,$rec);

		if($time >= 20){
			$over20_counts{"emp"}++;
			$over20_counts{"time"} = $over20_counts{"time"} + $time;
		}else{
			$under20_counts{"emp"}++;
			$under20_counts{"time"} = $under20_counts{"time"} + $time;
		}

		if($status == 1){
			$counts{"success"}++;;
			$counts{"stime"} = $counts{"stime"} + $time;
		}else{
			$counts{"ftime"} = $counts{"ftime"} + $time;
		}
		if($type eq "ansible-1" && $status == 1){
			$counts{"ansible-1-s"}++;
		}elsif($type eq "ansible-1" && $status == 0){
			$counts{"ansible-1-f"}++;
		}
		if($type eq "ansible-2" && $status == 1){
			$counts{"ansible-2-s"}++;
		}elsif($type eq "ansible-2" && $status == 0){
			$counts{"ansible-2-f"}++;
		}
		if($type eq "serverspec-1" && $status == 1){
			$counts{"serverspec-1-s"}++;
		}elsif($type eq "serverspec-1" && $status == 0){
			$counts{"serverspec-1-f"}++;
		}
		$total++;
        }
	}
        close(R);

        $ucnt = uniq_func(@ids);
        $urec = uniq_func(@id_type);

	# /employee
	# $round=sprintf("%.2f",$val); 3.14
	if($ucnt != 0){
		$emp_m = sprintf("%.1f",($counts{'stime'} + $counts{'ftime'})/$ucnt);
	}
	if($over20_counts{'emp'} != 0){
		$emp_m_o20 = sprintf("%.1f",$over20_counts{'time'}/$over20_counts{'emp'});
	}
	
	if($under20_counts{'emp'} != 0){
		$emp_m_u20 = sprintf("%.1f",$under20_counts{'time'}/$under20_counts{'emp'});
	}

	# ajust for hours
	my $emp_h = sprintf("%.1f", ($counts{'stime'} + $counts{'ftime'})/60); 

# OUTPUT
print <<STATS;

<h3>総合集計 （$month）</h3><br>
試験運用：2016/7/19～2016/7/31 <br>
サービス開始日：2016/8/1～
<table class="simple">
<tr><th>項目</th><th>値</th></tr>
<tr><td>トータル施策適用工数（時）</td><td id="r"><font size="5pt"><b>$emp_h</b></font></td></tr>
<tr><td>トータルハンズオン実施数</td><td id="r">$total</td></tr>
<tr><td>トータルハンズオン完了数</td><td id="r">$counts{'success'}</td></tr>
<tr><td>トータルハンズオン完了時間（分）</td><td id="r"><font color="blue">$counts{'stime'}</font></td></tr>
<tr><td>トータルハンズオン未完了時間（分）</td><td id="r"><font color="red">$counts{'ftime'}</font></td></tr>
<tr><td>ユニークユーザ数</td><td id="r">$ucnt</td></tr>
<tr><td>ユニークハンズオン数（ID＋ハンズオンタイプ）</td><td id="r">$urec</td></tr>
<tr><td>ハンズオン時間/人（分）</td><td id="r">$emp_m</td></tr>
<table>
<p>

<h3>詳細集計</h3>
<p>
各ハンズオンはインチキをしない限り、数分では完了できませんのでそのような実施は除外とするための情報
<p>
<table class="simple">
<tr><th>項目</th><th>サブ項目</th><th>値</th></tr>
<tr><td rowspan="2">20分以上で終了</td><td>ハンズオン数</td><td id="r">$over20_counts{'emp'}</td></tr>
<tr></td><td>時間/ハンズオン（分）</td><td id="r">$emp_m_o20</td></tr>
<tr><td rowspan="2">20分以下で終了</td><td>ハンズオン数</td><td id="r">$under20_counts{'emp'}</td></tr>
<tr></td><td>時間/ハンズオン（分）</td><td id="r">$emp_m_u20</td></tr>
</table>
<p>

<h3>ハンズオン科目別</h3><br>
<table class="simple">
<tr><th>項目</th><th>値</th></tr>
<tr><td>Ansible 初級ハンズオン数（完了）</td><td id="r"><font color="blue">$counts{'ansible-1-s'}</font></td></tr>
<tr><td>Ansible 中級ハンズオン数（完了）</td><td id="r"><font color="blue">$counts{'ansible-2-s'}</font></td></tr>
<tr><td>Serverspec 初級ハンズオン数（完了）</td><td id="r"><font color="blue">$counts{'serverspec-1-s'}</font></td></tr>
<tr><td>Ansible 初級ハンズオン数（未完了）</td><td id="r"><font color="red">$counts{'ansible-1-f'}</font></td></tr>
<tr><td>Ansible 中級ハンズオン数（未完了）</td><td id="r"><font color="red">$counts{'ansible-2-f'}</font></td></tr>
<tr><td>Serverspec 初級ハンズオン数（未完了）</td><td id="r"><font color="red">$counts{'serverspec-1-f'}</font></td></tr>
</table>
STATS

}

sub uniq_func{
        my @src = @_;
        my %hash;

        @hash{@src} = ();
        return keys %hash;
}
