# Zabbix-SMS
Python tool to send you sms notification when one of your host goes down or has a critical issue , Zabbix-SMS also send you a slack notification
and it logs zabbix alerts.

 
# Dependencies
Zabbix-SMS needs Slacker module which you can simply install via
- pip install slacker.  or you can get it from
- https://github.com/os/slacker

# Usage
you can run it manually 
python zabixsms.py or it's better to run it as a cronjob, an example of cron job that execute zabbix-sms every one minitue
- */1   *    *    *    * pathto/zabbixsms.py


# Limits
- The tool support uniphonic sms gateway only , in the future it will support more gateways


# Contact Me
https://goo.gl/WD4T3r
