#!/usr/bin/perl
use strict ;
use BerkeleyDB ;
use vars qw( %h $k $v ) ;

my $filename = "db.dat" ;
my @list;

# Initialize file
unlink $filename ;
tie %h, "BerkeleyDB::Hash",
	-Filename => $filename,
	-Flags    => DB_CREATE
    or die "Cannot open file $filename: $! $BerkeleyDB::Error\n" ;

# Add a few key/value pairs to the file
#$h{"apple"} = "red" ;
#$h{"orange"} = "orange" ;
#$h{"banana"} = "yellow" ;
#$h{"tomato"} = "red" ;

my $name = "user1";
my $string = "8092,3003,3004";
$h{"$name"} = $string;

# Check for existence of a key
#print "Banana is $h{banana}\n" if $h{"banana"} ;
#print "Apple is $h{apple}\n\n" if $h{"apple"} ;

# Delete a key/value pair.
#delete $h{"apple"} ;

# print the contents of the file
while (($k, $v) = each %h) {
	@list = split(/,/,$v);
	print "$k -> \"port: '$list[0]',htty: '$list[1]',ttty: '$list[2]'\"\n" 
	}
untie %h ;
