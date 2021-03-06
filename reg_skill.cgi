#!/usr/bin/perl

require 'lib.pl';
use strict;

# From POST
my $form = CGI->new;
my $user = $form->param('userid');
my $username = $form->param('username');
my $depname = $form->param('depname');

my $shift = $form->param('Shift');
my $ansible = $form->param('Ansible');
my $puppet = $form->param('Puppet');
my $chef = $form->param('Chef');
my $saltstack = $form->param('SaltStack');
my $itamae = $form->param('Itamae');
my $serverspec = $form->param('Serverspec');
my $infrataster = $form->param('Infrataster');
my $aws = $form->param('AWS');
my $azure = $form->param('Azure');
my $softlayer = $form->param('SoftLayer');
my $docker = $form->param('Docker');
my $openstack = $form->param('OpenStack');

# Get values
my $host = get_value('host');
my $datadir = get_value('udatadir');
my $userdata = "$datadir/$user";

my $data = {
          'skill' => [
                       {
                         'Cloud' => [
                                      {
                                        'Azure' => "$azure",
                                        'SoftLayer' => "$softlayer",
                                        'AWS' => "$aws",
                                        'Docker' => "$docker",
                                        'OpenStack' => "$openstack"
                                      }
                                    ],
                         'Test' => [
                                     {
                                       'Serverspec' => "$serverspec",
                                       'Infrataster' => "$infrataster"
                                     }
                                   ],
                         'Automation' => [
                                           {
                                             'Itamae' => "$itamae",
                                             'Chef' => "$chef",
                                             'Ansible' => "$ansible",
                                             'SaltStack' => "$saltstack",
                                             'Puppet' => "$puppet"
                                           }
                                         ],
                         'Shift' => "$shift",
                         'Username' => "$username",
                         'Depname' => "$depname"
                       }
                     ]
        };

my $json = JSON->new();
my $json_data = $json->encode($data);

# Write user data
open(W,">$userdata");
print W $json_data;
close(W);


### OUTPUT HTML ###
header("$host");

print "登録されました。<p>\n";
print "<a href=\"http://$host/haas/user_skill.cgi?userid=$user\">[ ここから ] </a>確認できます。<p>";
print "<a href=\"http://$host/haas/\">[ Back Home ]</a>";

footer();

exit (0);
