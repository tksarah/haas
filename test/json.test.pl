#!/usr/bin/perl

use JSON;
use strict;
use JSON;

#my $json_data = '{"skill":[{"Ansible":"5","Serverspec":"3"}],"status":[{"School":"unko","Area":"koiwa"}]}';

my $filepath = shift;
my $items = parse_json("$filepath");

my $cate = $items->{skill}->[0];
my $out3 = $items->{skill}->[0]->{Ansible};
my $out4 = $items->{skill}->[0]->{Serverspec};

my $k;
#my $v;
foreach my $k (keys $cate){
#foreach my $k (sort keys $cate){
	print "$k\n";
}
#while (($k, $v) = each $cate) {
#	print "$k\n";
#}

print "$out3 \n";
print "$out4 \n";

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
