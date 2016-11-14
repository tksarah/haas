#!/usr/bin/perl

require 'lib.pl';
use strict;

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

$this_month =~ s/(^\d$)/$year-0$1/;
if($bm eq "last"){
	my $last_month = $this_month - 1;
        $set_month = "$year-"."$last_month";
}else{
        $set_month = "$year-$this_month";
}


### OUTPUT HTML ###
header("$host");

# out logfile
dep_user_list($host,$dep_name,$set_month,$logfile);

print <<LINKS;
<p>
<hr>
<a href="./haas/department.cgi?dep_name=$dep_name">[ This Month for $dep_name ]</a>
<a href="./haas/department.cgi?bm=last&dep_name=$dep_name">[ Last Month for $dep_name ]</a>
<a href="./haas/manage.cgi">[ Manage Top ]</a>
<p>
LINKS

footer();

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
	my $zero=0;
	

	print "<h3>$dep_name 集計 （$month）</h3><br>\n";
	print "<table class=\"simple\">\n";
	print "<tr><th>ユーザ</th><th>ハンズオン合計回数</th><th>ハンズオン合計実行時間</th></tr>\n";

	# Create Hash from a department list
        open(R,"<./data/$name.list");
        while (<R>) {
		if( /,/ ){
       			$_ =~ s/\s+//g;
                	my $dep_id = (split/,/,$_)[0];
       			my $username = (split/,/,$_)[1];
			chomp($username);
			if($username eq ""){
				$dep{$dep_id} = "$dep_id";
			}else{
				$dep{$dep_id} = "$username";
			}
		}else{
			chomp($_);
			$dep{$_} = "$_";
		}
	}
	close(R);

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
			print "<tr><td><a href=\"http://$hostaddr/haas/users.cgi?user=$user\">$dep{$user}</a></td>";
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

