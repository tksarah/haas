#!/usr/bin/perl

require 'lib.pl';
use strict;

# From POST
my $form = CGI->new;
my $dep_name = $form->param('dep_name');
my $year = $form->param('year');
my $month = $form->param('month');

# Get values
my $host = get_value('host');
my $datadir = "./data";
my $archivedir = "$datadir/archives/";
my $listfile = "$datadir/$dep_name.list";
my $logfile = "$archivedir/$year-$month-$dep_name.log";
my $all_logfile = "$archivedir/$year-$month-ALL.log";

### OUTPUT HTML ###
header("$host");

print "<font color=\"red\">IDを間違えて実施している場合はカウントされません。</font>\n";

if($dep_name eq "all"){
	statistics_archive("$year-$month",$all_logfile);
}elsif($dep_name ne "" & $year ne "" & $month ne ""){
	dep_user_list_archive($host,$dep_name,$year,$month,$logfile,$listfile);
}else{
	select_func_archive();
}

print <<LINKS;
<p>
<hr>
<a href="./haas/archives.cgi">[ Archvies Top ]</a>
<a href="./haas/manage.cgi">[ Manage Top ]</a>
<p>
LINKS

footer();

exit (0);

sub dep_user_list_archive{

	my $hostaddr = shift;
        my $name = shift;
        my $year = shift;
        my $month = shift;
        my $logfile = shift;
        my $listfile = shift;
	my %dep;
	my %counts;
	my $zero=0;
	

	print "<h3>$dep_name 集計 （$year-$month）</h3><br>\n";
	print "<table class=\"simple\">\n";
	print "<tr><th>ユーザ</th><th>ハンズオン合計回数</th><th>ハンズオン合計実行時間</th></tr>\n";

	# Create Hash from a department list
	%dep = create_hash($listfile);

	foreach my $user ( sort keys %dep ){
        	my $total=0;
	        my $total_m=0;
		my $total_h=0;
	        open(R,"<$logfile");
        	while (<R>) {

			my $id = (split/,/,$_)[0];
			my $type = (split/,/,$_)[1];
			# date hands-on has been started
			my $date = (split/,/,$_)[2];
			my $status = (split/,/,$_)[7];
			my $time = (split/,/,$_)[9];

			if( $date =~ /$month/ && $id =~ /$user/ ){
				$total_m += $time;
				$total++;
			}
		}
		close(R);
		# ajust for hours
		$total_h = sprintf("%.1f", $total_m/60); 

		# OUTPUT
		if($total != 0){
			print "<tr><td>$dep{$user}</td>";
			print "<td id=\"r\">$total</td>";
			print "<td id=\"r\">$total_h</td><tr>\n";
		}
		$zero += $total;
	}

	if($zero == 0){
		print "<tr><td colspan=\"3\">該当なし</td></tr>\n";
	}
	print "<table>\n";
	print "<br>\n";
	print "* <font color=\"red\">0回</font>の人は除く\n";
	print "<p>\n";
}


sub select_func_archive{
	my @select_list = &dep_list();

	print <<HTML1;

	<h3>アーカイブ選択</h3><p>
        <form action="./haas/archives.cgi" method="post">
	<dl>
	<dt><b>年度</b></dt>
	  <dd><input type="radio" name="year" value="2016" checked>2016</dd>
	<dt><b>月</b></dt>
	  <dd><input type="radio" name="month" value="07" checked>7</dd>
	  <dd><input type="radio" name="month" value="08" checked>8</dd>
	<dt><b>部署</b></dt>
	  <dd><input type="radio" name="dep_name" value="all" checked>ALL
HTML1

	foreach (@select_list){
	  print "<input type=\"radio\" name=\"dep_name\" value=\"$_\">$_\n";
	}

	print <<HTML_2;
	  </dd>
	</dl>

	<input type="submit" value="Check">
	
	</form>

HTML_2
}

sub statistics_archive{

        my $month = shift;
        my $logfile = shift;
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

                my $id = (split/,/,$_)[0];
                my $type = (split/,/,$_)[1];
                # date hands-on has been started
                my $date = (split/,/,$_)[2];
                my $status = (split/,/,$_)[7];
                my $time = (split/,/,$_)[9];

                if( $date =~ /$month/ ){
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
                        }elsif($type eq "ansible-2" && $status == 1){
                                $counts{"ansible-2-s"}++;
                        }elsif($type eq "ansible-2" && $status == 0){
                                $counts{"ansible-2-f"}++;
                        }elsif($type eq "serverspec-1" && $status == 1){
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

	<h3>$month</h3>
	<h4 id="archive">総合</h4>
	<br>
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
	</table>
	<p>

	<h4 id="archive">詳細</h4>
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

	<h4 id="archive">ハンズオン科目別</h4>
	<br>
	<table class="simple">
	<tr><th>項目</th><th>値</th></tr>
	<tr><td>Ansible 初級ハンズオン数（完了）</td><td id="r"><font color="blue">$counts{'ansible-1-s'}</font></td></tr>
	<tr><td>Ansible 中級ハンズオン数（完了）</td><td id="r"><font color="blue">$counts{'ansible-2-s'}</font></td></tr>
	<tr><td>Serverspec 初級ハンズオン数（完了）</td><td id="r"><font color="blue">$counts{'serverspec-1-s'}</font></td></tr>
	<tr><td>Ansible 初級ハンズオン数（未完了）</td><td id="r"><font color="red">$counts{'ansible-1-f'}</font></td></tr>
	<tr><td>Ansible 中級ハンズオン数（未完了）</td><td id="r"><font color="red">$counts{'ansible-2-f'}</font></td></tr>
	<tr><td>Serverspec 初級ハンズオン数（未完了）</td><td id="r"><font color="red">$counts{'serverspec-1-f'}</font></td></tr>
	</table>
	<p>
STATS

}
