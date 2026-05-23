from tools import *
import shutil
d='.minecraft'
def listlib(d=d):
    fls,osn,arch={},getosname(),str(findver(platform.architecture()[0]))
    for ver in os.listdir(pj(d,'versions')):
        for lib in readv(ver,d)['libraries']:
            #if 'rules' in lib and not prules(lib['rules']):continue
            if 'downloads' in lib:
                if 'classifiers' in lib['downloads']:
                    nt=lib['natives'][osn].replace('${arch}',arch)
                    if not nt in lib['downloads']['classifiers']:continue
                    fl=pj(lib['downloads']['classifiers'][nt]['path'])
                    try:fls[fl].append(ver)
                    except:fls[fl]=[ver]
                if 'actrifact' in lib['downloads']:
                    fl=lib['downloads']['artifact']['path']
                    try:fls[fl].append(ver)
                    except:fls[fl]=[ver]
            else:
                p,n,v,fll=fmname(lib['name'])
                fl=pj(p,n,v,fll)
                try:fls[fl].append(ver)
                except:fls[fl]=[ver]
    return fls
def listass(d=d):
    fls={}
    for ver in os.listdir(pj(d,'versions')):
        ass=readass(ver,d)
        if not ass:continue
        else:ass=ass['objects']
        for a in ass:
            h=ass[a]['hash']
            try:fls[h].append(ver)
            except:fls[h]=[ver]
    return fls
def outskin(d=d):
    try:os.makedirs('mhc/skins')
    except:pass
    for r,d,f in os.walk(pj(d,'assets','skins')):
        for i in f:
            shutil.copyfile(pj(r,i),pj('mhc/skins',i+'.png'))
def rmemptdir(d):
    tag=1
    for i in os.listdir(d):
        p=pj(d,i)
        if os.path.isfile(p):tag=0
        else:
            try:
                if not rmemptdir(p):tag=0
            except Exception as s:print(s)
    if tag:
        print('del',d)
        shutil.rmtree(d)
    return tag
