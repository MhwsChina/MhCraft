import sys,time,os
from json import dumps,loads
os.system('')
def walktraceback(traceback_object):
    while traceback_object:
        yield re.findall('code .+',str(traceback_object.tb_frame))[0].replace('code ','')[0:-1]
        traceback_object=traceback_object.tb_next
def exout(a, limit=None, file=None):
    print(f'[ThreadException]: {"->".join(walktraceback(a[2]))}:',a[1],mode='ERROR',start='\r')
try:os.mkdir('mhc')
except:pass
cfp='./mhc/config.json'
with open(cfp,'a+') as jfr:
    jfr.seek(0)
    try:js=loads(jfr.read())
    except:js={}
def print(*txt,mode=None,sep=' ',end='\n',start='',b=''):
    m=sys._getframe(1).f_globals['__name__']
    m='' if m=='__main__' else f'[{m}]: '
    txt=sep.join([str(i) for i in [*txt]])
    if not mode:mode='INFO'
    if not b:
        if mode=='WARN':b='\033[33m'
        if mode=='ERROR' or mode=='ERR':b='\033[31m'
        if mode=='TIPS':b='\033[34m'
        if mode=='SUC' or mode=='SUCCESSFUL':b='\033[32m'
        if mode=='PROG' or mode=='PROGRESS':b,m='\033[37;42m','\033[0m\033[1m'+m
    sys.stdout.write(f'{start}{b}{m}{txt}{end}\033[K\033[0m')
    sys.stdout.flush()
def getjs(*st):
    m,a=sys._getframe(1).f_globals['__name__'],[]
    if not m in js:js[m]={}
    if not [*st]:return js[m]
    for i in [*st]:
        t=i[0] if len(i)==2 else i
        if t in js[m]:a+=[js[m][t]]
        else:
            if len(i)==2:
                js[m][i[0]]=i[1]
                a+=[i[1]]
    if len(a)==1:return a[0]
    return a
def setjs(*st,rt=0):
    a,m=[*st],sys._getframe(1).f_globals['__name__']
    if not a:js[m]={};return
    try:js[m]
    except:js[m]={}
    for i in a:
        try:b,c=i;js[m][b]=c
        except:
            if i in js[m]:del js[m][i]
    with open(cfp,'w') as f:f.write(dumps(js))
    if rt:return js[m]
def updatejs(a):
    js[sys._getframe(1).f_globals['__name__']]=a
    with open(cfp,'w') as f:f.write(dumps(js))
