#!/usr/bin/perl

require 'lib.pl';
use strict;
use BerkeleyDB;
use vars qw( %h $k $v );

# From POST
my $form = CGI->new;
my $guest = $form->param('guest');
my $id = $form->param('name');
my $type = $form->param('type');

# Get values
my $limit = get_value('limit');
my $host = get_value('host');
my $playhome = get_value('playhome');
my $inventory = get_value('inventory');
my $inventoryfile = "$playhome/$inventory";
my $playbook = get_value('playbook');
my $playbookfile = "$playhome/$playbook";
my $dbfilename = get_value('dbfilename');
my @list;

my $back_url = $ENV{'HTTP_REFERER'};
if(!$back_url){
        $back_url = "http://$host/haas/";
}

# DB Initialize file
tie %h, "BerkeleyDB::Hash",
        -Filename => $dbfilename,
        -Flags    => DB_CREATE
    or die "Cannot open file $dbfilename: $! $BerkeleyDB::Error\n";
my $num = keys %h;

# when id is 1 check name skipped
if($guest == 1 && $id eq "" ){ 
	$id = "guest_$num";
}else{
	# Check name,type exists/name duplicated
	my $state = user_check($id);
	if( $state eq "" ){
		error_page(1,$back_url);
		exit(0);
	}
	# Lower 6 digits
	$id = substr($id,-6,6);
	if($h{$id}){
		error_page(3,$back_url);
		exit(0);
	}
}
# Check hands-on type
if($type eq ""){
	error_page(2,$back_url);
	exit(0);
}

# Get time
my $dts = DateTime->now(time_zone => 'Asia/Tokyo');
my $dte = $dts->clone;
$dte->add(minutes => $limit);

# Create ports
my $blog = 8081 + $num;
my $htty = 3000 + $num + 1;
my $ttty = $htty + 10;

# Check Open port
my $ret = system("ss -ltn | grep $blog");
if(!$ret){
	my $add = int(rand(99));
	$blog = $blog + $add;
	$htty = $htty + $add;
	$ttty = $ttty + $add;
}
	
# Generate portlist
my $port = "$blog,$htty,$ttty";

# Make string
my $string = "$type,$dts,$dte,$port";

# Run Playbook
create($id,$type,$blog,$htty,$ttty,$inventoryfile,$playbookfile);
#system("ansible-playbook -i $playhome/hosts -e \"lesson=$type userid=$id port=$blog htty=$htty ttty=$ttty\" $playhome/site.yml >& /dev/null &");

# Set k/v
$h{"$id"} = $string;

untie %h;

### OUTPUT HTML ###
header("$host");

print "ハンズオン環境を作成しました。<p>\n";
print "以下の情報を元にハンズオンを始めてください。なお、この環境は<font color=\"red\"><b>６０分後に自動的に削除</b></font>されますのでそれまでに実施してください。\n";

handsref($host,$type,$blog,$htty,$ttty,$dte,$id);

print "完了したら以下の「 終了 」ボタンを押してください。実施が記録され、環境がクリアされます。<br>";
print "<form action=\"./haas/delete.cgi\" method=\"post\">\n";
print "<input type=\"hidden\" name=\"name\" value=\"$id\"><input id=\"button\" type=\"submit\" value=\"終了\">\n";
print "</form><br><br>\n";
print "このページの情報（ご自身のハンズオン環境の情報）はTopページの<b>現在の利用状況</b>テーブルから自身の社員番号をクリックすることでも確認できます。";
print "<a href=\"http://$host/haas/\"><b>[ Top ]</b></a>\n";

howto();
footer();

exit (0);
