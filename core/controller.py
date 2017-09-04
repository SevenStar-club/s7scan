#!/usr/bin/env python		
#coding:utf-8

import os
import sys
import json
import argparse
import threading
import random
from core.config import ConfigFileParser,webdir_result,portscan_result,exploit_result
from core.data import output,data,queue,output,threads_num,paths,banners,colorprinter,print_random_text
from core.exploit import loadScript,loadTargets
from core.plugins.thread_func import Thread_Func
from core.plugins.process_func import speed
from core.plugins.portscan import PortScan


class Controller():
	def __init__(self):
		self.cf  = ConfigFileParser()
		threads_num = self.cf.threads_num()
		print_random_text(banners[random.randint(0,4)])
		#colorprinter.print_blue_text(u'[-_-]不忘初心，一群走在安全路上的年轻人[-_-]')

	def webdir(self,args):
		output.dataOut('[*] 加载目录扫描插件...')
		#参数解析
		url = args.u
		outfile = args.o
		output.target(url)

		#配置文件解析
		mode = self.cf.webdir_mode()

		#调用扫描插件
		if mode == '0':
			Thread_Func(url,data,threads_num)
		if mode =='1':
			pass 
		if mode == '2':
			speed(Thread_Func,url)

		if outfile:
			self.report(webdir_result,outfile)

	def portscan(self,args):
		output.dataOut('[*] 加载端口扫描插件...')
		#参数解析
		ip = args.t
		mask = args.m 
		port = args.p
		outfile = args.o

		# 获取配置文件里的端口信息
		scanports = self.cf.scanports()
		
		#调用插件
		if ip:
			output.target(ip)
			ps = PortScan(ports=scanports)
		elif mask:
			if port:
				ps = PortScan(single_port=port,Mask='211.82.99.1')
			else:
				output.warning('please input port')

		if outfile:
			self.report(portscan_result,outfile)

			
	def Exploit(self,args):
		# list所有的poc
		if args.list:
			files = os.listdir(paths['SCRIPT_PATH'])
			mes1 = '[*] Script Name（总共%s个POC)'%str(len(files)-1)
			output.dataOut(mes1)
			for file in files:
				if '__init__' not in file:
					output.dataOut('   '+file)

		# 查询文件名
		if args.q:
			keyword = args.q
			files = os.listdir(paths['SCRIPT_PATH'])
			mes = "[*] 查询关键字: %s"%keyword
			output.dataOut(mes)
			for file in files:
				if '__init__' not in file:
					if keyword in file:
						output.dataOut('   '+file)

		#加载poc文件
		if args.s:
			script_name = args.s
			if script_name.endswith('.py'):
				script_name = script_name[:-3]
			#print script_name
			output.dataOut('[*] 加载poc: %s.py ...\n'%script_name)
			script_path = paths['SCRIPT_PATH']+script_name
			self.script_obj = loadScript(script_name)
			#print self.script_obj.poc(1)

		if (args.s and not args.u) and (args.s and not args.m):
			output.error('请设置target目标')
			sys.exit()

		#加载目标
		loadTargets(args)

		# 如果是单个url, 直接调用scan函数，没必要用多线程
		if args.u:  
			output.target(args.u)
			self.scan()
		else:
			self.run()
		if args.o:
			outfile = args.o 
			self.report(exploit_result,outfile)

	# 对单个目标的扫描
	def scan(self):
		while 1:
			try:
				url = queue.get(False)
				#print url
				res = self.script_obj.poc(url)
				if res: # 如果失败返回False
					mes = 'Target %s is exploit...: %s'%(url,res)
					output.expOut(mes)
					exploit_result.append(mes)
				else:
					output.expOut('Target %s fail'%url)
			except:
				break

	# 基于多线程的扫描
	def run(self):
		threads = []
		for i in range(threads_num):
			t = threading.Thread(target=self.scan)
			threads.append(t)
			t.start() 
		for t in threads:
			t.join()


	# report 导出
	def report(self,result,outfile):
		content = json.dumps(result, sort_keys=True, indent=4)
		with open(paths['REPORT_PATH']+outfile,'a') as f:
			f.write(content)



	def main(self):
		reload(sys)
		sys.setdefaultencoding("utf-8")
		'''
			exploit -s  -u 
			exploit -s -f 
			explit -l

			webdir -u (mode=0 thread, mode=1 gevent mode=2 thread+mulit)

			portscan -ip
			portscan -m -p 

		'''
		parser = argparse.ArgumentParser(usage="python s7scan.py [-h] {exploit,webdir,portscan} ...")
		#产生一个子命令解析器
		subparser = parser.add_subparsers(title=u'子命令',description=u"使用 's7star.py 子命令 -h' 获得子命令帮助")

		#使用子命令解析器去生成每一个子命令

		# exploit
		exploit = subparser.add_parser("exploit",help=u"Exploit系统，可自行添加POC, 批量执行exp",description=u'example: python s7scan.py exploit -s test -m 127.0.0.1/30')
		exploit.add_argument('-s',help=u"加载POC, 提供test测试poc")
		exploit.add_argument('-u',help=u"target url: 目标url")
		exploit.add_argument('-f',help=u"target file: 目标url文件")
		exploit.add_argument('-m',help=u"target mask: 目标网段,默认掩码为24")
		exploit.add_argument('-l','--list',help=u"列举所有的poc",default=False, action='store_true')  #store_true表示是布尔类型，不需要传值，只需要判断有无这个参数
		exploit.add_argument('-q',help=u"关键字搜索poc",default=False)
		exploit.add_argument('-o',help=u"导出json格式文件")
		exploit.set_defaults(func=self.Exploit)

		# webdir
		webdir = subparser.add_parser("webdir",help=u"敏感信息扫描",description=u"example:python s7scan.py webdir -u localhost")
		webdir.add_argument('-u',help="target url:目标url")
		webdir.add_argument('-o',help=u"导出json格式文件")
		webdir.set_defaults(func=self.webdir)
		# portscan
		portscan = subparser.add_parser("portscan",help=u"端口扫描",description=u"example:python s7scan.py portscan -t localhost")
		portscan.add_argument('-t',help=u"target ip 目标ip")
		portscan.add_argument('-m',help=u"mask(127.0.0.1/28 默认掩码为24)")
		portscan.add_argument('-p',help=u"port 目标端口",type=int)
		portscan.add_argument('-o',help=u"导出json格式文件")
		portscan.set_defaults(func=self.portscan)

		args = parser.parse_args()
		args.func(args)
