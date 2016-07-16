use lib qw(./lib);

### HEADER Output
sub header{
	$hostaddr = shift;

print <<HEADER;
Content-type: text/html

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="html://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
 <head>
  <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8"/>
  <title>Handson as a Service</title>
  <base href="http://$hostaddr/"/>
  <link rel="stylesheet" type="text/css" href="default.css"/>
 </head>

<body>

<div id="header">
  <h2><a href="http://$hostaddr/cgi-bin/index.cgi">Handson as a Service</a></h2>
</div>

<div id="content">
HEADER

}

### FOOTER Output
sub footer{

print <<FOOTER;
</div>

<div id="footer">
  <em>
  <font size="2" color="#508090">
  COPYRIGHT(C) 2016 「Hands on as a Service」 version 0.1<BR>
  ALL RIGHTS RESERVED<BR>
  Author:TK<BR>
  </FONT>
  </em>
</div>

</body>
</html>
FOOTER

}


### Handson Ref Output
sub handsref{

	my $hostaddr = shift;
	my $type = shift;
	my $wport = shift;
	my $hport = shift;
	my $tport = shift;
	my $endtime = shift;
	my $wp = "http://$hostaddr:$wport/wordpress";
	my $hurl = "http://$hostaddr:$hport/wetty/ssh/root/";
	my $turl = "http://$hostaddr:$tport/wetty/ssh/root/";
	my $str = get_value($type);

print <<START;

<h3>あなたのハンズオン情報</h3>
<dl id="globalnav">
  <dt>ハンズオンマシンアドレス</dt>
    <dd>$hostaddr</dd>
  <dt>ハンズオンコンソール Ansible/Serverspec Host 側</dt>
    <dd><a href="$hurl" target="_blank">$hurl</a></dd>
  <dt>ハンズオンコンソール Ansible/Serverspec Target 側</dt>
    <dd><a href="$turl" target="_blank">$turl</a></dd>
  <dt>WordPressへのアクセスURL</dt>
    <dd><a href="$wp" target="_blank">$wp</a></dd>
  <dt>ハンズオンテキスト</dt>
    <dd><a href="http://$hostaddr/docs/$type.pdf" target="_blank">$str</a></dd>
  <dt>終了時間</dt>
    <dd><font color="red"><b>$endtime</b></a></font></dd>
</dl>

<p>


START
}

### Destroy
sub destroy{

	my $id = shift;
	my $inventory = shift;
	my $playbook = shift;
	my $type = "destroy";
	
	system("ansible-playbook -i $inventory -e \"lesson=$type userid=$id\" $playbook >& /dev/null &");

}

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
	print "現在<font color=\"red\">フル稼働</font>です。1時間以上お待ち下さい。\n";
	print "<table>\n";
	print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th></tr>\n";

	while (($k, $v) = each %data) {
		@list = split(/,/,$v);
		print "<tr>";
		print "<td><a href=\"./cgi-bin/myhandson.cgi?name=$k\">$k</a></td>";
		print "<td>$list[0]</td>";
		print "<td>$list[1]</td>";
		print "<td>$list[2]</td>";
		print "</tr>\n";
		}
	print "</table>\n";
}else{
	print "<table>\n";
	print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th></tr>\n";

	while (($k, $v) = each %data) {
		@list = split(/,/,$v);
		print "<tr>";
		print "<td><a href=\"./cgi-bin/myhandson.cgi?name=$k\">$k</a></td>";
		print "<td>$list[0]</td>";
		print "<td>$list[1]</td>";
		print "<td>$list[2]</td>";
		print "</tr>\n";
		}
	print "</table>\n";
	}		
}

### Error Page
sub error_page{
	
	my $flag = shift;
	my $msg;
	my $url = "http://192.168.0.154/cgi-bin/index.cgi";

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


# Get table name
# Ex: get_value('utable');
sub get_value{

        my $inkey = shift;

        my ($key,$value);
        my %conf;

        open(R,"<./set.conf");
        while (<R>){
                if($_ !~ /^#/){
                        $_ =~ s/\s//g;
                        ($key,$value) = (/(^.*)\=(.*$)/);
                $conf{$key} = $value;
                }
        }
        close(R);

        return $conf{$inkey};
}

1;
