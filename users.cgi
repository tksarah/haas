#!/usr/bin/perl

require './lib.pl';
use strict;
use CGI;
use DateTime;

# From POST
my $form = CGI->new;
my $bm = $form->param('bm');
my $user = $form->param('user');


# Get values
my $host = get_value('host');
my $back_url = $ENV{'HTTP_REFERER'};
if(!$back_url){
	$back_url = "http://$host/haas/";
}
my $logfile = get_value('logfile');

# Get Date
my $dt = DateTime->now(time_zone => 'Asia/Tokyo');
my $year = $dt->year;
my $this_month = $dt->month;
my $set_month;
my $last_month;

if($bm eq "last"){
	$last_month = $this_month -1;
	$set_month = "$year-0$last_month";
}else{
	$set_month = "$year-0$this_month";
}


### OUTPUT HTML ###
header("$host");

user_stats($host,$user,$set_month,$logfile);

print <<FOOTER;
<p>
<a href="./haas/users.cgi?user=$user">[ This Month for $user ]</a>
<a href="./haas/users.cgi?bm=last&user=$user">[ Last Month for $user ]</a>
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
sub user_stats{

        my $hostaddr = shift;
        my $name = shift;
        my $month = shift;
        my $logfile = shift;

        my $total=0;
	my %counts;
	my $emp_m = 0;
	
        open(R,"<$logfile");
        while (<R>) {

                my $id = (split/,/,$_)[0];
                my $type = (split/,/,$_)[1];
		# date hands-on has been started
                my $date = (split/,/,$_)[2];
                my $status = (split/,/,$_)[7];
                my $time = (split/,/,$_)[9];

		if( $date =~ /$month/ && $id =~ /$name/ ){

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

	# ajust for hours
	my $emp_h = sprintf("%.1f", ($counts{'stime'} + $counts{'ftime'})/60); 

# OUTPUT
print <<STATS;

<h3>$user さんの受講状況（$month）</h3><br>
<table class="simple">
<tr><th>実行時間（H）</th><td id="r"><font size="5pt"><b>$emp_h</b></font></td></tr>
<table>
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
