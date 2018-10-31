# Zabbix-SMS
Python tool to send you sms notification when one of your host goes down or has a critical issue , Zabbix-SMS also send you a slack notification
and it logs zabbix alerts.

 
# Installation
- git clone https://github.com/mohtork/zabbix-sms
- pip install -r requirements.txt

# Usage
1. Manually 
./zabbixsms.py slack #Send alerts to slack<br/> 
./zabbixsms.py aws-sms #Send alerts to your mobile , list of mobile numbers through aws sns<br/> 
./zabbixsms.py uniphonic #Use uniphonic as your sms gatewat<br/> 

2. Add to Crons
Edit crontab "crontab -e'
* * * * *  /'path-to'/zabbix-sms/zabbixsms.py option<br/>  
replace option with your preferred alert method 'slack, aws-sms or uniphonic<br/> 

# Contact Me
https://goo.gl/WD4T3r
