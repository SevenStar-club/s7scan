#!/usr/bin/env python
# __author__= 'w8ay'
import os
import sys
import Queue
import time
import requests
import gevent
from gevent import monkey,pool
monkey.patch_all()


class webdir:
    def __init__(self,root,threadNum):
        self.root = root
        self.threadNum = threadNum
        self.headers = {
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
             'Referer': 'http://www.shiyanlou.com',
             'Cookie': 'whoami=w8ay',
             }
        self.s_list = []
        self.links = []
        #filename = os.path.join('/home/pytool/Scaner/w8ay/shiyanlouscan7/shiyanlouscan/data', "dir.txt")
        filename = '/home/pytool/dirsearch-master/db/dicc.txt'
        for line in open(filename):  
            self.links.append(line.strip())
    
    def checkdir(self,url):
        status_code = 0
        try:
            r = requests.head(url,headers=self.headers,timeout=3)
            status_code = r.status_code
        except:
            status_code = 0
        return status_code

    def test_url(self,path):
        url = self.root+path
        s_code = self.checkdir(url)
        if s_code==200:
            self.s_list.append(url)
        print "Testing: %s status:%s"%(path,s_code)
    
    def work(self):
        start = time.time()
        p = pool.Pool(self.threadNum)
        pools = []
        for link in self.links:
            pools.append(p.spawn(self.test_url,link))
        
        gevent.joinall(pools)
        print('[*] The DirScan is complete!')
        print 'use time:',time.time()-start

    def output(self):
        if len(self.s_list):
            print "[*] status = 200 dir:"
            for url in self.s_list:
                print url



if __name__ == '__main__':
    scan = webdir('http://116.62.63.190:8080/ee00f46afe33f2ff/web6/',50)
    scan.work()
