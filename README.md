# Haas
* CentOS 7.X x86_64

## Install
* Install git screen at wget 
* Install Ansible( 2.1< ) , Docker( 1.11< )
* Perl
  * perl-BerkeleyDB perl-CGI httpd perl-DateTime-Format-Strptime perl-DateTime

## Configuration
* Disable SELinux
* Set Timezone Asia/Tokyo
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

### set ip address 
* set.conf
* host_vars/localhost
