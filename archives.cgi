#!/usr/bin/perl

require './lib.pl';
use strict;
use CGI;
use DateTime;

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

### OUTPUT HTML ###
header("$host");

# out logfile
if($dep_name ne "" & $year ne "" & $month ne ""){
	dep_user_list($host,$dep_name,$year,$month,$logfile,$listfile);
}else{
	select_func();
}

print <<FOOTER;
<p>
<a href="./haas/archives.cgi">[ Archvies Top ]</a>
<a href="./haas/manage.cgi">[ Manage Top ]</a>
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
sub dep_user_list{

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
	%dep = &create_hash($listfile);

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


sub select_func{
print <<HTML;

	<h3>アーカイブ選択</h3><p>
        <form action="./haas/archives.cgi" method="post">
	<dl>
	<dt><b>年度</b></dt>
	  <dd><input type="radio" name="year" value="2016" checked>2016</dd>
	<dt><b>月</b></dt>
	  <dd><input type="radio" name="month" value="07" checked>07</dd>
	<dt><b>部署</b></dt>
	  <dd>
	      <input type="radio" name="dep_name" value="A">A
	      <input type="radio" name="dep_name" value="B">B
	      <input type="radio" name="dep_name" value="C">C
	  </dd>
	</dl>

	<input type="submit" value="Check">
	
	</form>

HTML
}

sub create_hash{
        my $file = shift;
        my $dep_id;
        my $username;
        my %hash;

        open(R,"<$file");
        while (<R>) {
                if( /,/ ){
                        $_ =~ s/\s+//g;
                        $dep_id = (split/,/,$_)[0];
                        $username = (split/,/,$_)[1];
                        chomp($username);
                        if($username eq ""){
                                $hash{$dep_id} = "$dep_id";
                        }else{
                                $hash{$dep_id} = "$username";
                        }
                }else{
                        chomp($_);
                        $hash{$_} = "$_";
                }
        }
        return %hash;
}
