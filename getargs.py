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
st={
    'name':'_MhwsChina_',
    'uuid':'6512b7c6-2d53-4513-bb8f-d698143c939f',
    'token':'6512b7c6-2d53-4513-bb8f-d698143c939f'
}
d='.minecraft'

def fmarggame(txt,v,d,st,gamed,ver):#若在游戏左下角显示启动器名称就把v['type']改为启动器名称
    return txt.replace('${auth_player_name}',st['name'])\
        .replace('${version_name}',ver)\
        .replace('${game_directory}',gamed)\
        .replace('${assets_root}',pj(d,'assets'))\
        .replace('${assets_index_name}',v['assets'])\
        .replace('${auth_uuid}',st['uuid'])\
        .replace('${auth_access_token}',st['token'])\
        .replace('${user_type}','legacy')\
        .replace('${version_type}',v['type'])\
        .replace('${user_properties}','{}')\
        .replace('${game_assets}',pj(d,"assets/virtual/legacy"))\
        .replace('${auth_session}',st['token'])
def fmargjvm(txt,ver,d,cs):
    return txt.replace('${natives_directory}',pj(d,f'versions/{ver}/{ver}-natives'))\
        .replace('${launcher_name}','MhCraft')\
        .replace('${launcher_version}','1145149178')\
        .replace('${library_directory}',pj(d,'libraries'))\
        .replace('${classpath_separator}',cs)\
        .replace('${version_name}',ver)
def getargjvm(v,d,ver=None):
    args,cs=[],getcs()
    if not ver:ver=v['id']
    if not 'arguments' in v:return ["-Djava.library.path="+pj(d,f'versions/{ver}/{ver}-natives')]
    for jvm in v['arguments']['jvm']:
        try:
            jv,rules=jvm['value'],jvm['rules']
            if prules(rules):args.append(fmargjvm(jv,ver,d,cs))
        except:
            args.append(fmargjvm(jvm,ver,d,cs))
    return args
def getarggame(v,d,st,ver=None):
    if not ver:ver=v['id']
    args,gamed=[],pj(d,'versions',ver)
    if 'minecraftArguments' in v:
        ls,ls1,j=fmarggame(v['minecraftArguments'],v,d,st,gamed,ver).split(),[],''
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
        try:args.append(fmarggame(ag,v,d,st,gamed,ver))
        except KeyError:args.append(ag)
        except:pass #此处检测到非文本不直接退出为了适配pcl下载的json
    return args
def getcp(v,d,cps=[],ns=[],vs=[]):
    osn,ntd,arch=getosname(),pj(d,f'versions/{v["id"]}/{v["id"]}-natives'),str(findver(platform.architecture()[0]))
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
            if v1<v2:print(n,v);continue
        ns.append(n);vs.append(v)
        cps.append(pj(d,'libraries',p,n,v,file))
    return [cps,ns,vs]
def getarg(ver,d=d,st=st,args=['java','-Xmx2g','-Xms2g']):
    #java {jvm参数} -cp {classpath} {mainClass(主类名)} {游戏参数}
    v=readv(ver,d)
    vid,j,args=v['id'],v.get('javaVersion',{}),args+['-XX:+UseG1GC','-XX:+UnlockExperimentalVMOptions','-XX:G1NewSizePercent=20','-XX:G1ReservePercent=20','-XX:G1HeapRegionSize=32M','-XX:MaxGCPauseMillis=50','-XX:+PerfDisableSharedMem','-XX:MinHeapFreeRatio=25','-XX:MaxHeapFreeRatio=40','-XX:-UseAdaptiveSizePolicy','-XX:-OmitStackTraceInFastThrow']
    if 'inheritsFrom' in v:
        v1=readv(v['inheritsFrom'],d)
        vid,j,jvm,cp,game=v1['id'],v1['javaVersion'],getargjvm(v1,d,ver),getcp(v1,d,[],[]),(getarggame(v1,d,st,ver) if not 'minecraftArguments' in v else [])
    else:jvm,cp,game=[],[[],[],[]],[]
    jvm+=getargjvm(v,d,ver);cp=getcp(v,d,*cp);game+=getarggame(v,d,st,ver)
    if not '${classpath}' in jvm:jvm+=['-cp','${classpath}']
    if not '-p' in jvm:cp[0].append(pj(d,'versions',vid,vid+'.jar'))
    jvm=[getcs().join(cp[0]) if i=='${classpath}' else i for i in jvm]
    return args+jvm+[v['mainClass']]+game,j
