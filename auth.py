#第三方登录模块,作者_MhwsChina_
from tools import *
import base64
apiurl='https://littleskin.cn/api/yggdrasil'#api地址,默认littleskin
head={'Content-Type':'application/json; charset=utf-8'}
def getapiurl(url='https://littleskin.cn'):#获取api地址
    return req.get(url,timeout=100).headers['x-authlib-injector-api-location']
def login(email,password,apiurl=apiurl):
    data={'username':email,'password':password,'requestUser':True,'agent':{'name':'Minecraft','version':1}}
    return req.post(apiurl+'/authserver/authenticate/',json=data,headers=head).json()
def logout(email,password,apiurl=apiurl):
    data={'username':email,'password':password}
    return req.post(apiurl+'/authserver/signout/',json=data,headers=head)
def check(accesstoken,apiurl=apiurl):
    if req.post(apiurl+'/authserver/validate/',json={'accessToken':accesstoken},headers=head).status_code==204:return True
    else:return False
def refresh(accesstoken,apiurl=apiurl):
    return req.post(apiurl+'/authserver/refresh/',json={'accessToken':accesstoken,'requestUser':True},headers=head).json()
def delete(accesstoken,apiurl=apiurl):
    return req.post(apiurl+'/authserver/invalidate/',json={'accessToken':accesstoken,'requestUser':True},headers=head)
def fmapi(apiurl=apiurl):
    return base64.b64encode(req.get(apiurl,headers=head).content).decode()
def getjvm(jarp,apiurl=apiurl):
    return [f'-javaagent:{jarp}={apiurl}',f'-Dauthlibinjector.yggdrasil.prefetched={fmapi(apiurl)}']
def getprofile(uuid,apiurl=apiurl):
    return loads(base64.b64decode(req.get(apiurl+'/sessionserver/session/minecraft/profile/'+uuid,headers=head).json()['properties'][0]['value']))
