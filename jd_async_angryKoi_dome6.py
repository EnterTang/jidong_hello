'''
cron: 5 0 * * *
new Env('锦鲤助力码助力');
变量: jinglicodes
export jinglicodes=" 助力码1 & 助力码2 "
'&'符号连接,不填默认全部账号内部随机助力
'''

import os,json,random,time,re,string,functools,asyncio
import sys
import requests
import aiohttp
import socks  # pip install PySocks
from  multiprocessing import Pool
from urllib.parse import unquote, quote
requests.packages.urllib3.disable_warnings()
path_prefix=os.path.split(os.path.abspath(__file__))[0]


key=""
token=""
p=5    # 进程数
sleep=0
txtCookiePath="转换出来的cookie.txt"
sceneid='JLHBhPageh5'
# proxy
proxy_txt='''
'''
proxy_list=list()


cookie_findall=re.compile(r'pin=(.+?);')
def get_pin(cookie):
    try: return cookie_findall.findall(cookie)[0]
    except: print('ck格式不正确，请检查')
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
        if len(cookie_list)<1: print('请填写环境变量JD_COOKIE\n')    
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
def get_log(cookie,appid):
    url="http://121.4.99.83:5003/get_log"
    data={"appid": appid, "cookie": cookie, "key": key, "token": token}
    try:
        res=requests.post(url,json=data).json()
        if res['code']=='200':
            return res['randomnum'],res['log'],res['cookie'],res['ua']
        elif res['code']=="401":
            print('请求额度已空')
            exit()
        elif res['code']=="402":
            print('token已过期')
            exit()
        else:
            print('已拉黑')
            exit()
    except Exception as e:
        print(e)
        return None,None,None,None
    
    
# 返回 txtCookie
def get_txtcookie():
    with open(f'{path_prefix}/{txtCookiePath}','r') as f:
        txtCookie=f.read().replace('\r','')
    return txtCookie.split('\n') 


async def taskPostUrl(functionId, body, cookie, ua):
    data=f"body={body}"
    url=f'https://api.m.jd.com/api?appid=jinlihongbao&functionId={functionId}&loginType=2&client=jinlihongbao&t={gettimestamp()}&clientVersion=10.3.0&osVersion=-1'
    headers={
        'Cookie': cookie,
        "content-length": str(len(data)),
        "accept": "application/json, text/plain, */*",
        "origin": "https://happy.m.jd.com",
        "user-agent": ua,
        "sec-fetch-mode": "cors",
        "content-type": "application/x-www-form-urlencoded",
        "x-requested-with": "com.jingdong.app.mall",
        "sec-fetch-site": "same-site",
        "referer": "https://happy.m.jd.com/babelDiy/zjyw/3ugedFa7yA6NhxLN5gw2L3PF9sQC/index.html?channel=9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    try:
        async with session.post(url, headers=headers, data=data, timeout=3) as res:
            res =await res.text(encoding="utf-8")
        return res
    except:
        print('API请求失败，请检查网路重试❗\n')  
        
        
def taskPostUrl_2(functionId, body, cookie, proxy, ua):
    proxies = {'http': proxy, 'https': proxy}
    data=f"body={body}"
    url=f'https://api.m.jd.com/api?appid=jinlihongbao&functionId={functionId}&loginType=2&client=jinlihongbao&t={gettimestamp()}&clientVersion=10.3.0&osVersion=-1'
    headers={
        'Cookie': cookie,
        "content-length": str(len(data)),
        "accept": "application/json, text/plain, */*",
        "origin": "https://happy.m.jd.com",
        "user-agent": ua,
        "sec-fetch-mode": "cors",
        "content-type": "application/x-www-form-urlencoded",
        "x-requested-with": "com.jingdong.app.mall",
        "sec-fetch-site": "same-site",
        "referer": "https://happy.m.jd.com/babelDiy/zjyw/3ugedFa7yA6NhxLN5gw2L3PF9sQC/index.html?channel=9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    try:
        if proxy:
            res=requests.post(url, headers=headers, proxies=proxies, data=data, timeout=3).text
        else:
            res=requests.post(url, headers=headers, data=data, timeout=3).text
        return res
    except:
        # print('API请求失败，请检查网路重试❗\n')  
        pass


# 开启助力
code_findall=re.compile(r'"code":(.*?),')
async def h5launch(cookie,n=0):
    randomnum,log,cookie,ua=get_log(cookie,'50087_help')
    body={"followShop":0,"random":randomnum,"log":log,"sceneid":sceneid}
    res=await taskPostUrl("h5launch", quote(json.dumps(body)), cookie, ua)
    if not res:
        if n<5:
            n+=1
            return await h5launch(cookie,n)
    if Code:=code_findall.findall(res):
        if str(Code[0])=='0':
            print(f"账号 {get_pin(cookie)} 开启助力码成功\n")
        else:
            print(f"账号 {get_pin(cookie)} 开启助力码失败")
            print(res)
            if n<5:
                n+=1
                return await h5launch(cookie,n)
    else:
        print(f"账号 {get_pin(cookie)} 开启助力码失败")
        print(res)
        if n<5:
            n+=1
            return await h5launch(cookie,n)


# 获取助力码
id_findall=re.compile(r'","id":(.+?),"')
async def h5activityIndex(cookie,n=0):
    global inviteCode_list
    randomnum,log,cookie,ua=get_log(cookie,'50087')
    body={"isjdapp":1}
    res=await taskPostUrl("h5activityIndex", quote(json.dumps(body)), cookie, ua)
    if not res:
        print(f"账号 {get_pin(cookie)} 获取助力码失败\n")
        if n<5:
            n+=1
            return await h5activityIndex(cookie,n)
    if inviteCode:=id_findall.findall(res):
        inviteCode=inviteCode[0]
        inviteCode_list.append(inviteCode)
        print(f"账号 {get_pin(cookie)} 的锦鲤红包助力码为 {inviteCode}\n")
    else:
        print(f"账号 {get_pin(cookie)} 获取助力码失败\n")
        if n<5:
            n+=1
            return await h5activityIndex(cookie,n)

# 助力
re_cookie_joyytoken=re.compile(r'joyytoken=.*?;') 
statusDesc_findall=re.compile(r',"statusDesc":"(.+?)"')
def jinli_h5assist(cookie,inviteCode,n=0):
    global cookie_list_2
    
    try:
        if cookie in cookie_list_2:
            cookie_list_2.remove(cookie)
            with open(f'{path_prefix}/转换出来的cookie.txt','w',encoding='utf-8') as f:
                f.write('\n'.join(cookie_list_2))
    except Exception as e:
        print(f"移除cookie失败{e}")  
            
    try:
        time.sleep(sleep)
        global okcookie_list,inviteCode_num,okproxy_set
        randomnum,log,cookie,ua=get_log(cookie,'50087_help')
        joyytoken=re_cookie_joyytoken.findall(cookie)
        if joyytoken:
            cookie.replace(joyytoken[0],'joyytoken=;')
        body={"redPacketId":inviteCode,"followShop":0,"random":randomnum,"log":log,"sceneid":sceneid}
        if proxy_list: proxy=random.choice(proxy_list)
        else: proxy=None
        res=taskPostUrl_2("jinli_h5assist", quote(json.dumps(body)), cookie, proxy, ua)
        if n==0:
            print(f'账号 {get_pin(cookie)} 去助力{inviteCode}')
        if not res:
            if proxy:
                print(f"代理 {proxy} 连接波动,请求失败")
            else:
                print('网络连接失败')
            sys.stdout.flush()
            if n<10:
                n+=1
                return jinli_h5assist(cookie,inviteCode,n)
        if statusDesc:=statusDesc_findall.findall(res):
            statusDesc=statusDesc[0]
            print(f"{statusDesc}\n")
            if "火爆" not in statusDesc:
                okcookie_list.append(cookie)
                with open(f'{path_prefix}/锦鲤助力成功的pin.txt','a',encoding='utf-8') as f:
                    f.write(f'{cookie}\n')
            if "助力已满" in statusDesc:
                inviteCode_num[inviteCode]=True
        else:
            if '406' in res or '403' in res:
                print(f"错误\n{res}")
                sys.stdout.flush()
                if n<10:
                    n+=1
                    return jinli_h5assist(cookie,inviteCode,n)
        if proxy:
            okproxy_set.add(proxy)
            with open(f'{path_prefix}/锦鲤连接成功的proxy.txt','a',encoding='utf-8') as f:
                f.write(f'{proxy}\n')
        sys.stdout.flush()
    except Exception as e:
        print(f"代理 {proxy} 连接波动,请求失败")
        sys.stdout.flush()
        if n<10:
            n+=1
            return jinli_h5assist(cookie,inviteCode,n)
        

# 开红包
biz_msg_findall=re.compile(r'"biz_msg":"(.*?)"')
discount_findall=re.compile(r'"discount":"(.*?)"')
def h5receiveRedpacketAll(cookie,n=0):
    randomnum,log,cookie,ua=get_log(cookie,'50087')
    body={"random":randomnum,"log":log,"sceneid":sceneid}
    if proxy_list: proxy=random.choice(proxy_list)
    else: proxy=None
    res=taskPostUrl_2("jinli_h5assist", quote(json.dumps(body)), cookie, proxy, ua)
    print(f'账号 {get_pin(cookie)} 开红包')
    if not res: 
        if n<5:
            n+=1
            return h5receiveRedpacketAll(cookie)
    try:
        biz_msg=biz_msg_findall.findall(res)[0]
    except:
        print(res)
        return
    if '火爆' in res:
        if n<5:
            n+=1
            return h5receiveRedpacketAll(cookie,n)
    elif discount:=discount_findall.findall(res):
        discount=discount[0]
        print(f"恭喜您，获得红包 {discount}\n")
        return h5receiveRedpacketAll(cookie)
    else:
        print(f"{biz_msg}\n")


def Pool_jinli_h5assist(cookie_list_dome,inviteCode_list):
    global okcookie_list,okproxy_set
    okcookie_list=list()
    okproxy_set=set()
    if not inviteCode_list:return
    num=len(cookie_list_dome)//len(inviteCode_list)+1
    random.shuffle(inviteCode_list)
    for e,inviteCode in enumerate(inviteCode_list):      
        cookie_list_dome2=cookie_list_dome[num*e:num*(e+1)]
        for f,cookie in enumerate(cookie_list_dome2):
            if f%7==0 and f!=0:
                print("暂停10s\n")
                time.sleep(10)
            jinli_h5assist(cookie,inviteCode)
            if inviteCode_num[inviteCode]:
                print(f'{inviteCode} 助力已满跳过\n')
                cookie_list_dome3=list(set(cookie_list_dome[num*e:])-set(cookie_list_dome2[:f]))
                return Pool_jinli_h5assist(cookie_list_dome3,inviteCode_list[e+1:])
    # with open(f'{path_prefix}/锦鲤助力成功的pin.txt','a',encoding='utf-8') as f:
    #     f.write('\n')
    #     f.write('\n'.join(okcookie_list))
    # with open(f'{path_prefix}/锦鲤连接成功的proxy.txt','a',encoding='utf-8') as f:
    #     f.write('\n')
    #     f.write('\n'.join(okproxy_set))

async def async_main():
    print('🔔愤怒的锦鲤，开始! \n')
    print(f'====================共{len(cookie_list)}京东个账号Cookie=========\n')

    # debug_pin=get_env('kois')
    # if debug_pin:
    #     cookie_list_1=[cookie for cookie in cookie_list if get_pin(cookie) in debug_pin]
    # else:
    #     cookie_list_1=cookie_list
    global inviteCode_list,session,cookie_list_2,inviteCode_num
    inviteCode_list=list()
    cookie_list_2=cookie_list
    inviteCode_list=get_env('jinglicodes').split('&')
    inviteCode_num={inviteCode:False for inviteCode in inviteCode_list}
    

    async with aiohttp.ClientSession() as session:

        # print('***************************开启助力码***************\n')
        # tasks=[h5launch(cookie) for cookie in cookie_list_1]
        # await asyncio.wait(tasks)

        # print('***************************获取助力码***************\n')
        # tasks=[h5activityIndex(cookie) for cookie in cookie_list_1]
        # await asyncio.wait(tasks)

        if not inviteCode_list:
            print('没有需要助力的锦鲤红包助力码\n')
        else:
            print('*******************助力**************************\n')
            num=len(cookie_list_2)//p+1
            pool = Pool(p)
            for e in range(p):
                cookie_list_dome=cookie_list_2[num*e:num*(e+1)]
                pool.apply_async(func=Pool_jinli_h5assist,args=(cookie_list_dome,inviteCode_list))    
                # Pool_jinli_h5assist(cookie_list_dome,inviteCode_list)   
            pool.close()
            pool.join()

        # print('*******************开红包**************************\n')
        # [h5receiveRedpacketAll(cookie) for cookie in cookie_list_1]
        

def main():    
    with open(f'{path_prefix}/锦鲤助力成功的pin.txt','w',encoding='utf-8') as f:
        pass
    with open(f'{path_prefix}/锦鲤连接成功的proxy.txt','w',encoding='utf-8') as f:
        pass
    asyncio.run(async_main())
    

if __name__ == '__main__':
    main()
