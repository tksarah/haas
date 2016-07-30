#!/usr/bin/perl

require './lib.pl';
# yum install perl-DateTime
# yum install perl-DateTime-Format-Strptime
#use DateTime;
#use DateTime::Format::Strptime;
use strict ;
use CGI;
use BerkeleyDB;
use vars qw( %h $k $v );

# Get values
my $host = get_value('host');
my $dbfilename = get_value('dbfilename');
my $max_emp = get_value('max_emp');

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $dbfilename,
        -Flags    => DB_CREATE
    or die "Cannot open file $dbfilename: $! $BerkeleyDB::Error\n";

### OUTPUT HTML ###
header("$host");

print "<a href=\"http://192.168.175.198:8080/#/\" target=\"_blank\">Notebook</a><br>";

# Registration List
print "<h3>利用状況</h3><br>";

if(keys %h == 0){
        print "利用者がいません。<p>\n";
}elsif(keys %h == $max_emp){
        print "現在<font color=\"red\">フル稼働</font>です。1時間以上お待ち下さい。\n";
        print "<table>\n";
	print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th><th>Destroy</th></tr>\n";

        while (($k, $v) = each %h) {
                my @list = split(/,/,$v);
                print "<tr>";
                print "<td><a href=\"./haas/myhandson.cgi?name=$k\">$k</a></td>";
                print "<td>$list[0]</td>";
                print "<td>$list[1]</td>";
                print "<td>$list[2]</td>";
		print "<td><form action=\"./haas/delete.cgi\" method=\"post\"><input type=\"hidden\" name=\"name\" value=\"$k\"><input type=\"submit\" value=\"Destroy\"></form></td>";
                print "</tr>\n";
                }
        print "</table>\n";
}else{
        print "<table>\n";
	print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th><th>Destroy</th></tr>\n";

        while (($k, $v) = each %h) {
                my @list = split(/,/,$v);
                print "<tr>";
                print "<td><a href=\"./haas/myhandson.cgi?name=$k\">$k</a></td>";
                print "<td>$list[0]</td>";
                print "<td>$list[1]</td>";
                print "<td>$list[2]</td>";
		print "<td><form action=\"./haas/delete.cgi\" method=\"post\"><input type=\"hidden\" name=\"name\" value=\"$k\"><input type=\"submit\" value=\"Destroy\"></form></td>";
                print "</tr>\n";
                }
        print "</table>\n";
        print "</p>\n";
}

untie %h;

# out logfile
log_page();

# out at
my $atl_out = `sudo at -l`;
my $atq_out = `sudo atq`;
print "<h3>at list</h3>";
print "<h4>at -l</h4>";
print "<pre style=\"padding-left: 20px\">$atl_out</pre>";
print "<h4>atq</h4>";
print "<pre style=\"padding-left: 20px\">$atq_out</pre>";

# out docker
my $docker_out = `docker ps -a`;
print "<h3>container list</h3>";
print "<pre style=\"padding-left: 20px\">$docker_out</pre>";

footer();

exit (0);

### Log Page
sub log_page{

        my $logfile = get_value('logfile');
        my $log = `cat $logfile`;
        my $rec;
        my $ucnt;
        my $urec;
        my @ids;
        my @types;
	my @id_type;
	my $x;
	my %counts;

        open(R,"<$logfile");
        while (<R>) {
                my $id = (split/,/,$_)[0];
                my $type = (split/,/,$_)[1];
                my $status = (split/,/,$_)[7];
                my $time = (split/,/,$_)[9];

                $rec = "$id:$type";
                push(@ids,$id);
                push(@id_type,$rec);

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
		}
		if($type eq "ansible-2" && $status == 1){
			$counts{"ansible-2-s"}++;
		}elsif($type eq "ansible-2" && $status == 0){
			$counts{"ansible-2-f"}++;
		}
		if($type eq "serverspec-1" && $status == 1){
			$counts{"serverspec-1-s"}++;
		}elsif($type eq "serverspec-1" && $status == 0){
			$counts{"serverspec-1-f"}++;
		}
		
		
        }
        close(R);

        $ucnt = uniq_func(@ids);
        $urec = uniq_func(@id_type);


# OUTPUT
print "<h3>簡易集計</h3><br>\n";
print "<table class=\"simple\">\n";
print "<tr><th>項目</th><th>値</th></tr>\n";
print "<tr><td>ユニークユーザ数</td><td id=\"r\">$ucnt</td></tr>\n";
print "<tr><td>ユニークトレーニング数</td><td id=\"r\">$urec</td></tr>\n";
print "<tr><td>トータルトレーニング完了数</td><td id=\"r\">$counts{'success'}</td></tr>\n";
print "<tr><td>トータルトレーニング完了時間（分）</td><td id=\"r\"><font color=\"blue\">$counts{'stime'}</font></td></tr>\n";
print "<tr><td>トータルトレーニング未完了時間（分）</td><td id=\"r\"><font color=\"red\">$counts{'ftime'}</font></td></tr>\n";
print "<tr><td>Ansible 初級ハンズオン数（完了）</td><td id=\"r\"><font color=\"blue\">$counts{'ansible-1-s'}</font></td></tr>\n";
print "<tr><td>Ansible 初級ハンズオン数（未完了）</td><td id=\"r\"><font color=\"red\">$counts{'ansible-1-f'}</font></td></tr>\n";
print "<tr><td>Ansible 中級ハンズオン数（完了）</td><td id=\"r\"><font color=\"blue\">$counts{'ansible-2-s'}</font></td></tr>\n";
print "<tr><td>Ansible 中級ハンズオン数（未完了）</td><td id=\"r\"><font color=\"red\">$counts{'ansible-2-f'}</font></td></tr>\n";
print "<tr><td>Serverspec 初級ハンズオン数（完了）</td><td id=\"r\"><font color=\"blue\">$counts{'serverspec-1-s'}</font></td></tr>\n";
print "<tr><td>Serverspec 初級ハンズオン数（未完了）</td><td id=\"r\"><font color=\"red\">$counts{'serverspec-1-f'}</font></td></tr>\n";
print "</table>\n";

print "<h3>ログ</h3><br>\n";
print "<table>\n";
print "<tr><th>ID</th><th>Type</th><th>Start</th><th>End</th><th>Blog</th><th>Htty</th><th>Ttty</th><th>Status</th><th>Finish</th><th>Duration(min)</th></tr>\n";

open(R,"<$logfile");
while (<R>) {
        print "<tr>";

        my @cols = split(/,/,$_);
        foreach $x (@cols){
                print "<td>$x</td>";
        }

        print "</tr>\n";
}
close(R);
print "</table>\n";
print "</p>\n";

}

sub uniq_func{
        my @src = @_;
        my %hash;

        @hash{@src} = ();
        return keys %hash;
}
