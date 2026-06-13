from tools import *
def isarm():
    if 'aarch' in platform.architecture()[0]:return 1
def fmosn(osn):
    if osn=='osx':
        if isarm():return 'mac-os-arm64'
        else:return 'mac-os'
    if osn=='windows':
        if isarm():return 'windows-arm64'
        else:
            if sys.maxsize>2147483647:return 'windows-x64'
            else:return 'windows-x86'
    if osn=='linux':
        if sys.maxsize>2147483647:return 'linux'
        else:return 'linux-i386'
def getjavaf(name,p='mhc/java'+getosname(),rp='',osn1=getosname(),d=None):
    if not d:
        osn1=fmosn(osn1)
        url='https://launchermeta.mojang.com/v1/products/java-runtime/2ec0cc96c44e5a76b9c8b7c39df7210883d12871/all.json'
        if rp:url=url.replace('launchermeta.mojang.com',rp)
        url1=urljson(url)[osn1][name][0]['manifest']['url']
        if rp:url1=url1.replace('piston-meta.mojang.com',rp)
        d=urljson(url1)
    fs=[]
    for i in d['files']:
        if d['files'][i]['type']=='directory':mkdir(pj(p,name,i));continue
        if d['files'][i]['type']=='file':
            raw=d['files'][i]['downloads']['raw']
            if rp:raw['url']=raw['url'].replace('piston-meta.mojang.com',rp)
            fs.append((raw['url'],pj(p,name,i),raw['sha1']))
    return fs
def getmajorv(path):#获取java版本方法一:从release文件读取
    with open(path) as f:t=f.read()
    ver=int(re.findall('JAVA_VERSION="\\d+',t)[0].replace('JAVA_VERSION="',''))
    if ver==1:return 8
    else:return ver
def getjavav(path):#获取java版本方法二:从java.exe的输出截取
    ver=sbrun([path,'-version'],text=1,capture_output=1,).stderr.split()[2].replace('"','').split('.')
    if ver[0]=='1':return int(ver[1])
    else:return int(ver[0])
def findjava(path):
    finds={}
    if getosname()=='windows':find='java.exe'
    else:find='java'
    for r,d,f in os.walk(path):
        p,tag=pj(r,'bin',find),0
        if not os.path.exists(p):continue
        for i in f:
            if i=='release':ver,tag=getmajorv(pj(r,i)),1
        if not tag:ver=getjavav(p)
        finds[ver]=p
    return finds
            
        
