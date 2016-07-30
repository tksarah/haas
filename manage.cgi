#!/usr/bin/perl

require './lib.pl';
use strict;
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
statistics();

print <<FOOTER;
<p>
<a href="./haas/"  target="_blank">[ Top ]</a>
<a href="./haas/log_check.cgi"  target="_blank">[ Log & Check ]</a>
<a href="http://192.168.175.198:8080/#/"  target="_blank">[ Notebook ]</a>
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
sub statistics{

        my $logfile = get_value('logfile');
        my $rec;
        my $ucnt;
        my $urec;
        my @ids;
        my @types;
	my @id_type;
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

}

sub uniq_func{
        my @src = @_;
        my %hash;

        @hash{@src} = ();
        return keys %hash;
}
