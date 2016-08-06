#!/usr/bin/perl

require './lib.pl';
use strict;
use CGI;
use DateTime;

# From POST
my $form = CGI->new;
my $bm = $form->param('bm');
my $dep_name = $form->param('dep_name');

# Get values
my $host = get_value('host');
my $logfile = get_value('logfile');

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


### OUTPUT HTML ###
header("$host");

# out logfile
dep_user_list($host,$dep_name,$set_month,$logfile);

print <<FOOTER;
<p>
<a href="./haas/"  target="_blank">[ Top ]</a>
<a href="./haas/department.cgi"  target="_blank">[ This Month for $dep_name ]</a>
<a href="./haas/department.cgi?bm=1&dep_name=$dep_name"  target="_blank">[ Last Month for $dep_name ]</a>
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
        my $month = shift;
        my $logfile = shift;
	my %dep;
	my %counts;
	

	print "<h3>$dep_name 総合集計 （$month）</h3><br>\n";
	print "<table class=\"simple\">\n";
	print "<tr><th>ユーザ</th><th>ハンズオン合計回数</th><th>ハンズオン合計実行時間</th></tr>\n";

	# Create Hash from a department list
        open(R,"<./data/$name.list");
        while (<R>) {
                my $dep_id = (split/,/,$_)[0];
                my $username = (split/,/,$_)[1];
		chomp($username);
		
		$dep{$dep_id} = "$username";
	}
	close(R);
	my @userlist = keys %dep;

	foreach my $user ( @userlist ){
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
		print "<tr><td><a href=\"http://$hostaddr/haas/users.cgi?user=$user\">$dep{$user}</a></td><td id=\"r\">$total</td><td id=\"r\">$total_h</td><tr>\n";
	}

	print "<table>\n";
	print "<p>\n";
}

