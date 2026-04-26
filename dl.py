import threading as th
from tools import *
from log import *
from time import sleep
d='.minecraft'
class xcdl:
    def __init__(self):
        self.threads=[]
        self.dls=[]
        #self.speed=0
    def chksha1(self,p,chunk_size=1048576):
        sha1=hashlib.sha1()
        with open(p,'rb') as f:
            c=f.read(chunk_size)
            while c:
                sha1.update(c)
                c=f.read(chunk_size)
        return sha1.hexdigest()
    def dl_th(self,chsha1=0):
        while self.dls:
            dct=self.dls.pop(0)
            try:u,p,s=dct
            except:u,p=dct;s=''
            if not u:continue
            if os.path.exists(p):
                if not s or not chsha1:continue
                if self.chksha1(p) in s:continue      
            print('下载',u)
            dlurl(u,p)
    def start(self,thread,chsha1=1):
        l=len(self.threads)
        if thread<=l:return
        else:thread-=l
        for i in range(thread):
            t=th.Thread(target=self.dl_th,args=(chsha1,),name='dl_th')
            t.start()
            self.threads.append(t)
        if l==0:self.join()
    def join(self):
        for i in self.threads:
            i.join()
        self.threads.clear()
def rpliburl(url,rp):
    return url.replace('libraries.minecraft.net',rp)\
        .replace('files.minecraftforge.net/maven',rp)\
        .replace('maven.fabricmc.net',rp)
def getlibs(v,d=d,rp=''):#启用bmclapi则将rp改为bmclapi2.bangbang93.com/maven
    fs=[]
    osn,arch=getosname(),str(findver(platform.architecture()[0]))
    for l in v['libraries']:
        if 'rules' in l and not prules(l['rules']):continue
        if 'downloads' in l and 'classifiers' in l['downloads']:
            nt=l['natives'][osn].replace('${arch}',arch)
            url=l['downloads']['classifiers'][nt]['url']
            if rp:url=rpliburl(url,rp)
            p,h=pj(d,'libraries',l['downloads']['classifiers'][nt]['path']),l['downloads']['classifiers'][nt]['sha1']
            fs.append((url,p,h))
            if not 'artifact' in l['downloads']:continue
        if 'downloads' in l and 'artifact' in l['downloads']:
            url=l['downloads']['artifact']['url']
            if rp:url=rpliburl(url,rp)
            p,h=pj(d,'libraries',l['downloads']['artifact']['path']),l['downloads']['artifact']['sha1']
            fs.append((url,p,h))
        else:
            p,n,v,file=fmname(l['name'])
            pt=pj(p,n,v,file)
            if not 'url' in l:continue
            url=pj(l['url'],pt)
            if rp:url=rpliburl(url,rp)
            p,h=pj(d,'libraries',pt),(l['sha1'] if 'sha1' in l else (l['checksums'] if 'checksums' in l else ''))
            fs.append((url,p,h))
    return fs
def getass(a,d,rp=''):
    if not rp:rp='https://resources.download.minecraft.net'
    else:rp='https://'+rp
    fs=[]
    for i in a['objects']:
        h=a['objects'][i]['hash']
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
def dlver(vd,ver,d=d,rpl='',rpa='',v=None):
    try:
        if not v:v=readv(ver,d)
    except:
        rs=req.get(findv(vd,0,ver),timeout=100)
        mkdir(d,'versions',ver)
        writec(pj(d,'versions',ver,ver+'.json'),rs.content)
        v=rs.json()
    fs=getlibs(v,d,rpl)
    if 'downloads' in v:fs+=[(v['downloads']['client']['url'],pj(d,'versions',ver,ver+'.jar'),v['downloads']['client']['sha1'])]
    if 'assetIndex' in v:
        try:a=fmass(v,d)
        except:
            rs=req.get(v['assetIndex']['url'],timeout=100)
            mkdir(d,'assets/indexes',ver)
            writec(pj(d,'assets/indexes',v['assetIndex']['id']+'.json'),rs.content)
            a=rs.json()
        fs+=getass(a,d,rpa)
    if 'inheritsFrom' in v:fs+=dlver(vd,v['inheritsFrom'],d,rpl,rpa)
    return fs
'''dl=xcdl()
dl+=dlver({},'1.21.4')
dl.start(128)'''
