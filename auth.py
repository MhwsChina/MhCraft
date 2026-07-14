#登录,作者_MhwsChina_
from tools import *
import base64
head={'Content-Type':'application/json; charset=utf-8'}
#class thirdauth:#第三方登录模块
apiurl='https://littleskin.cn/api/yggdrasil'#api地址,默认littleskin
def getapiurl(url='https://littleskin.cn'):#获取api地址
    return req.get(url,timeout=100,verify=False).headers['x-authlib-injector-api-location']
def login(email,password,apiurl=apiurl):
    data={'username':email,'password':password,'requestUser':False,'agent':{'name':'Minecraft','version':1}}
    return req.post(apiurl+'/authserver/authenticate/',json=data,headers=head,verify=False).json()
def logout(email,password,apiurl=apiurl):
    data={'username':email,'password':password}
    return req.post(apiurl+'/authserver/signout/',json=data,headers=head,verify=False)
def check(accesstoken,apiurl=apiurl):
    if req.post(apiurl+'/authserver/validate/',json={'accessToken':accesstoken},headers=head,verify=False).status_code==204:return True
    else:return False
def refresh(accesstoken,apiurl=apiurl):
    return req.post(apiurl+'/authserver/refresh/',json={'accessToken':accesstoken,'requestUser':True},headers=head,verify=False).json()
def delete(accesstoken,apiurl=apiurl):
    return req.post(apiurl+'/authserver/invalidate/',json={'accessToken':accesstoken,'requestUser':True},headers=head,verify=False)
def fmapi(apiurl=apiurl):
    return base64.b64encode(req.get(apiurl,headers=head,verify=False).content).decode()
def getjvm(jarp,apiurl=apiurl):
    return [f'-javaagent:{jarp}={apiurl}',f'-Dauthlibinjector.yggdrasil.prefetched={fmapi(apiurl)}']
def getprofile(self,uuid,apiurl=apiurl):
    return loads(base64.b64decode(req.get(apiurl+'/sessionserver/session/minecraft/profile/'+uuid,headers=head,verify=False).json()['properties'][0]['value']))
class microsoftauth:#微软登录模块
    pass
###################第三方登录模块说明###################
'''
----------需知----------
一般情况下，若操作失败或请求不成功服务器会返回以下结果
{
    "error":"错误的简要描述（机器可读）",
    "errorMessage":"错误的详细信息（人类可读）",
    "cause":"该错误的原因（可选）"
}
----------添加账户流程----------
1.获取email和password和登陆服务器api地址
2.添加账户
    1.运行thirdauth.login(email,password,登陆服务器api地址)
    2.若请求不成功，则报错退出流程，否则继续执行:
    3.若账户正常且服务器正确可用，可获得以下结果:
    {
        'accessToken'(需保存): 玩家的token,
        'clientToken'(无需保存): 玩家的clienttoken,
        'availableProfiles'(玩家创建的所有角色): [
            {'id':该角色的uuid,'name':该角色的游戏名},
            {'id':该角色的uuid,'name':该角色的游戏名},
            ......（省略）
        ]
        'selectedProfile'(玩家当前选择的角色): {'id':该角色的uuid,'name':该角色的游戏名},
    }
    4.若availableProfiles为空，则没有创建过角色，报错退出流程，否则继续执行
    5.若availableProfiles内只有一个角色，直接添加，退出流程，否则继续执行
    6.若availableProfiles内有多个角色，让玩家选一个添加或全部添加
----------启动游戏流程(LittleSkin)----------   
1.验证账户
    1.运行thirdauth.check(角色的token,服务器api地址)
    2.若请求成功，退出流程，否则为继续执行
    3.运行thirdauth.refresh(角色的token,服务器api地址)，获得新的token
    4.若获取成功，退出流程
    5.运行thirdauth.login(email,password,服务器api地址)
    6.保存token
    7.从availableProfiles中找到和该角色uuid相同的角色并使用
    8.找不到的话报错退出
2.启动游戏
    1.下载authlib-injector
    2.添加额外的JVM参数(加在主类前)
        1.运行thirdauth.getjvm(authlib-injector的路径,服务器api地址)
        2.若没有报错，把运行结果添加进jvm
    3.替换参数
        把${auth_access_token}或${auth_session}替换为角色的token
        把${auth_uuid}替换为角色的uuid
        把${user_type}替换为mojang
    4.完成启动
----------其他功能示例----------
1.thirdauth.getprofile(角色的uuid,服务器api地址)
返回结果:
{
    'timestamp':角色创建日期(没用),
    'profileId':角色的id(没用),
    'profileName':角色名称(可能有用),
    'textures'(可能有用):{
        'SKIN':{
            {'url':皮肤下载地址,'metadata':{'model':手臂粗细)}}
        },
        'CAPE'(有些角色没有):{
            {'url':披风下载地址}
        }
    }
}
'''
