时间同步
=======

参考资料: https://vitux.com/how-to-install-ntp-server-and-client-on-ubuntu/  

局域网内部集群服务器的时间同步

sudo apt-get install ntp ntpdate

/etc/ntp.conf

时间服务器 对应文件 ntp-server.conf
时间客户端 对应文件 ntp-client.conf

sudo systemctl status ntp
sudo systemctl enable ntp.service
sudo systemctl start ntp.service

设置107为时间同步服务器

ntpdate -u 10.239.1.107

查看

ntpq -p

设置hosts
=========
/etc/hosts  

fincal 10.239.1.107

timedatectl
===========

参考资料:  
https://www.cnblogs.com/zhi-leaf/p/6282301.html

sudo timedatectl status
sudo timedatectl set-time 15:58:30
sudo timedatectl set-time '16:10:40 2015-11-20'

sudo timedatectl list-timezones
sudo timedatectl set-timezone "Asia/Shanghai"

将硬件时钟设置为本地时区  
sudo timedatectl set-local-rtc 1 --adjust-system-clock

将硬件时钟设置为协调世界时（UTC）  
sudo timedatectl set-local-rtc 0

另一种将硬件时钟设置为本地时区
sudo hwclock -w