#!/usr/bin/perl

require './lib.pl';
use strict;
use CGI;
use File::Basename;
use JSON;

# From POST
my $form = CGI->new;
my $user = $form->param('userid');

# Get values
my $host = get_value('host');
my $datadir = get_value('udatadir');
my $userdata = "$datadir/$user";

my $back_url = $ENV{'HTTP_REFERER'};
if(!$back_url){
        $back_url = "http://$host/haas/";
}

# Check ID
if($user eq "000000" || $user eq "" ||  $user !~ /^\w{6}$/ ){
        error_page(1,$back_url);
        exit(0);
}



# Format Initialize
$userdata = "$datadir/000000" if (! -f $userdata);
my @shift_level = (
	"聞いたことがない。",
	"名前だけ聞いたことがある。",
	"資料やガイドを見ことがある、社内研修を受けたことがある。",
	"1度でも利用したことがある。（検証や、個別利用等可）",
	"案件へ利用したことがある。（部分利用も可）",
	"Shift用のコードを見て、バグを指摘したことがある。",
	"Shift用のコードを自ら修正したことがある。",
	"Shift用のコードを書いたことがある。",
	"Shiftの開発・メンテナーである。"
);
my @other_level = (
	"聞いたことがない。",
	"名前だけ聞いたことがある。",
	"社内研修、イベントを受けたがある。",
	"利用したことがある。（検証や、個別利用等可）",
	"自力でこのツールのコードを修正できる。",
	"自力でこのツールのコードを書ける。"
);

my @cloud_level = (
	"聞いたことがない。",
	"名前だけ聞いたことがある。",
	"GUIやポータルでの当該のクラウド/コンテナを操作したことがある。",
	"CUIで手動で当該のクラウド/コンテナを操作したことがある。（コードは書かない）",
	"APIやAutomation/Testツールを使って当該クラウド/コンテナの操作ができる。（コードを書く）"
);

my @user_meta = check_user($user);

### OUTPUT HTML ###
header("$host");

my $items = parse_json($userdata);
input_func($user,$items,@user_meta);

footer();

exit (0);

sub input_func{

	my $userid = shift;
	my $items = shift;
	my @user_meta = @_;

        my $shift = $items->{skill}->[0]->{Shift};
	my $auto = $items->{skill}->[0]->{Automation}->[0];
	my $test = $items->{skill}->[0]->{Test}->[0];
	my $cloud = $items->{skill}->[0]->{Cloud}->[0];
	my $i;

	print <<HTML_1;

	<h3>本部施策コードの熟練度を登録 （$user_meta[0] / $userid / $user_meta[1]）</h3><p>
        <form action="./haas/reg_skill.cgi" method="post">
	<input type="hidden" name="userid" value="$userid">
	<input type="hidden" name="username" value="$user_meta[0]">
	<input type="hidden" name="depname" value="$user_meta[1]">
HTML_1

	print "<h4 id=\"archive\">Shift</h4>\n";
	print "<p>\n";
	print "<table>\n";
	print "<tr><th>レベル</th><th>熟練度チェック指標</th></tr>\n";
	for ($i=1;$i<10;$i++){
		if($shift == $i){
			print "<tr><td><input type=\"radio\" name=\"Shift\" value=\"$i\" checked>$i</td><td>$shift_level[$i-1]</td></tr>\n";
		}else{
			print "<tr><td><input type=\"radio\" name=\"Shift\" value=\"$i\">$i</td><td>$shift_level[$i-1]</td></tr>\n";
		}
	}
	print "</table>\n";
	print "<p>\n";

	print "<div onclick=\"obj=document.getElementById('skill_detail').style; obj.display=(obj.display=='none')?'block':'none';\">\n";
	print "<a style=\"cursor:pointer;\"><h3>個別にチェックしてください。（オプション）</h3></a>\n";
	print "</div><p>\n";
	print "<div id=\"skill_detail\" style=\"display:none;clear:both;\">\n";
	
	print "<ol id=\"readme\">\n";
	foreach (@other_level){
		print "<li>$_</li>\n";
	}
	print "</ol>\n";
	
	print "<h4 id=\"archive\">Automation</h4>\n";
	print "<dl>\n";
	foreach my $k (sort keys $auto){
		my $item = $items->{skill}->[0]->{Automation}->[0]->{$k};
		print "<dt><b>$k</b></dt>\n";
		print "<dd>\n";
		for ($i=1;$i<7;$i++){
			if($item == $i){
				print "<input type=\"radio\" name=\"$k\" value=\"$i\" checked>$i\n";
			}else{
				print "<input type=\"radio\" name=\"$k\" value=\"$i\">$i\n";
			}
		}
	}

	print "</dl>\n";
	print "<h4 id=\"archive\">Test</h4>\n";
	print "<dl>\n";
	foreach my $k (sort keys $test){
		my $item = $items->{skill}->[0]->{Test}->[0]->{$k};
		print "<dt><b>$k</b></dt>\n";
		print "<dd>\n";
		for ($i=1;$i<7;$i++){
			if($item == $i){
				print "<input type=\"radio\" name=\"$k\" value=\"$i\" checked>$i\n";
			}else{
				print "<input type=\"radio\" name=\"$k\" value=\"$i\">$i\n";
			}
		}
	}

	print "</dl>\n";
	print "<h4 id=\"archive\">Cloud</h4>\n";
	print "<ol id=\"readme\">\n";
	foreach (@cloud_level){
		print "<li>$_</li>\n";
	}
	print "</ol>\n";
	print "<dl>\n";
	foreach my $k (sort keys $cloud){
		my $item = $items->{skill}->[0]->{Cloud}->[0]->{$k};
		print "<dt><b>$k</b></dt>\n";
		print "<dd>\n";
		for ($i=1;$i<6;$i++){
			if($item == $i){
				print "<input type=\"radio\" name=\"$k\" value=\"$i\" checked>$i\n";
			}else{
				print "<input type=\"radio\" name=\"$k\" value=\"$i\">$i\n";
			}
		}
	}

	print <<HTML_2;
	</dl>
	</div>

	<input type="submit" value="Registration">
	</form>
HTML_2
}


sub parse_json{

        my $filepath = shift;
        my $json_data;
        my $ref_hash;

        open(R,"<$filepath");
        $json_data = <R>;
        close(R);
        $ref_hash = JSON->new()->decode($json_data);

        return $ref_hash;
}

sub check_user{

	my $user = shift;
	my $depname;
	my $uid;
	my $uname;
	my $pass = 1;
	my @listfiles = `ls /var/www/cgi-bin/data/*.list`;
	LOOP: foreach my $depfile (@listfiles) {
		chomp($depfile);
		$depname = basename($depfile,'.list');
		open(R,"<$depfile");
		while (<R>) {
			$uid = (split/,/,$_)[0];
			$uname = (split/,/,$_)[1];
			if( $uid =~ /$user/ ){
				$pass = 0;
				last LOOP;
			}
		}
		close(R);
	}
	if($pass){
		error_page(4,$back_url,"その番号は無効な社員番号です。");
		exit(1);
	}
	my @ret=("$uname","$depname");

	return(@ret);


}
