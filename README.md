# Haas

## Setup Memo
* CentOS 7.X x86_64
* Install Ansible( 2.1< ) , Docker( 1.11< ) , Zeppelin( 0.6< )
* Perl
  * perl-berkeleydb perl-CGI httpd perl-DateTime-Format-Strptime perl-DateTime
* Disable SELinux
* Set Timezone Asia/Tokyo
* Useradd apache
* uermod -G docker apache
* visudo
```
%apache ALL=(ALL)       NOPASSWD: ALL
Defaults:apache !requiretty
```
* git clone "this repo"
* put /var/www/{cgi-bin,html}
* chown -R apache.apache /var/www/

## Configuration
### ip address 
* set.conf
* host_vars/localhost
