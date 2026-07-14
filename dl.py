import threading as th
from tools import *
from log import *
from time import sleep
d='.minecraft'
wrt=[]
class mopen:
    def __init__(self,p,a='wb'):
        self.data={'p':p,'a':a,'d':b''}
    def __enter__(self):
        return self
    def __exit__(self,*a):
        self.close()
    def write(self,t):
        while 1:
            try:
                try:self.data['d']+=t
                except:self.data['d']=t
                break
            except:pass
    def close(self):
        global wrt
        while 1:
            try:wrt.append(self.data);break
            except:pass
        del self.data
class xcdl:
    def __init__(self):
        self.threads=[]
        self.dls=[]
        #self.speed=0
    def dl_th(self,chsha1=0,huancun=1):
        while self.dls:
            dct=self.dls.pop(0)
            try:u,p,s=dct
            except:u,p=dct;s=''
            if not u:continue
            if os.path.exists(p):
                if not s or not chsha1:continue
                if chksha(p) in s:continue      
            #print('下载',u)
            dlurl(u,p,openf=(mopen if huancun else open))
    def start(self,thread,chsha1=1,huancun=1):
        l=len(self.threads)
        if thread>l:thread=thread-l
        else:thread=0
        for i in range(thread):
            t=th.Thread(target=self.dl_th,args=(chsha1,huancun),name='dl_th')
            t.start()
            self.threads.append(t)
        if l==0 and huancun:self.wt=th.Thread(target=self.write);self.wt.start()
        #self.join()
    def write(self):
        while wrt or self.threads:
            try:d=wrt.pop(0)
            except:sleep(0.1);continue
            with open(d['p'],d['a']) as f:
                f.write(d['d'])
    def join(self):
        while self.threads:
            i=self.threads.pop(0)
            try:i.join()
            except Exception as ex:print(ex)
        try:self.wt.join()
        except:pass
def rpliburl(url,rp):
    return url.replace('libraries.minecraft.net',rp)\
        .replace('files.minecraftforge.net',rp)\
        .replace('maven.fabricmc.net',rp)\
        .replace('maven.neoforged.net/releases',rp)
        #.replace('maven.quiltmc.org/repository/release',rp)
def getlibs(vd,d=d,rp=''):#启用bmclapi则将rp改为bmclapi2.bangbang93.com/maven
    fs=[]
    osn,arch=getosname(),str(findver(platform.architecture()[0]))
    for l in vd['libraries']:
        if 'rules' in l and not prules(l['rules']):continue
        if 'downloads' in l and 'classifiers' in l['downloads']:
            nt=l['natives'][osn].replace('${arch}',arch)
            url=l['downloads']['classifiers'][nt]['url']
            if rp:url=rpliburl(url,rp)
            p,h=pj(d,'libraries',l['downloads']['classifiers'][nt]['path']),l['downloads']['classifiers'][nt]['sha1']
            fs.append((url,p,h))
            if 'artifact' not in l['downloads']:continue
        if 'downloads' in l and 'artifact' in l['downloads']:
            url=l['downloads']['artifact']['url']
            if rp:url=rpliburl(url,rp)
            p,h=pj(d,'libraries',l['downloads']['artifact']['path']),l['downloads']['artifact']['sha1']
            fs.append((url,p,h))
        else:
            p,n,v,file=fmname(l['name'])
            pt=pj(p,n,v,file)
            if 'url' not in l:continue
            url=pj(l['url'],pt)
            if rp:url=rpliburl(url,rp)
            p,h=pj(d,'libraries',pt),(l['sha1'] if 'sha1' in l else (l['checksums'] if 'checksums' in l else ''))
            fs.append((url,p,h))
    return fs
def getass(ad,d,rp=''):
    if not rp:rp='https://resources.download.minecraft.net'
    else:rp='https://'+rp
    fs=[]
    for i in ad['objects']:
        h=ad['objects'][i]['hash']
        p=pj(h[0:2],h)
        url=pj(rp,p)
        fs.append((url,pj(d,'assets/objects',p),h))
    return fs
def getallv():
    url='http://launchermeta.mojang.com/mc/game/version_manifest.json'
    return urljson(url)
def writec(file,c):
    with open(file,'wb') as f:
        f.write(c)
def dlver(vdc,ver,d=d,rpl='',rpa='',vd=None):
    try:
        if not vd:vd=readv(ver,d)
    except:
        rs=req.get(findmcv(vdc,0,ver),timeout=100)
        mkdir(d,'versions',ver)
        writec(pj(d,'versions',ver,ver+'.json'),rs.content)
        vd=rs.json()
    fs=getlibs(vd,d,rpl)
    if 'downloads' in vd:fs+=[(vd['downloads']['client']['url'],pj(d,'versions',ver,ver+'.jar'),vd['downloads']['client']['sha1'])]
    if 'assetIndex' in vd:
        try:a=fmass(vd,d)
        except:
            rs=req.get(vd['assetIndex']['url'],timeout=100)
            mkdir(d,'assets/indexes')
            writec(pj(d,'assets/indexes',vd['assetIndex']['id']+'.json'),rs.content)
            a=rs.json()
        fs+=getass(a,d,rpa)
    if 'inheritsFrom' in vd:fs+=dlver(vdc,vd['inheritsFrom'],d,rpl,rpa)
    return fs
'''dl=xcdl()
dl+=dlver({},'1.21.4')
dl.start(128)'''
