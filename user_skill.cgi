#!/usr/bin/perl

require './lib.pl';
use strict;
use CGI;
use JSON;

# From POST
my $form = CGI->new;
my $user = $form->param('userid');

# Get values
my $host = get_value('host');
my $datadir = get_value('udatadir');
my $userdata = "$datadir/$user";

### OUTPUT HTML ###
header("$host");

# Check ID
if($user eq "000000" || $user !~ /^\w{6}$/){
	input4html();
}else{
	my $items = parse_json($userdata);
	output_html($user,$items);
}

footer();

exit (0);

sub output_html{
	my $user = shift;
	my $items = shift;
	my $shift = $items->{skill}->[0]->{Shift};
	my $username = $items->{skill}->[0]->{Username};
	my $depname = $items->{skill}->[0]->{Depname};
	my $ansible = $items->{skill}->[0]->{Automation}->[0]->{Ansible};
	my $chef = $items->{skill}->[0]->{Automation}->[0]->{Chef};
	my $puppet = $items->{skill}->[0]->{Automation}->[0]->{Puppet};
	my $saltstack = $items->{skill}->[0]->{Automation}->[0]->{SaltStack};
	my $itamae = $items->{skill}->[0]->{Automation}->[0]->{Itamae};
	my $serverspec = $items->{skill}->[0]->{Test}->[0]->{Serverspec};
	my $infrataster = $items->{skill}->[0]->{Test}->[0]->{Infrataster};
	my $docker = $items->{skill}->[0]->{Cloud}->[0]->{Docker};
	my $openstack = $items->{skill}->[0]->{Cloud}->[0]->{OpenStack};
	my $aws = $items->{skill}->[0]->{Cloud}->[0]->{AWS};
	my $azure = $items->{skill}->[0]->{Cloud}->[0]->{Azure};
	my $softlayer = $items->{skill}->[0]->{Cloud}->[0]->{SoftLayer};
	my $other_cloud = $items->{skill}->[0]->{Cloud}->[0]->{Other_Cloud};

print <<HTML_USER_OUT;
<h3>$username / $depname</h3><br>
<table class="simple">
<tr><th>項目</th><th>熟練度</th></tr>
<tr><td><b>Shift</b></td><td id="r">$shift</td></tr>
<tr><td>Ansible</td><td id="r">$ansible</td></tr>
<tr><td>Chef</td><td id="r">$chef</td></tr>
<tr><td>Puppet</td><td id="r">$puppet</td></tr>
<tr><td>SaltStack</td><td id="r">$saltstack</td></tr>
<tr><td>Itamae</td><td id="r">$itamae</td></tr>
<tr><td>Serverspec</td><td id="r">$serverspec</td></tr>
<tr><td>Infrataster</td><td id="r">$infrataster</td></tr>
<tr><td>Docker</td><td id="r">$docker</td></tr>
<tr><td>OpenStack</td><td id="r">$openstack</td></tr>
<tr><td>AWS</td><td id="r">$aws</td></tr>
<tr><td>Azure</td><td id="r">$azure</td></tr>
<tr><td>SoftLayer</td><td id="r">$softlayer</td></tr>
<tr><td>Other_Cloud</td><td id="r">$other_cloud</td></tr>
</table>
HTML_USER_OUT
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

output_html();

footer();

exit (0);

sub input4html{
        print <<HTML_OUT;
        <form action="./haas/user_skill.cgi" method="post">
        <h4 id="archive">社員番号を入力（例：123456）</h4>
        <p>
        <input type="text" name="userid" size="6">
        <input type="submit" value="Registration">
        </form>

HTML_OUT
}
