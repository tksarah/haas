use lib qw(./lib);
#use lib qw(/home/sites/lolipop.jp/secret.jp-sarah/lib);

# Modules
use DBI;
use CGI;
use CGI::Session qw/-ip-match/;
use KCatch qw( source );

sub db_open() {

	# DB Setting
	my $dbname = get_value('dbname');
	my $user = get_value('user');
	my $password = get_value('password');
	my $server = get_value('server');

	my $dbh = DBI->connect("dbi:mysql:dbname=$dbname:$server;", $user, $password );
	
	return $dbh;
}

sub db_close() {
	my $dbh = shift;
	$dbh->disconnect();
}

# Check Account
# Check Password 
# return 0 = NG 
#        1 = OK create_session 
#        1 = OK no create_session ( if flag  = 1 ) 
sub check_ac{
	my $dbh = shift;
	my $ac = shift;
	my $pw = shift;
	my $pflag = shift;

	my $table = get_value('atable');
	my ($sql,$sth,$rv);

        # Set SQL
	$sql = "select ac from $table where ac='$ac' and pw='$pw'";
 
        # Run SQL
        $sth = $dbh->prepare($sql);
        $rv=$sth->execute;

	$sth->finish();

	if($rv == 1){
		(!$pflag) && &create_session($dbh,$ac);
        	return 1;
	}
	return 0;
}

# Check session
# return 1        = NG 
#        account  = OK
sub check_session{

	my $dbh = shift;
	my $table = get_value('stable');

        # Get Cookies ID from Client
        my $cgi=CGI->new;
        my $sid = $cgi->cookie("CGISESSID") || undef;

        my $get_name;

	my $session = new CGI::Session("driver:MySQL;serializer:Default;id:md5", $sid, {Handle=>$dbh,TableName=>$table});

        # Get Account from DB
        $get_name = $session->param('name');
        if($get_name ne ""){
                # Re Expire 
                $session->expire('+1h');
                $session->id($sid);
                $session->flush();

		return($get_name);
        }

	# To Login Page
	$session->delete();
        $session->flush();

	return(1);

}

sub exists_url{

	my $dbh = shift;
	my $name = shift;
	my $id = shift;

	my $table = get_value('utable');
	my $table2 = get_value('atable');
	my ($sql,$sth,$rv);

	my $accound_id = get_accountid($dbh,$name);

        # Set SQL
	$sql = "select * from $table where id='$id' and account='$accound_id'";
 
        # Run SQL
        $sth = $dbh->prepare($sql);
        $rv = $sth->execute;

	return $rv;
}

sub target_link{

	my $url = shift;
	my $type = shift;

	if($type eq 'new'){
		return "\"$url\" target=\"_blank\"";
	}else{
		return "$url";
	}

}
	
sub create_session{
	my $dbh = shift;
	my $ac_name = shift;

	my $sid="undef";
	my $table= get_value('stable');
	
	my $session = new CGI::Session("driver:MySQL;serializer:Default;id:md5", $sid, {Handle=>$dbh,TableName=>$table});

	# Get NEW-SID
	my $create_sid = $session->id();
	$session->param('name', $ac_name);

	# Set Session-DATA
	$session->expire('+1h');
	# TEST vaule
	#$session->expire('+1m');

	# To Client SID
	print $session->header(-charset=>'UTF-8');
	$session->flush();

	switch(1,0);
	
}


sub switch{

	my $flag=shift;
	my $time=shift;
	my $home = get_value('home');

	if($flag == 1){

		# Top bookmark.cgi
		print "<HTML><HEAD>\n";
		print "<meta http-equiv=\"Refresh\" content=\"$time;URL=$home/bookmark.cgi\">\n";
		print "</HEAD></HTML>\n";

	}elsif($flag == 2){
		# Error page
		error_page(1);

	}elsif($flag == 3){
		# Login page
		error_page(2);
	}


}

sub category_out{

	my $dbh = shift;
	my $name = shift;
	my $table = get_value('ctable');
	my $table2 = get_value('utable');
	my $table3 = get_value('atable');
	my $accound_id = get_accountid($dbh,$name);

	my ($sql,$sth,$rv);

        # Set SQL
	$sql = "select * from $table 
                where account='$accound_id' order by name";
 
        # Run SQL
        $sth = $dbh->prepare($sql);
        $rv = $sth->execute;

	my ($id,$cname);
	# bind_col
	$sth->bind_col(1,\$id);
	$sth->bind_col(2,\$cname);

	print "<ul id=\"globalnav\">\n";
	while($sth->fetchrow_arrayref){

		my ($sql2,$sth2,$rv2);
		$sql2 = "select id from $table2
                         where cate='$id' and account='$accound_id'";
		$sth2 = $dbh->prepare($sql2);
	        $rv2 = $sth2->execute;
		if($rv2 == ''){$rv2=0;}

        	if($id != '1'){
	        	print "<li><a href=\"./listup.cgi?category_id=$id&num=$rv2\">$cname</a> ($rv2)</li>\n";
		}
		$sth2->finish();
        }
	print "</ul>\n";

	$sth->finish();
}

sub category_select{

	my $dbh = shift;
	my $name = shift;
	my $cate_id = shift;
	my $table = get_value('ctable');
	my $table2 = get_value('atable');
	my $accound_id = get_accountid($dbh,$name);

	my ($sql,$sth);

        # Set SQL
	$sql = "select id,name from $table where account='$accound_id' order by name";
 
        # Run SQL
        $sth = $dbh->prepare($sql);
        $sth->execute;

	my ($id,$cname);
	# bind_col
	$sth->bind_col(1,\$id);
	$sth->bind_col(2,\$cname);

	while($sth->fetchrow_arrayref){
		if($id != '1'){
			if($cate_id eq $id){
		        	print "<option value=$id selected>$cname\n";
			}else{
	        		print "<option value=$id>$cname\n";
			}
		}
        }
	$sth->finish();
}

sub public_num{

	my $dbh = shift;
	my $name = shift;
	my $table = get_value('utable');
	my $accound_id;

	my ($sql,$sth,$rv);

        # Set SQL
	if($name eq ""){
		$sql = "select * from $table where pub='checked'";
	}else{
		$accound_id = get_accountid($dbh,$name);
		$sql = "select * from $table where pub='checked' and account='$accound_id'";
	}
 
        # Run SQL
        $sth = $dbh->prepare($sql);
        $rv = $sth->execute;

	if($rv != 0 ){ return $rv; }
	else { return 0; }
}

# Get category name from id 
sub category_one{

	my $dbh = shift;
	my $id = shift;
	my $table = get_value('ctable');

	my ($sql,$sth,$rv);

        # Set SQL
	$sql = "select name from $table where id=$id";
 
        # Run SQL
        $sth = $dbh->prepare($sql);
        $rv = $sth->execute;

	my ($name,$ret);
	# bind_col
	$sth->bind_col(1,\$name);

	while($sth->fetchrow_arrayref){$ret=$name;} 

	$sth->finish;
	return $ret;
}

# Latest 10
sub latest{

	my $dbh = shift;
	my $name=shift;
	my $table= get_value('utable');
	my $table2= get_value('atable');
	my $accound_id = get_accountid($dbh,$name);

	my $limit=20;

	my ($sql,$sth,$rv);

        # Set SQL
	$sql = "select datetime,title,url from $table
		where account='$accound_id'
		order by datetime desc limit 0,5";
        # Run SQL
        $sth = $dbh->prepare($sql);
        $rv = $sth->execute;

	my ($datetime,$title,$url);
	# bind_col
	$sth->bind_col(1,\$datetime);
	$sth->bind_col(2,\$title);
	$sth->bind_col(3,\$url);

	print "<ol id=\"list\">\n";
	while($sth->fetchrow_arrayref){
		if($title =~ /^.{$limit}/){
			$title=substr($title,0,$limit);
			$title=("$title"."...");
		}
		$url = target_link($url,'new');
		print "<li>[<a href=$url>$title</a>] <em>$datetime</em></li>\n";
	}
	print "</ol>\n";

	$sth->finish;
}

sub logout{

        my $dbh = shift;
        my $name = shift;
        my $str = shift;
	my $table = get_value('stable');
	my $home = get_value('home');

        my $rv;

	my $session = new CGI::Session("driver:MySQL;serializer:Default;id:md5", $sid, {Handle=>$dbh,TableName=>$table});

        # Delete Session
        $session->delete();
        $session->flush();

        # Get Name(->SID) from DB
        my $aname = $session->param('name');

        ### Force delete session record
        if($aname ne ""){

                $sql = "delete from $table where id='$sid'";

                # Run SQL
                $sth = $dbh->prepare($sql);
                $rv  = $sth->execute;
        }
	# Logout Page
	error_page(3);

}

### Error Page
sub error_page{
	
	$flag = shift;

	my $home = get_value('home');

# Login Fail
if($flag == '1'){

print <<HTML_OUT;
Content-type: text/html


<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="html://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
 <head>
  <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8"/>
  <title>My Bookmark</title>
  <meta name="description" content="コンテンツ"/>
  <meta name="keywords" content="ブックマーク"/>
  <base href="$home/"/>
  <link rel="stylesheet" type="text/css" href="./default.css"/>
 </head>

<body>

<center>
ログイン失敗 <br>
<a href="$home/index.html">[ BACK ]</a>
</center>

</body>
</html>

HTML_OUT

# Expire Login 
}elsif($flag == '2'){

print <<HTML_OUT;
Content-type: text/html

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="html://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
 <head>
  <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8"/>
  <title>My Bookmark</title>
  <meta name="description" content="コンテンツ"/>
  <meta name="keywords" content="ブックマーク"/>
  <base href="$home/"/>
  <link rel="stylesheet" type="text/css" href="./default.css"/>
 </head>

<body>
<p>
<b>１時間以上</b>アクセスがなかったか、もしくはログインされていません。
<br>
再度ログインしてください。 ... <a href="$home/index.html">[ ここから ]</a>

</body>
</html>

HTML_OUT

# Logout 
}elsif($flag == '3'){

print <<HTML_OUT;
Content-type: text/html


<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="html://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
 <head>
  <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8"/>
  <meta http-equiv="Refresh" content="1;URL=$home/">
  <title>My Bookmark</title>
  <meta name="description" content="コンテンツ"/>
  <meta name="keywords" content="ブックマーク"/>
  <base href="$home/"/>
  <link rel="stylesheet" type="text/css" href="./default.css"/>
 </head>

<body>

<center>
ログアウトしました。
1秒後にログインページに戻ります。
</center>

</body>
</html>

HTML_OUT
}

}


sub get_accountid{

	my $dbh = shift;
	my $name = shift;
	my $table=get_value('atable');
	my $id;

	my ($sql,$sth,$rv,$ret);

        # Set SQL
	$sql = "select id from $table where ac='$name'";

        # Run SQL
        $sth = $dbh->prepare($sql);
        $rv = $sth->execute;

	# bind_col
	$sth->bind_col(1,\$id);

	while($sth->fetchrow_arrayref){$ret=$id;} 

	$sth->finish;

	return $id; 
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

