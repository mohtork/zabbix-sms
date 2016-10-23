#!/usr/bin/python
import logging
import requests
import json
import yaml
from urllib2 import Request, urlopen
from urllib import urlencode
from slacker import Slacker

class Zabbix(object):
	def User_Login(self,zabbix_api_url,uname,password):
		payload = {
          	  "jsonrpc" : "2.0",
          	  "method" : "user.login",
          	  "params" : {
            	  'user': uname,
            	  'password': password,
                 },
                 "auth" : None,
                 "id" : 0,
                }
                headers = {
                 'content-type': 'application/json',
                }

                zabbix_login = requests.post(zabbix_api_url, data=json.dumps(payload), headers=headers)
		zabbix_login = zabbix_login.json()
		return (zabbix_login, zabbix_api_url, headers)
		

z = Zabbix()
z_login = z.User_Login('http://type_zabbixurl/api_jsonrpc.php', 'type_zabbix_uname', 'type_zabbix_password')


def GetInfo():
	url = z_login[1]
	headers = z_login[2]
	payload = {
	    "jsonrpc" : "2.0",
            "method" : "trigger.get",
            "params": {
                  "output": [
                      "only_true",
                      "triggerid",
                      "description",
                      "priority"
                  ],
                  "selectHosts": [
                       "hostid",
                  ],
	
                  "filter": {
                      "value": 1,
                      
	             
                  },
                  "sortfield": "priority",
                  "sortorder": "DESC",
                  "limit": 1

             },
             "auth" : z_login[0][u'result'],
             "id" : 1,
	
        }	
       

	output = requests.post(url, data=json.dumps(payload), headers=headers)
	output = output.json()
	x = output[u'result']
	return x

def HostID():
	Info = GetInfo()
	for i in Info[0][u'hosts']:
        	ID = i[u'hostid']
		return ID


def GetHostName():
	ID = HostID()
        url = z_login[1]
        headers = z_login[2]
        payload = {
            "jsonrpc" : "2.0",
            "method" : "host.get",
            "params": {
               "output": ["name",],
            "hostids": ID
            },
            "auth" : z_login[0][u'result'],
            "id" : 2,
	}
	output = requests.post(url, data=json.dumps(payload), headers=headers)
        output = output.json()
        x = output[u'result']
        return x

def ZabbixVar():
        Priority = GetInfo()[0][u'priority']
        TrigID = GetInfo()[0][u'triggerid']
        HName = GetHostName()[0][u'name']
        Message = GetInfo()[0][u'description']
        Message = str(Message)
        Message = Message.replace("{HOSTNAME}", HName)
        return (Priority, TrigID, HName, Message)


def ZabbixVar():
        Priority = GetInfo()[0][u'priority']
        TrigID = GetInfo()[0][u'triggerid']
        HName = GetHostName()[0][u'name']
        Message = GetInfo()[0][u'description']
        Message = str(Message)
        Message = Message.replace("{HOSTNAME}", HName)
        return (int(Priority), TrigID, HName, Message)

def ZabbixLog():
	Message = ZabbixVar()[3]
	logging.basicConfig(filename='zabbixsms.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
	Debug = logging.debug(Message)
	return Debug
	
def UniPhonic(appsid, mobile, message):
                SMS = message + ' Do not let me down :('
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                Data = 'AppSid=' + appsid + '&Recipient=' + mobile + '&Body=' + SMS
                SendSms = requests.post('http://api.unifonic.com/rest/Messages/Send', data=Data, headers=headers)
                return SendSms

def ZabbixSlack():
	slack = Slacker('type_slack_tocken)
	return slack.chat.post_message('#yourchannelname', ZabbixVar()[3], username="type_name")

def Main():	
	if ZabbixVar()[0] <= 4:
		ZabbixLog()
		


	else:
		ZabbixLog()
		UniPhonic('type_AppSid', 'type_phone_number', ZabbixVar()[3]) # you can add multiple phone numbers seperated by ,
		ZabbixSlack()	
	

if __name__=="__main__":
	try:
		Main()

	except:
		ZabbixLog()
		
