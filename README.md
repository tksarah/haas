# Haas

## Setup Memo
* CentOS 7.X x86_64
* Install git screen at wget 
* Install Ansible( 2.1< ) , Docker( 1.11< ) , Zeppelin( 0.6< )
* Perl
  * perl-BerkeleyDB perl-CGI httpd perl-DateTime-Format-Strptime perl-DateTime
* Disable SELinux
* Set Timezone Asia/Tokyo
* useradd -m apache
* uermod -G docker apache
* visudo
```
%apache ALL=(ALL)       NOPASSWD: ALL
Defaults:apache !requiretty
```
* git clone "this repo"
* put /var/www/{cgi-bin,html}
* /var/www/html/default.css
* /var/www/html/docs/*.pdf
* chown -R apache.apache /var/www/

## Configuration
### ip address 
* set.conf
* host_vars/localhost
