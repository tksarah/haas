# Page of header 
#         contents
#         footer
#         sidebar

require "./lib.pl";
my $home = get_value('home');

#############################
sub header{

	my $name = shift;

print <<HEADER;
Content-type: text/html

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="html://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja">
 <head>
  <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8"/>
  <title>Handson as a Service</title>
  <base href="$home/"/>
  <link rel="stylesheet" type="text/css" href="./default.css"/>
 </head>
 
<body>	

<div id="header">
  <h2>Handson as a Servic</h2>
</div>

<div id="container">
HEADER

}

#############################
sub contents{

	my $dbh = shift;
	my $name = shift;

        my $table = get_value('utable');
        my $table2 = get_value('atable');
	my $accound_id = get_accountid($dbh,$name);

	my ($sql,$sth,$rv);

	# Set SQL
	$sql = "select id,title,url from $table where main='checked' and account='$accound_id'";

	# Run SQL
	$sth = $dbh->prepare($sql);
	$rv = $sth->execute;
                                                                                                                                     
	my($id,$title,$url);
	$sth->bind_col(1,\$id);
	$sth->bind_col(2,\$title);
	$sth->bind_col(3,\$url);

	print "<ul id=\"list\">\n";
	while($sth->fetchrow_arrayref){
		$url = target_link($url,'new');
                print "<li>【<a href=$url>$title</a>】\n";
                print "[<a href=\"./manage.cgi?sw=edit&id=$id\">編集</a>][<a href=\"./manage.cgi?sw=delete&id=$id\">削除</a>]</li>\n";
        }
        print "</ul>\n";

	$sth->finish;

}
		
#############################
sub footer{

print <<FOOTER;
</div>

<div id="footer">
  <em>
  <font size="2" color="#508090">
  COPYRIGHT(C) 2006-2007 「My Bookmark」 version 0.1<BR>
  ALL RIGHTS RESERVED<BR>
  Author:TK<BR>
  </FONT>
  </em>
</div>

</body>
</html>

FOOTER
}

#############################
sub sidebar{ 

	my $dbh = shift;
	my $name = shift;
	
	my $pub_max;
	my $my_pub_max;

print <<SIDEBAR1;
<div id="sidebar">

 <dl id="globalnav">
   <dt>Bookmark</dt>
   <dd><a href="./bookmark.cgi">トップ</a></dd>
SIDEBAR1

   $pub_max = public_num($dbh,'');
   $my_pub_max = public_num($dbh,$name);
   print "<dd><a href=\"./listup.cgi?category_id=1&num=$pub_max\">公開</a> ($pub_max)</dd>\n";
   print "<dd><a href=\"./listup.cgi?category_id=1&num=$my_pub_max&myflag=1\">My公開</a> ($my_pub_max)</dd>\n";
   ### For Demo
   if($name eq 'admin'){
	print "<dd><a href=\"./admin.cgi?type=1\">ALL URLリスト</a></dd>\n";
	print "<dd><a href=\"./admin.cgi?type=2\">ログインログ</a></dd>\n";
   }
   ### 
   print "<dd>カテゴリ</dd>\n";

        category_out($dbh,$name);

print <<SIDEBAR2;
   <dd>タイトル名で検索</dd>
   <form action="./search.cgi" method="post">
   <INPUT TYPE="text" NAME="search" size="14">
   <input type="submit" value="検索">
   </form>
   <p>
   <dt>Edit</dt>
   <dd><a href="./manage.cgi?sw=newbook">お気に入り登録</a></dd>
   <dd><a href="./manage.cgi?sw=addcate">カテゴリ追加</a></dd>
   <dd><a href="./manage.cgi?sw=delcate">カテゴリ削除</a></dd>
   <p>
   <dt>Readme</dt>
   <dd><a href="./bookmark.cgi?readme=1">使い方</a></dd>
   <dd><a href="./bookmark.cgi?readme=2">お知らせ</a></dd>
   <dd><a href="./bookmark.cgi?readme=3">利用規約</a></dd>
   <p>
   <dt>Administration</dt>
   <dd><a href="./manage.cgi?sw=inquiry">お問い合わせ</a></dd>
   <dd><a href="./manage.cgi?sw=logout">ログアウト</a></dd>
  </dl>
</div>

SIDEBAR2

}
1;

