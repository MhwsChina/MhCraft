import re,platform,sys,zipfile,os,hashlib
import requests as req
import subprocess as sub
from json import loads,dumps
req.urllib3.disable_warnings()
def urljson(url,timeout=100):
    while 1:
        try:return req.get(url,verify=False,timeout=timeout).json()
        except:pass
def dlurl(u,p,chunk_size=1048576):
    mkdir(os.path.split(p)[0])
    while 1:
        try:
            rs,total=req.get(u,timeout=10,verify=False,stream=True),0
            if rs.status_code!=200:raise RuntimeError(f'{u},resp code!=200')
            with open(p,'wb') as f:
                for c in rs.iter_content(chunk_size=chunk_size):
                    f.write(c)#;t1=f.tell();self.speed+=t1-total
                    #total=t1
            return
        except Exception as ex:print(ex)
def pj(*p,cn='/'):#连接路径 pj('a','b','c')返回'a/b/c' pj('c:\\a\\b','c')返回'c:/a/b/c' cn表示默认用'/'连接
    res=''
    for i in p:
        if not i:continue
        if i[-1] in '\\/':i=i[0:-1]
        if i[0] in '\\/':i=i[1:]
        i=i.replace('\\','/').split('/')
        if res:res+=cn
        res+=cn.join(i)
    return res
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
def findver(txt):
    return int(''.join(re.findall('\\d+',txt)))
def extzfa(fl,p,f=True):
    try:
        z=zipfile.ZipFile(fl)
        z.extractall(p)
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
def caluuid(name):
    return hashlib.sha1(name.encode()).hexdigest()[0:32]
def fmbt(num):
    if num<=512:return '512m'
    if num%1024==0:return str(num//1024)+'g'
    else:return str(int(num))+'m'
def findv(vd,typ='release',find=False):
    #typ=release,snapshot,old_beta,old_alpha
    vs=[]
    for v in vd['versions']:
        if v['type']==typ:vs.append(v)
        if find:
            if v['id']==find:return v['url']
    if find:raise RuntimeError('版本不存在!')
    return vs
def fvanilla(vd,txt):
    for i in vd['versions']:
        if i['id'] in txt:fd,txt=i['id'],txt.replace(i['id'],'');break
    return fd,txt
def fmmln(vd,txt):
    return findver(fvanilla(vd,txt)[1])
#p=r"d:\Admin\Downloads\forge-1.20.1-47.4.20-installer.jar"
#extzfa(p,'666')
