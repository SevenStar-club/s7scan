# s7scan


### 安装依赖
pip install -r requirements.txt 

### Usage
```
usage: python s7scan.py [-h] {exploit,webdir,portscan} ...

optional arguments:
  -h, --help            show this help message and exit

子命令:
  使用 's7star.py 子命令 -h' 获得子命令帮助

  {exploit,webdir,portscan}
    exploit             Exploit系统，可自行添加POC, 批量执行exp
    webdir              敏感信息扫描
    portscan            端口扫描
```


### 各个功能

#### exploit 

```
usage: python s7scan.py [-h] {exploit,webdir,portscan} ... exploit
       [-h] [-s S] [-u U] [-f F] [-m M] [-l] [-q Q] [-o O]

example: python s7scan.py exploit -s test -m 127.0.0.1/30

optional arguments:
  -h, --help  show this help message and exit
  -s S        加载POC, 提供test测试poc
  -u U        target url: 目标url
  -f F        target file: 目标url文件
  -m M        target mask: 目标网段,默认掩码为24
  -l, --list  列举所有的poc
  -q Q        关键字搜索poc
  -o O        导出json格式文件
```

#### webdir 
```
usage: python s7scan.py [-h] {exploit,webdir,portscan} ... webdir
       [-h] [-u U] [-o O]

example:python s7scan.py webdir -u localhost

optional arguments:
  -h, --help  show this help message and exit
  -u U        target url:目标url
  -o O        导出json格式文件
```


#### portscan 
```
usage: python s7scan.py [-h] {exploit,webdir,portscan} ... portscan
       [-h] [-t T] [-m M] [-p P] [-o O]

example:python s7scan.py portscan -t localhost

optional arguments:
  -h, --help  show this help message and exit
  -t T        target ip 目标ip
  -m M        mask(127.0.0.1/28 默认掩码为24)
  -p P        port 目标端口
  -o O        导出json格式文件
```

