import re,platform,sys,zipfile,os,hashlib
import requests as req
import subprocess as sub
from json import loads,dumps
req.urllib3.disable_warnings()
hd={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0','Accept-Encoding': 'br'}
def movemc(v1,v2,d):
    print('转移版本',v1,'->',v2)
    p=pj(d,'versions')
    try:os.remove(pj(p,v1,v1+'.json'))
    except:pass
    try:os.remove(pj(p,v1,v1+'.jar'))
    except:pass
    mkdir(pj(p,v2));shutil.copytree(pj(p,v1),pj(p,v2),dirs_exist_ok=True)
def sbrun(cmd,m=sub.run,**k):
    if os.name=='nt':k['creationflags']=sub.CREATE_NO_WINDOW
    return m(cmd,**k)
def openfd(path):
    path=os.path.abspath(path)
    if os.name=='nt':os.startfile(path)
    elif sys.platform=='darwin':sub.run(['open',path])
    else:
        for i in ['xdg-open','nautilus', 'dolphin', 'thunar', 'pcmanfm', 'caja']:
            try:th.Thread(target=sub.run,args=([i,path])).start();break
            except FileNotFoundError:continue
def urljson(url,timeout=100):
    while 1:
        try:return req.get(url,verify=False,timeout=timeout).json()
        except Exception as ex:print(ex)
def dlurl(u,p,chunk_size=1048576,openf=open):
    mkdir(os.path.split(p)[0])
    while 1:
        try:
            rs=req.get(u,timeout=10,verify=False,stream=True)
            if rs.status_code!=200:raise RuntimeError(f'{u},resp code!=200')
            with openf(p,'wb') as f:
                for c in rs.iter_content(chunk_size=chunk_size):
                    f.write(c)#;t1=f.tell();self.speed+=t1-total
                    #total=t1
            return
        except Exception as ex:print(ex)
def pj(*p,cn='/',abspath=False):#连接路径 pj('a','b','c')返回'a/b/c' pj('c:\\a\\b','c')返回'c:/a/b/c' cn表示默认用'/'连接
    res=''
    for i in p:
        if not i:continue
        i=i.replace('\\','/').split('/')
        if res:
            if res[-1] not in '\\/':res+=cn
        else:pass#if i[0] and ':' not in i[0]:res+='./'
        res+=cn.join(i)
    if abspath:return os.path.abspath(res)
    else:return res
def readv(ver,d):
    with open(pj(d,'versions',ver,ver+'.json')) as f:
        return loads(f.read())
def fmass(v,d):
    if 'assetIndex' in v:
        p=pj('assets/indexes',v['assetIndex']['id']+'.json')
        with open(pj(d,p)) as f:
            return loads(f.read())
    else:return {}
def readass(ver,d):
    return fmass(readv(ver,d),d)
def getosversion():
    if platform.system() == "Windows":
        ver=sys.getwindowsversion()
        return f"{ver.major}.{ver.minor}"
    elif platform.system == "Darwin":return ""
    else:return platform.uname().release
def getosname():
    name=platform.system().lower()
    if name=='darwin':return 'osx'
    else:return name
def getcs():
    if getosname()=='windows':return ';'
    else:return ':'
def prules(rules):
    for rule in rules:
        if not 'os' in rule:continue
        if rule['action']=='allow':rt=True
        else:rt=False
        osrule=rule['os']
        if 'name' in osrule and osrule['name']==getosname():return rt
        if 'arch' in osrule and osrule['arch']=='x86' and platform.architecture()[0]=='32bit':return rt
        if 'version' in osrule and re.match(osrule['version'],getosversion()):return rt
        return not rt
def findver(txt,sep='',mode=int):
    return mode(sep.join(re.findall('\\d+',txt)))
def extzfa(fl,p,f=True):
    try:
        z=zipfile.ZipFile(fl)
        for f in z.namelist():
            to=pj(p,f)
            if os.path.exists(to):print(to,'exists');continue
            z.extract(f,p)
            print('extract',p)
        z.close()
    except:pass
def extzf(zf,path,to,chunk_size=524288):
    if os.path.exists(to):print(to,'exists');return
    mkdir(os.path.split(to)[0])
    f,f1=zf.open(path,'r'),open(to,'wb')
    print('extract',path,'to',to)
    b=f.read(chunk_size)
    while b:f1.write(b);b=f.read(chunk_size)
def extzff(zf,fd,to,chunk_size=524288):
    fd=pj(fd)
    for f in zf.namelist():
        if f.startswith(fd):
            if f[-1]=='/':mkdir(to,f.split('/')[1:]);continue
            p=pj(to,*f.split('/')[1:])
            try:extzf(zf,f,p)
            except Exception as s:print(s)
def fmname(name,end='jar'):
    n=name.split(':')
    if '@' in n[-1]:n[-1],end=n[-1].split('@')
    return n[0].replace('.','/'),n[1],n[2],n[1]+'-'+'-'.join(n[2:])+'.'+end
def mkdir(*p):
    try:os.makedirs(pj(*p))
    except:pass
def caluuid(name):#mojang的uuid计算原理
    md5_bytes=bytearray(hashlib.md5(f'OfflinePlayer:{name}'.encode('utf-8')).digest())
    #设置 UUID 版本为 3 (0011xxxx)
    #保留原字节低 4 位，高 4 位设为 0011 (即 0x30)
    md5_bytes[6] = (md5_bytes[6] & 0x0F) | 0x30
    #设置 UUID 变体为 RFC 4122 (10xxxxxx)
    #保留原字节低 6 位，高 2 位设为 10 (即 0x80)
    md5_bytes[8] = (md5_bytes[8] & 0x3F) | 0x80
    #将 16 字节转换为 32 位十六进制字符串
    return md5_bytes.hex()
def fmbt(num):
    if num<=512:return '512m'
    if num%1024==0:return str(num//1024)+'g'
    else:return str(int(num))+'m'
def findv(vd,typ='release',find=False):
    #typ=release,snapshot,old_beta,old_alpha
    vs=[]
    for v in vd['versions']:
        if typ and typ in v['type']:vs.append(v)
        if find:
            if v['id']==find:return v['url']
    if find:raise RuntimeError('版本不存在!')
    return vs
def fvanilla(vd,txt):
    for i in vd['versions']:
        if i['id'] in txt:return txt.replace(i['id'],''),i['id']
    return txt,''
def copyver(ver,d):
    vd=readv(ver,d)
    if 'inheritsFrom' in vd:return vd
    else:return {'id':ver,'inheritsFrom':ver,'libraries':[],'type':vd['type'],'mainClass':vd['mainClass']}
def mclist(d):
    p=pj(d,'versions')
    if not os.path.exists(p):return []
    for i in os.listdir(p):
        if os.path.exists(pj(p,i,i+'.json')):
            yield i
def getmlpcl(p):#返回mod加载器列表,如{'forge':'47.4.20'}
    pcl=pj(p,'PCL','Setup.ini')
    if os.path.exists(pcl):
        vd={}
        with open(pcl,'r',encoding='utf-8') as f:txt=f.read()
        for i in re.findall('(?<=Version)\\w+\\:[0-9.]+',txt):
            if 'Vanilla' in i:continue
            name,ver=i.split(':')
            vd[name.lower()]=ver
        return vd
    return {}
def fmlver(vd):
    dc={}
    if 'arguments' in vd:
        for i in vd['arguments']['game']:
            try:
                if t:return {t:i}#dc[t]=i;break
            except:pass
            if '--fml.' in i:t=i.split('.')[1][:-7].lower()
    for i in vd['libraries']:
        if 'fabric-loader:' in i['name']:dc['fabric']=i['name'].split(':')[-1]
        elif 'forge:fmlloader' in i['name'] or 'forge:forge:' in i['name']:
            dc['forge']=i['name'].split('-')[1]
        elif 'quilt-loader:' in i['name']:dc['quilt']=i['name'].split(':')[-1]
    return dc
    
def getmlname(vd,vid):
    return findver(fvanilla(vd,vid)[0],'.',str)
