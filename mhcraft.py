from getargs import *
from dl import *
from java import *
from files import *
from ml import *
if os.path.exists('mhl'):
    try:shutil.remove('mhl')
    except:pass
mkdir('mhc')
dl=xcdl()
getd=lambda:getjs(('d','.minecraft'))
def getname():
    if not getjs('name'):return getjs(('name',input('请输入游戏名:').replace(' ','')))
    else:return getjs('name')
getuuid=lambda:getjs(('uuid',caluuid(getname())))
gettoken=lambda:getjs(('token',getuuid()))
getst=lambda:{
    'name':getname(),
    'uuid':getuuid(),
    'token':gettoken()
}
getmem=lambda:['java','-Xmx'+getjs(('mem','2g')),'-Xms'+getjs(('mem','2g'))]
getth=lambda:int(getjs(('thread',256)))
getu=lambda:'bmclapi2.bangbang93.com'
getisu=lambda:int(getjs(('isu',1)))
getrpl=lambda:((getu()+'/maven',getu()+'/assets') if getisu() else ('',''))
getrp=lambda:getu() if getisu() else ''
getbq=lambda:int(getjs(('deepbq',0)))
mkdir(getd(),'versions')
def getln(txt,typ=str,n=None,ls=[],err='输入不正确,请重新输入!'):
    while True:
        tmp=input(txt)
        if not tmp and n!=None:
            return n
        if not tmp in ls and ls!=[]:
            print(err)
            continue
        try:return typ(tmp)
        except:print(err)
def getjava(java):
    global jd,dl
    try:return jd[java['majorVersion']]
    except:
        dl.dls+=getjavaf(java['component'],rp=getrp())
        dl.start(getth())
        dl.join()
        jd=findjava('mhc')
        return jd[java['majorVersion']]
def movemc(v1,v2):
    print('转移版本',v1,'->',v2)
    p=pj(getd(),'versions')
    mkdir(pj(p,v2))
    shutil.copytree(pj(p,v1),pj(p,v2),dirs_exist_ok=True)
    removemc(v1)
    try:os.remove(pj(p,v2,v1+'.json'))
    except:pass
    try:os.remove(pj(p,v2,v1+'.jar'))
    except:pass
def fabric(ver):
    oldv,tag=ver,0
    try:ver,nv=fvanilla(vd,readv(ver,getd())['id']);nv=findver(nv)        
    except:pass
    lt=fabric_latestloader()
    try:
        print(ver,nv)
        input()
        if nv==findver(lt):print('已是最新版!');return
        else:print('发现更新',lt);tag=1;
    except:pass
    print('正在安装fabric',ver)
    v=instfabric(ver,lt)
    if tag:
        print('正在转移文件到新版本')
        movemc(oldv,v)
    print(v,'安装完成')
def forge(ver):
    oldv,tag=ver,0
    try:ver,nv=fvanilla(vd,readv(ver,getd())['id']);nv=findver(nv)        
    except:pass
    print('正在安装forge',ver)
    url,fgv=forge_inst_url(ver)
    try:
        if nv==fmmln(vd,fgv):print('已是最新版!');return
        else:print('发现更新',fgv);tag=1
    except:pass
    if getisu():url=url.replace('files.minecraftforge.net',getu())
    instp=pj('mhc/forge','forge'+fgv+'.jar')
    if not os.path.exists(instp):print('下载',url);dlurl(url,instp)
    lzp,dc,v=instforge_part1(instp,getd())
    #if not lzp:print('已经安装过该版本的forge且是最新版!');return
    if 'libraries' in dc:bqwj(v,v=dc)
    bqwj(v)
    java=getjava({'component':'java-runtime-gamma','majorVersion':17})
    instforge_part2(lzp,dc,v,instp,java,getd())
    if tag:
        print('正在转移文件到新版本')
        movemc(oldv,v)
    print(v,'安装完成')
def runmc(ver):
    print('正在补全文件')
    bqwj(ver,getbq())
    args,jv=getarg(ver,getd(),getst(),getmem())
    java=getjava(jv)
    args[0]=java
    sub.run(args)
    print(ver,'已关闭')
def dlmc(ver):
    dl.dls+=dlver(vd,ver,getd(),*getrpl())
    dl.start(getth())
    print(ver,'下载完毕')
def bqwj(ver,chsha1=1,v=None):
    dl.dls+=dlver(vd,ver,getd(),*getrpl(),v=v)
    dl.start(getth(),chsha1)
    print(ver,'补全完毕')
def scv():
    vers=os.listdir(pj(getd(),'versions'))
    j=1
    for i in vers:
        print(j,i);j+=1
    return vers[getln('请选择版本序号:',int,'')-1]
def lsav():
    print('\n1.下载最新版\n2.手动选择版本')
    if getln('请选择序号:',int,['1','2'])==1:
        print('\n1.正式版\n2.快照版')
        return vd['latest'][{'1':'release','2':'snapshot'}[getln('请选择序号',str,['1','2'])]]
    else:
        print('\n1.正式版\n2.快照版\n3.远古版')
        t={'1':'release','2':'snapshot','3':'old'}[getln('请选择序号',str,['1','2','3'])]
        print('所有版本:',' / '.join([i['id'] for i in findv(vd,t)[::-1]]))
        return input('请输入要下载的版本:')
def setst(a,b):
    if not a:return
    print('set',a,'to',b)
    setjs((a,b))
    updatejs(getjs())
def listst():
    t={'name':'游戏名','mem':'游戏运行内存','d':'mc文件夹','thread':'下载线程数','isu':'是否使用国内源下载加速(1表示是,0表示否)',
       'deepbq':'补全文件是否检查文件sha1(1表示是,0表示否)'
    }
    fm={'mem':lambda x:fmbt(int(x)),'thread':int,'isu':lambda x:int(int(x) and 1),'deepbq':lambda x:int(int(x) and 1)}
    ls,ls1=getjs(),[]
    j=1
    for n in getjs():
        try:print(j,t[n],'(',n,')');ls1.append(n);j+=1
        except:continue
    sst=ls1[getln('请选择要设置的序号:',lambda a:abs(int(a)),'')-1]
    z=getln(f'请输入设置成什么?(留空为{getjs(sst)})',(fm[sst] if sst in fm else str),'')
    if z=='':return None,None
    return sst,z
def removemc(ver):
    d=getd()
    libs=listlib(d)
    for i in libs:
        if libs[i]==[ver]:
            path=pj(d,i)
            try:os.remove(path);print('删除',path)
            except Exception as ex:print('删除失败:',ex)
    libs,ass=None,listass(d)
    for i in ass:
        if ass[i]==[ver]:
            path=pj(d,'assets/objects',i[0:2],i)
            try:os.remove(path);print('删除',path)
            except Exception as ex:print('删除失败:',ex)
    shutil.rmtree(pj(d,'versions',ver))
    print(ver,'删除完毕')
psnone=lambda *a:None
hlp=lambda *a:print('帮助:\n你可以在该窗口输入指令\n启动游戏:r,下载游戏:d,设置:s,删除版本:rm,帮助:h,深度补全文件:b,安装/更新/更改mod加载器为fabric:f,安装/更新/更改mod加载器为forge:fg,退出:e\n警告:更新fabric或forge请选择安装过fabric或forge的版本,否则会重新安装',mode='WARN')
commands={
    'r':(runmc,scv),#指令:(函数,没有参数调用的函数)
    'd':(dlmc,lsav),
    's':(setst,listst),
    'h':(hlp,psnone),
    'rm':(removemc,scv),
    'b':(bqwj,scv),
    'f':(fabric,scv),
    'fg':(forge,scv),
    'fabric':'f',
    'forge':'fg',
    'run':'r',
    'dl':'d',
    'download':'d',
    'set':'s',
    'help':'h',
    'bq':'b',
    'exit':(sys.exit,sys.exit),
    'e':'exit'
}
print('MhCraft b1.0  _MhwsChina_制作');print('正在加载配置...')
getmem();getth();getrpl();getst();getbq();updatejs(getjs())
if not os.path.exists(pj(getd(),'launcher_profiles.json')):
    with open(pj(getd(),'launcher_profiles.json'),'w') as f:
        f.write('{"clientToken":"","profiles":{},"selectedProfile":""}')
if getjs('isu'):vdurl='https://'+getu()+'/mc/game/version_manifest.json'
else:vdurl='http://launchermeta.mojang.com/mc/game/version_manifest.json'
vd,jd=urljson(vdurl),findjava('mhc')
hlp();print('你的游戏名:',getname())
def parcmd():
    global arg
    if not arg[0] in commands:
        return os.system(' '.join(arg))
    cmd=commands[arg[0]]
    if type(cmd)==str:
        arg[0]=cmd
        return parcmd()
    arg1=arg[1:]
    if not arg1:
        arg1=cmd[1]()
        if type(arg1)!=tuple:arg1=(arg1,)
    cmd[0](*arg1)
_txt='>'
while 1:
    try:
        arg=input(_txt).split()
        _txt=_txt or '>'
        if not arg:continue
    except:_txt='';continue
    try:parcmd()
    except Exception as s:pass;print(s,mode='ERROR')
