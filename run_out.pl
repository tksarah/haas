#!/usr/bin/perl

require 'lib.pl';
use strict;

# Get Date
my $dt = DateTime->now(time_zone => 'Asia/Tokyo');
my $now_month = $dt->month;
my $year;
my $month;
my $name;
my @dep = &dep_list();
my %dep_hash;

# Set logfiles
my $logfile = "./data/haas.log";
my $datadir = "./data";
my $archivedir = "$datadir/archives/";

# From arg
if($ARGV[0] =~ /\d{2}/){
	$month = $ARGV[0];
}else{
	$month = "0$now_month";
}
if($ARGV[1] =~ /\d{4}/){
	$year = $ARGV[1];
}else{
	$year = $dt->year;
}

foreach $name (@dep){
	my $listfile = "$datadir/$name.list";
	my $ym = "$year-$month";
	if( -f "$archivedir/$year-$month-$name.log"){
		print "$year-$month-$name.log exists.\n";
	}else{
		print "$year-$month-$name ... ";
		# Create Hash from a department list
		%dep_hash = create_hash($listfile);

		foreach my $user ( sort keys %dep_hash ){
		        open(R,"<$logfile");
       		 	while (<R>) {

				# date hands-on has been started
                                my $date = (split/,/,$_)[2];
                                my $id = (split/,/,$_)[0];

				if( $date =~ /$ym/ && $id =~ /$user/ ){
					open(W,">>$datadir/archives/$year-$month-$name.log");
					print W "$_";
					close(W);
				}
			}
			close(R);
		}
		if( !-f "$archivedir/$year-$month-$name.log"){
			print "No count.\n";
		}else{
			print "Created.\n";
			system("cat $archivedir/$year-$month-$name.log >> $archivedir/$year-$month-ALL.log");
		}
	}

}

exit(0);
