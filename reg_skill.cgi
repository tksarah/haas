#!/usr/bin/perl

require './lib.pl';
use strict;
use CGI;
use DateTime;
use File::Basename;
use JSON;

# From POST
my $form = CGI->new;
my $user = $form->param('name');

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
my $other_c = $form->param('Other_Cloud');

# Get values
my $host = get_value('host');
my $datadir = "../testdata";
my $userdata = "$datadir/$user";

my $data = {
          'skill' => [
                       {
                         'Cloud' => [
                                      {
                                        'Other_Cloud' => "$other_c",
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
                         'Shift' => "$shift"
                       }
                     ]
        };

my $json = JSON->new();
my $json_data = $json->encode($data);

open(W,">$userdata");
print W $json_data;
close(W);


### OUTPUT HTML ###
header("$host");

print "$json_data\n";

print <<FOOTER;
<p>
<hr>
<a href="./haas/manage.cgi">[ Manage Top ]</a>
<p>
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

