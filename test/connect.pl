#!/usr/bin/perl

use IO::Socket;

my $ip=$ARGV[0];
my $port=$ARGV[1];

        print "Setting:$ip:$port\n\n";

        # Socket & Connect
        $remote = IO::Socket::INET->new( Proto => "tcp",
        PeerAddr => "$ip",
        PeerPort => "$port"
        );

        unless($remote){
                print "Failed\n";
                print "$remote";
                exit(1);
        }
        $remote->autoflush(1);

        #print $remote "GET /wordpress/wp-admin/install.php \n\n";
        print $remote "HEAD /wordpress/wp-admin/install.php \n\n";

        $f=<$remote>;
        close $remote;

        print "$f\n";

        #if($f =~ /200\s{1}OK/){
        if($f =~ /DOCTYPE\sHTML/){
                print "HTTP OK\n";
                exit (0)

        }else{
                print "HTTP NG\n";
                exit (1)
        }
