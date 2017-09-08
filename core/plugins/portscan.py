#!/usr/bin/env python		
#coding:utf-8

import re
import socket 
import threading 
import Queue 
import nmap
from core.config import output
from core.data import portscan_result

class PortScan:
	def __init__(self,ip="localhost",ports=None,single_port=None,Mask=None,threadNum=5):
		if ports:
			self.ports = ports
		else:
			# 如果不传入配置中的ports，则使用默认posts
			self.ports = [('80', 'web'), ('8080', 'web'), ('3311', 'kangle'), ('3312', 'kangle'), ('3389', 'mstsc'), ('4440', 'rundeck'), ('5672', 'rabbitMQ'), ('5900', 'vnc'), ('6082', 'varnish'), ('7001', 'weblogic'), ('8161', 'activeMQ'), ('8649', 'ganglia'), ('9000', 'fastcgi'), ('9090', 'ibm'), ('9200', 'elasticsearch'), ('9300', 'elasticsearch'), ('9999', 'amg'), ('10050', 'zabbix'), ('11211', 'memcache'), ('27017', 'mongodb'), ('28017', 'mondodb'), ('3777', 'dahua jiankong'), ('50000', 'sap netweaver'), ('50060', 'hadoop'), ('50070', 'hadoop'), ('21', 'ftp'), ('22', 'ssh'), ('23', 'telnet'), ('25', 'smtp'), ('53', 'dns'), ('123', 'ntp'), ('161', 'snmp'), ('8161', 'snmp'), ('162', 'snmp'), ('389', 'ldap'), ('443', 'ssl'), ('512', 'rlogin'), ('513', 'rlogin'), ('873', 'rsync'), ('1433', 'mssql'), ('1080', 'socks'), ('1521', 'oracle'), ('1900', 'bes'), ('2049', 'nfs'), ('2601', 'zebra'), ('2604', 'zebra'), ('2082', 'cpanle'), ('2083', 'cpanle'), ('3128', 'squid'), ('3312', 'squid'), ('3306', 'mysql'), ('4899', 'radmin'), ('8834', 'nessus'), ('4848', 'glashfish')]
		self.threadNum = threadNum
		self.ip = ip
		self.task = Queue.Queue()
		#print self.ports
		for p in self.ports:
			#print p
			self.task.put(p)

		if Mask:
			self.Mask = self.MaskFix(Mask)
			self.single_port = single_port 
			self.markScanport()
		else:
			self.scanports()

	def scanports(self):
		while 1:
			try:
				port,descprition = self.task.get(False)
				port = int(port)
				#print port
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
				s.settimeout(1) 
				try:
					s.connect((self.ip, port))
					mes =  "%s:%s open [%s]"%(self.ip,port,descprition)
					#print mes
					output.openPort(mes)
					portscan_result.append(mes)
				except Exception,e:
					#print e
					mes = "%s:%s close"%(self.ip,port)
					portscan_result.append(mes)
					output.openPort(mes)
				finally:
					s.close()
			except Exception,e:
				print e
				break 

	def MaskFix(self,Mask):
		if 'http://' in Mask or 'https://' in Mask:
			Mask = Mask.replace('http://','').replace('https://','')
	
		if '/' in Mask:
			return Mask 
		else:
			return Mask+'/24'


	def markScanport(self):
		nm = nmap.PortScanner()
		info = nm.scan(hosts=self.Mask,arguments='-p %s'%str(self.single_port))
		nmap_info = info['nmap']
		command_line = nmap_info['command_line']
		scaninfo = nmap_info['scaninfo']
		scan = info['scan']
		output.dataOut('[*] commond: %s'%command_line) 
		output.dataOut('[*] scaninfo:'+str(scaninfo)+'\n') 
		for ip in scan:
			hoststate = scan[ip]['status']['state']
			portstate = scan[ip]['tcp'][self.single_port]['state']
			portname = scan[ip]['tcp'][self.single_port]['name']
			mes = '{0} is {1},{2}/tcp {3} {4}'.format(ip,hoststate,self.single_port,portstate,portname)
			output.maskOpenPort(mes)
			portscan_result.append(mes)


if __name__ == '__main__':
	#ports = {80:"web",8080:"web",3311:"kangle",3312:"kangle",3389:"mstsc",4440:"rundeck",5672:"rabbitMQ",5900:"vnc",6082:"varnish",7001:"weblogic",8161:"activeMQ",8649:"ganglia",9000:"fastcgi",9090:"ibm",9200:"elasticsearch",9300:"elasticsearch",9999:"amg",10050:"zabbix",11211:"memcache",27017:"mongodb",28017:"mondodb",3777:"dahua jiankong",50000:"sap netweaver",50060:"hadoop",50070:"hadoop",21:"ftp",22:"ssh",23:"telnet",25:"smtp",53:"dns",123:"ntp",161:"snmp",8161:"snmp",162:"snmp",389:"ldap",443:"ssl",512:"rlogin",513:"rlogin",873:"rsync",1433:"mssql",1080:"socks",1521:"oracle",1900:"bes",2049:"nfs",2601:"zebra",2604:"zebra",2082:"cpanle",2083:"cpanle",3128:"squid",3312:"squid",3306:"mysql",4899:"radmin",8834:'nessus',4848:'glashfish'}
	PortScan(single_port=445,Mask='211.82.99.1',threadNum=10)
	
