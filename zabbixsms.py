#!/usr/bin/python
import logging
import requests
import argparse
import json
import yaml
import sys
from gateways import config
from urllib2 import Request, urlopen
from urllib import urlencode
from slacker import Slacker
from gateways import aws_sns as sns


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
z_login = z.User_Login(config.Z_url, config.Z_user, config.Z_password)


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
	slack = Slacker(config.s_id)
	return slack.chat.post_message(config.s_channel, ZabbixVar()[3], username=config.s_uname)

#Check if we are running this on windows platform
is_windows = sys.platform.startswith('win')

#Console Colors
if is_windows:
        G = Y = B = R = W = G = Y = B = R = W = '' #use no terminal colors on windows 
else:
        G = '\033[92m' #green
        Y = '\033[93m' #yellow
        B = '\033[94m' #blue
        R = '\033[91m' #red
        W = '\033[0m'  #white


def parser_error(errmsg):
        print "Usage: python "+sys.argv[0]+" [Options] use -h for help"
        print R+"Error: "+errmsg+W
        sys.exit()

def msg(name=None):
    return '''  python zabbixsms.py option
                example: python zabbixsms.py slack
           '''

def parse_args():
        parser = argparse.ArgumentParser(prog='Zabbix SMS', description='Zabbix Alerts', usage=msg())
        parser.error = parser_error
        parser._optionals.title = 'OPTIONS'
        parser.add_argument('command', help='Command')
	return parser.parse_args()

def Main():
	args=parse_args()
        if args.command == 'slack':
        	ZabbixSlack()
	if args.command == 'aws-sms':
		sns.AWS_SNS(ZabbixVar()[3])
        if args.command == 'uniphonic':
        	UniPhonic(config.u_appsid, 'type phone number', ZabbixVar()[3]) # you can add multiple phone numbers seperated by ,
	
	if args.command == 'log':
        	ZabbixLog()
if __name__=="__main__":
	try:
		Main()

	except:
		ZabbixLog()
