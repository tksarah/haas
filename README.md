# Haas
* CentOS 7.X x86_64

## Install

* Install git, screen, at, wget , ntp
* Install Ansible( 2.1< ) , Docker( 1.11< )
* Perl
  * perl-BerkeleyDB perl-CGI httpd perl-DateTime-Format-Strptime perl-DateTime
  * perl-JSON perl-Data-Dumper

## Configuration

* Disable SELinux
* Set Timezone Asia/Tokyo
* Set NTP Server
* useradd -m apache
* uermod -G docker apache
* visudo
```
%apache ALL=(ALL)       NOPASSWD: ALL
Defaults:apache !requiretty
```
* git clone https://github.com/tksarah/haas.git
* put /var/www/{cgi-bin,html}
* move /var/www/html/default.css
* move /var/www/html/docs/*.pdf
* chown -R apache.apache /var/www/

## httpd.conf Configuration
```
<Directory /var/www/html>
    Options -Indexes +FollowSymLinks

ScriptAlias /haas/ "/var/www/cgi-bin/"

AddHandler cgi-script .cgi

<IfModule dir_module>
    DirectoryIndex index.html index.cgi
</IfModule>

```

### set ip address 

* set.conf
* host_vars/localhost

### set user data (Option)

* List files ./data/XXX.list
```
<id>,<name>
<id>,<name>
<id>,<name>
```

### Archive momo

* Archive directory : ./data/archives
* Archive files : ./data/archives/＜YYYY＞-＜MM＞-＜Dep＞.log
* Create archive file : ./run_out.pl 07 2016

### User Skill momo

* User data directory : ./data/udata
* User data files : ./data/udata/＜ID＞
* Data format : JSON
