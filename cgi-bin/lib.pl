### Start Input
sub input_form{
        print "<h3>利用開始</h3>";
        print "<form action=\"./cgi-bin/create.cgi\" method=\"post\">";
        print "<h5>社員番号を入力してください。（例：tie304410）</h5><br>";
        print "<input type=\"text\" name=\"name\" size=\"10\">\n";
        print "<h5>ハンズオンの種類を選択してください。</h5><br>";
        print "<input type=\"radio\" name=\"type\" value=\"ansible-1\">Ansible 初級編\n";
        print "<input type=\"radio\" name=\"type\" value=\"ansible-2\">Ansible 中級編\n";
        print "<input type=\"radio\" name=\"type\" value=\"serverspec-1\">Serverspec 初級編\n";
        print "<br><br>\n";
        print "<input type=\"submit\" value=\"ハンズオンビルド\">\n";
        print "</form>\n";
        print "<br>\n";
}

### User Table
sub userlist{
	my %data = @_;
	my $k;
	my $v;
	my @list;

print "<h3>現在の利用状況</h3><br>";

if(keys %data == 0){
	print "利用がありません。\n";
}elsif(keys %data == 10){
	print "現在フル稼働です。1時間以上お待ち下さい。\n";
	print "<table>\n";
	print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th><th>Ports</th><th>Action</th></tr>\n";

	while (($k, $v) = each %data) {
		@list = split(/,/,$v);
		print "<tr>";
		print "<td>$k</td>";
		print "<td>$list[0]</td>";
		print "<td>$list[1]</td>";
		print "<td>$list[2]</td>";
		print "<td>port: '$list[3]',htty: '$list[4]',ttty: '$list[5]'</td>";
		print "<td><form action=\"./cgi-bin/delete.cgi\" method=\"post\"><input type=\"hidden\" name=\"name\" value=\"$k\"><input type=\"submit\" value=\"DELETE\"></form></td>";
		print "</tr>\n";
		}
	print "</table>\n";
}else{
	print "<table>\n";
	print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th><th>Ports</th><th>Action</th></tr>\n";

	while (($k, $v) = each %data) {
		@list = split(/,/,$v);
		print "<tr>";
		print "<td>$k</td>";
		print "<td>$list[0]</td>";
		print "<td>$list[1]</td>";
		print "<td>$list[2]</td>";
		print "<td>port: '$list[3]',htty: '$list[4]',ttty: '$list[5]'</td>";
		print "<td><form action=\"./cgi-bin/delete.cgi\" method=\"post\"><input type=\"hidden\" name=\"name\" value=\"$k\"><input type=\"submit\" value=\"DELETE\"></form></td>";
		print "</tr>\n";
		}
	print "</table>\n";
	}		
}

### Error Page
sub error_page{
	
	my $flag = shift;
	my $msg;
	my $url = "http://192.168.166.210/cgi-bin/index.cgi";

# Login Fail
if($flag == '1'){
	$msg="<b>\"社員番号\"</b>を入力してください。<p>\n";
}elsif($flag == '2'){
	$msg="<b>\"ハンズオンタイプ\"</b>を選択してください。<p>\n";
}elsif($flag == '3'){
	$msg="<b>既にその社員番号は使われています。</b><p>\n";
}


print <<HEAD;
Content-type: text/html


<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="html://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
 <head>
  <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8"/>
  <title>Error Page</title>
 </head>

<body>

<center>
<font color="red"><b>Error:</b></font><br>
HEAD

print "$msg";
print "<a href=\"$url\">[ Back ]</a>";

print <<FOOTER;
</body>
</html>
FOOTER


}

1;

