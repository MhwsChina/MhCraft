#变量v:版本json 位置通常在.minecraft/versions/版本号/版本号.json
#变量d:mc地址 默认.minecraft
#变量cp:classpaths
#变量st:玩家信息
#游戏启动参数: {java路径} {jvm参数} {主类名} {游戏参数}
#jvm参数最后应是 -cp {游戏库+主文件}
#若有mod加载器,mod加载器的json优先原版
#比如classpath先遍历加载器,在末尾接上原版json
#jvm参数也一样
from tools import *
d='.minecraft'

def fmarggame(txt,v,d,st,gamed,ver,abspath=0):#若在游戏左下角显示启动器名称就把v['type']改为启动器名称
    return txt.replace('${auth_player_name}',st['name'])\
        .replace('${version_name}',ver)\
        .replace('${game_directory}',pj(gamed,abspath=abspath))\
        .replace('${assets_root}',pj(d,'assets',abspath=abspath))\
        .replace('${assets_index_name}',v['assets'])\
        .replace('${auth_uuid}',st['uuid'])\
        .replace('${auth_access_token}',st['token'])\
        .replace('${user_type}',st['type'] if 'type' in st else 'legacy')\
        .replace('${version_type}',v['type'] if 'type' in v else 'MhCraft')\
        .replace('${user_properties}','{}')\
        .replace('${game_assets}',pj(d,"assets/virtual/legacy",abspath=abspath))\
        .replace('${auth_session}',st['token'])
def fmargjvm(txt,ver,d,cs,abspath=0):
    return txt.replace('${natives_directory}',pj(d,f'versions/{ver}/{ver}-natives',abspath=abspath))\
        .replace('${launcher_name}','MhCraft')\
        .replace('${launcher_version}','1145149178')\
        .replace('${library_directory}',pj(d,'libraries',abspath=abspath))\
        .replace('${classpath_separator}',cs)\
        .replace('${version_name}',ver)
def getargjvm(v,d,ver=None,abspath=0):
    args,cs=[],getcs()
    if not ver:ver=v['id']
    if not 'arguments' in v:
        if 'minecraftArguments' in v:return ["-Djava.library.path="+pj(d,f'versions/{ver}/{ver}-natives',abspath=abspath)]
        else:return []
    for jvm in v['arguments']['jvm']:
        try:
            jv,rules=jvm['value'],jvm['rules']
            if prules(rules):
                if type(jv)==list:args+=jv
                else:args.append(jv)
        except:
            args.append(fmargjvm(jvm,ver,d,cs,abspath=abspath))
    return args
def getarggame(v,d,st,ver=None,abspath=0):
    if not ver:ver=v['id']
    args,gamed=[],pj(d,'versions',ver)
    if 'minecraftArguments' in v:
        ls,ls1,j=fmarggame(v['minecraftArguments'],v,d,st,gamed,ver,abspath=abspath).split(),[],''
        for i in ls:
            if i[0]=='-':
                if j:ls1.append(j);j=''
                ls1.append(i)
            else:
                if j:j+=' '
                j+=i
        if j:ls1.append(j)
        return ls1
    if not 'arguments' in v:return []
    for ag in v['arguments']['game']:
        try:args.append(fmarggame(ag,v,d,st,gamed,ver,abspath=abspath))
        except KeyError:args.append(ag)
        except:pass #此处检测到非文本不直接退出为了适配pcl下载的json
    return args
def getcp(v,d,ver=None,abscp=0,cps=[],ns=[],vs=[]):
    if not ver:ver=v['id']
    osn,ntd,arch=getosname(),pj(d,f'versions/{ver}/{ver}-natives'),str(findver(platform.architecture()[0]))
    for l in v['libraries']:
        if 'rules' in l and not prules(l['rules']):continue
        if 'downloads' in l and 'classifiers' in l['downloads']:
            nt=l['natives'][osn].replace('${arch}',arch)
            path=pj(d,'libraries',l['downloads']['classifiers'][nt]['path'])
            extzfa(path,ntd)
            if not 'actrifact' in l['downloads']:continue
        p,n,v,file=fmname(l['name'])
        if ns and n in ns:
            ind=ns.index(n)
            v1,v2=findver(v),findver(vs[ind])
            if v1>v2:
                print('del',cps[ind])
                del cps[ind],vs[ind],ns[ind]
            if v1<v2:print('skip',n,v);continue
        ns.append(n);vs.append(v)
        cps.append(pj(d,'libraries',p,n,v,file,abspath=abscp))
    return (cps,ns,vs)
def getarg(ver,st,d=d,args=['java','-Xmx2g','-Xms2g'],abspath=False):
    #java {jvm参数} -cp {classpath} {mainClass(主类名)} {游戏参数}
    v=readv(ver,d)
    vid,j,args=v['id'],v.get('javaVersion',{}),args+['-XX:+UseG1GC','-XX:-UseAdaptiveSizePolicy','-XX:-OmitStackTraceInFastThrow','-Djdk.lang.Process.allowAmbiguousCommands=true','-Dlog4j2.formatMsgNoLookups=true']
    if 'inheritsFrom' in v:
        v1=readv(v['inheritsFrom'],d)
        vid,j,jvm,cp,game=v1['id'],v1['javaVersion'],getargjvm(v1,d,ver,abspath),getcp(v1,d,ver,abspath,[],[],[]),(getarggame(v1,d,st,ver,abspath) if not 'minecraftArguments' in v else [])
    else:jvm,cp,game=[],[[],[],[]],[]
    jvm+=getargjvm(v,d,ver,abspath);cp=getcp(v,d,ver,abspath,*cp);game+=getarggame(v,d,st,ver,abspath)
    if '${classpath}' not in jvm:jvm+=['-cp','${classpath}']
    if '-p' not in jvm:cp[0].append(pj(d,'versions',vid,vid+'.jar',abspath=abspath))
    jvm=[getcs().join(cp[0]) if i=='${classpath}' else i for i in jvm]
    return args+jvm+[v['mainClass'] if 'mainClass' in v else v1['mainClass']]+game,j
'''
getarg函数说明
用法:
    getarg(mc版本,玩家信息,mc目录,附加启动参数,是否使用完整路径)
返回:
    格式:列表
参数说明:
    必填:
        mc版本:要启动的mc版本,通常位于"mc目录/versions"下
        玩家信息:
            格式:{'name':玩家名,'uuid':玩家uuid,'token':玩家的登录token,'type':'legacy'}
            'type'为选填选填,即玩家类型,不填即为legacy,legacy表示离线,mojang为第三方用户,microsoft为正版微软用户
            uuid格式详细见https://zh.minecraft.wiki/w/%E9%80%9A%E7%94%A8%E5%94%AF%E4%B8%80%E8%AF%86%E5%88%AB%E7%A0%81?variant=zh-cn
            token格式自己去搜
            玩家名必须为长度不少于1的字符串
    选填:
        mc目录:字符串,默认为".minecraft"
        附加启动参数:
            条件:不能为空,其中第一项必须为java路径
            格式:列表,默认为['java','-Xmx2g','-Xms2g']
        是否使用完整路径:
            格式:布尔值(即为True或False)
            示例1:(程序位于C:\\Users\\Admin\\mc)
                若为True:
                    C:\\Users\\Admin\\mc\\.minecraft\\versions
                若为False:
                    .minecraft/version
            示例2:(程序位于C:\\Users\\Admin)
                若为True:
                    C:\\Users\\Admin\\mc\\.minecraft\\libraries\\org
                若为False:
                    mc/.minecraft/libraries/org
            示例3:(程序位于C:\\Users\\Admin\\mc)
                若为True:
                    C:\\Users\\Admin\\mc\\.minecraft\\libraries\\org
                若为False:
                    .minecraft/libraries/org
示例代码(启动1.20.1版本):
import subprocess
st={
    'name':'sb123',
    'uuid':'e594f0aec20001c6002e878f3ec63c62',
    'token':'e594f0aec20001c6002e878f3ec63c62'
}
java='./mhc/java/17.0.15/bin/java.exe'
args=getarg('1.20.1',st)
args[0]=java
subprocess.run(args)
'''
