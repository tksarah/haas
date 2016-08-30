#!/usr/bin/perl

use JSON;
use strict;
use JSON;
use Data::Dumper;

my $filepath = shift;
my $items = parse_json("$filepath");

my $auto = $items->{skill}->[0]->{Automation}->[0];
my $str0 = $items->{skill}->[0]->{Shift};
my $str1 = $items->{skill}->[0]->{Automation}->[0]->{Ansible};
my $str2 = $items->{skill}->[0]->{Test}->[0]->{Serverspec};
my $str3 = $items->{skill}->[0]->{Cloud}->[0]->{AWS};

my $dump = Dumper($items);
print "$dump";

print "Shift .. $str0 \n";
print "Ansible .. $str1 \n";
print "Serverspec .. $str2 \n";
print "AWS .. $str3 \n";

foreach my $k (sort keys $auto){
	print "$k\n";
}
#while (($k, $v) = each $cate) {
#	print "$k\n";
#}


exit(0);




sub parse_json{

	my $filepath = shift;
	my $json_data;
	my $ref_hash;

	open(R,"<$filepath");
	$json_data = <R>;
	close(R);
	$ref_hash = JSON->new()->decode($json_data);

	return $ref_hash;
}
