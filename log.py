import sys,time,os
from json import dumps,loads
def walktraceback(traceback_object):
    while traceback_object:
        yield re.findall('code .+',str(traceback_object.tb_frame))[0].replace('code ','')[0:-1]
        traceback_object=traceback_object.tb_next
def exout(a, limit=None, file=None):
    print(f'[ThreadException]: {"->".join(walktraceback(a[2]))}:',a[1],mode='ERROR',start='\r')
try:os.mkdir('mhc')
except:pass
cfp,usp='./mhc/config.json','./mhc/users.json'
with open(cfp,'a+') as jfr:
    jfr.seek(0)
    try:js=loads(jfr.read())
    except:js={}
def getjs(*st):
    global js
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
    global js
    a,m=[*st],sys._getframe(1).f_globals['__name__']
    if not a:js[m]={};return
    try:js[m]
    except:js[m]={}
    for i in a:
        try:b,c=i;js[m][b]=c
        except:
            if i in js[m]:del js[m][i]
    savejs()
    if rt:return js[m]
def savejs():
    with open(cfp,'w') as f:f.write(dumps(js))
def updatejs(a):
    global js
    js[sys._getframe(1).f_globals['__name__']]=a
    savejs()
def alluser():
    global users
    with open(usp,'a+') as f:
        f.seek(0)
        users=[loads(i.strip()) for i in f.readlines() if i]
    return users
def saveuser():
    with open(usp,'w') as f:
        [f.write(dumps(user)+'\n') for user in users]
def rmuser(ind):
    try:
        del users[ind]
        saveuser()
    except:raise
def adduser(data):
    users.append(data)
    with open(usp,'a') as f:
        f.write(dumps(data)+'\n')
