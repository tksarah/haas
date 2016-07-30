use lib qw(./lib);
use IO::Socket;

### HEADER Output
sub header{
	$hostaddr = shift;

print <<HEADER;
Content-type: text/html
Pragma: no-cache
Cache-Control: no-cache
Cache-Control: post-check=0, pre-check=0
Expires: Thu, 01 Dec 1994 16:00:00 GMT


<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="html://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
 <head>
  <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8"/>
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>Handson as a Service</title>
  <base href="http://$hostaddr/"/>
  <link rel="stylesheet" type="text/css" href="default.css"/>
 </head>

<body>

<div id="header">
  <h2><a href="http://$hostaddr/haas/index.cgi">Handson as a Service</a></h2>
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

### Usage Output
sub usage{

print <<USAGE;
<b>Update</b>
<ul style="list-style:none;">
 <li><b>（2016/8/1）</b> 正式リリース </li>
</ul>
<b>Known Issues</b>
<ul style="list-style:none;">
 <li><b>（2016/8/1）</b>...</li>
</ul>
<hr>
こちらは、社員が自らのタイミングでセルフスタディできるようにしたハンズオンサービスです。現在は、AnsibleやServerspecの基礎を学べます。<p>
<p><font color="red">良く読んでから実施してください。</font>

<h3>利用方法</h3>
<ul id="list">
<li><b>社員番号を入力</b>します</li>
<li><b>ハンズオンの種類を選択</b>します</li>
<li>「ハンズオンビルド」ボタンを押すと、ハンズオンの環境が作られます</li>
<li>ハンズオンの環境の情報ページに沿って<b>環境にアクセスし実施</b>します</li>
<li>ハンズオン実施の工数は<u>各部の教育工数としてカウント</u>されるようトレースされます</li>
</ul>

<h4>前提および、保持スキル</h4>
<ul id="list">
<li>社内で開催している<b>”Ansible or Serverspec の概要編”</b>を受講済み、または同等の知識を保持</li>
<li>Unix/Linuxオペレーション1年以上の経験、またはLPIC Level 1 同等以上の知識を保持</li>
<li>viによるファイル編集、基本的なUnix/Linuxオペレーションが可能</li>
</ul>

<h4>必要なもの</h4>
<ul id="list">
<li>社内のLANにつながっているPC</li>
<li>ブラウザ（Internet Explorer or Chrome で動作確認済み）</li>
</ul>


<h4>注意と制限</h4>
<ul id="list">
<li>ブラウザでうまく表示されない場合、プロキシ設定を外してから実施してください</li>
<li>ハンズオンの環境は<font color=red><b>60分</b></font>で自動的に削除されます</li>
<li>同じ社員が同時に2つ以上のハンズオンを実行できません</li>
<li><font color=red>10社員</font>までが同時に本サービスを利用可能です</li>
</ul>

<h4>メニュー</h4>
<ul id="list">
<li><b>Ansible 初級ハンズオンズ</b>・・・たった２つのファイルから自動化を行う簡単なハンズオン</li>
<li><b>Ansible 中級ハンズオンズ</b>・・・実践的な形で自動化を行うハンズオン（Roleの利用）</li>
<li><b>Serverspec 初級ハンズオンズ</b>・・・テストを始める準備から簡単なテストコードを使ったハンズオン</li>
</ul>
USAGE

}

### Howto&Help
sub howto{

print <<HOWTO;
<p>
<h3>Web Console のTips</h3>
<ul id="list">
  <li>ラウザのページ単位が1つのSSHセッション</li>
  <li><b>Copy & Paste</b>は、Ctrl+C , Ctrl+V で可能</li>
  <li><font color="red">コンソールが出てこない（ブラウザが黒いまま）の時</font>、ブラウザの「更新」を試みる</li>
  <li><font color="red">コンソールが乱れたら</font>、ブラウザの「更新」か新たにページを開く</li>
</ul>
HOWTO
}

### Handson Ref Output
sub handsref{

	my $hostaddr = shift;
	my $type = shift;
	my $wport = shift;
	my $hport = shift;
	my $tport = shift;
	my $endtime = shift;
	my $name = shift;
	my $wp = "http://$hostaddr:$wport/wordpress";
	my $hurl = "http://$hostaddr:$hport/wetty/ssh/root/";
	my $turl = "http://$hostaddr:$tport/wetty/ssh/root/";
	my $str = get_value($type);

print <<START;

<h3>$nameさんのハンズオン情報</h3>
<dl id="globalnav">
  <dt>ハンズオンコンソール Ansible/Serverspec Host 側</dt>
    <dd><a href="$hurl" target="_blank">$hurl</a></dd>
  <dt>ハンズオンコンソール Ansible/Serverspec Target 側</dt>
    <dd><a href="$turl" target="_blank">$turl</a></dd>
  <dt>WordPressへのアクセスURL</dt>
    <dd><a href="$wp" target="_blank">$wp</a></dd>
  <dt>ハンズオンテキスト</dt>
    <dd><a href="http://$hostaddr/docs/$type.pdf" target="_blank">$str</a><font size="2pt"> （"3章"から進めてください）</font></dd>
  <dt>終了時間</dt>
    <dd><font color="red"><b>$endtime</b></a></font></dd>
</dl>

<p>


START
}

### Create
sub create{

	my $id = shift;
	my $type = shift;
	my $bport = shift;
	my $htty = shift;
	my $ttty = shift;
	my $inventory = shift;
	my $playbook = shift;
	
	# Run Playbook
	system("ansible-playbook -i $inventory -e \"lesson=$type userid=$id port=$bport htty=$htty ttty=$ttty\" $playbook >& /dev/null &");


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
        print "<form action=\"./haas/create.cgi\" method=\"post\"><p>";
        print "<b>社員番号を入力してください。（例：123456）</b><p>\n";
        print "<input type=\"text\" name=\"name\" size=\"10\"><p>\n";
        print "<b>ハンズオンの種類を選択してください。</b>";
	print "<ol style=\"list-style:none;\">\n";
        print "<li><input type=\"radio\" name=\"type\" value=\"ansible-1\"><b><font color=\"blue\"> Ansible 初級編</font></b></li>\n";
        print "<li><input type=\"radio\" name=\"type\" value=\"ansible-2\"><b><font color=\"blue\"> Ansible 中級編</font></b></li>\n";
        print "<li><input type=\"radio\" name=\"type\" value=\"serverspec-1\"><b><font color=\"blue\"> Serverspec 初級編</font></b></li>\n";
	print "</ol>\n";
        print "<p>\n";
        print "<b>以下のボタンを押してハンズオン環境を構築します。</b><p>\n";
        print "<input id=\"button\" type=\"submit\" value=\"ハンズオンビルド\">\n";
        print "</form>\n";
        print "<br>\n";
}

### User Table
sub userlist{
	my %data = @_;
	my $k;
	my $v;
	my $max_emp = get_value('max_emp');
	my @list;

print "<h3>現在の利用状況</h3><br>";

if(keys %data == 0){
	print "利用者がいません。<p>\n";
}elsif(keys %data == $max_emp){
	print "現在<font color=\"red\">フル稼働</font>です。1時間以上お待ち下さい。\n";
	print "<table>\n";
	print "<tr><th>User name</th><th>Lesson</th><th>Start time</th><th>End time</th></tr>\n";

	while (($k, $v) = each %data) {
		@list = split(/,/,$v);
		print "<tr>";
		print "<td><a href=\"./haas/myhandson.cgi?name=$k\">$k</a></td>";
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
		print "<td><a href=\"./haas/myhandson.cgi?name=$k\">$k</a></td>";
		print "<td>$list[0]</td>";
		print "<td>$list[1]</td>";
		print "<td>$list[2]</td>";
		print "</tr>\n";
		}
	print "</table>\n";
	print "</p>\n";
	}		
}

### Logging
sub logging{
	my @list = @_;

        open(W,">>$list[-1]");
	for($i=0; $i <= $#list-1; $i++){
		if($i == $#list-1){
			print W "$list[$i]\n";
		}else{
			print W "$list[$i],";
		}
	}
        close(W);

}

### Error Page
sub error_page{
	
	my $flag = shift;
	my $host = shift;
	my $msg;
	my $url = "http://$host/haas/index.cgi";

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

# Socket & Connect
sub check_http{

        my $ip = shift;
        my $port = shift;

        $remote = IO::Socket::INET->new( Proto => "tcp",
        PeerAddr => "$ip",
        PeerPort => "$port"
        );

        unless($remote){
                return (0);
        }
        $remote->autoflush(1);

        #print $remote "GET /wordpress/wp-admin/install.php \n\n";
        print $remote "HEAD /wordpress/wp-admin/install.php \n\n";

        $f=<$remote>;
        close $remote;

        if($f =~ /DOCTYPE\sHTML/){
                #print "HTTP OK\n";
                return (1)

        }else{
                return (0)
        }

}

sub uniq_func{
	my @src = @_;
	my %hash;

	@hash{@src} = ();
	return keys %hash;
}

1;


