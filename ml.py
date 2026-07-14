from tools import *
def latest_fabricloader(url='meta.fabricmc.net'):
    return urljson(f'https://{url}/v2/versions/loader',timeout=10)[0]['version']
#安装fabric很简单,不必多讲,就是下载文件即可
def instfabric(ver,loader,url='meta.fabricmc.net',d='.minecraft',v1=None):#ver为要安装fabric的mc版本,安装完后记得补全文件
    #print('获取最新版fabric-loader')
    #lt=fabric_latestloader()
    rs=req.get(f'https://{url}/v2/versions/loader/{ver}/{loader}/profile/json',timeout=10,verify=False)
    if rs.status_code==200:
        v=rs.json()['id']
        p=pj(d,'versions',v1 if v1 else v)
        #if os.path.exists(p):raise RuntimeError('已经安装过了')
        mkdir(p)
        with open(pj(p,(v1 if v1 else v)+'.json'),'wb') as f:
            f.write(rs.content)
        return v
    else:raise RuntimeError(f'没有支持该版本的fabric!\nres_code={rs.status_code},res_text={rs.text}')
#安装quilt和fabric方法一样,就是换个api
def latest_quiltloader(url='meta.quiltmc.org'):
    return urljson(f'https://{url}/v3/versions/loader',timeout=10)[0]['version']
def instquilt(ver,loader,url='meta.quiltmc.org',d='.minecraft',v1=None):#ver为要安装fabric的mc版本,安装完后记得补全文件
    #print('获取最新版fabric-loader')
    #lt=fabric_latestloader()
    rs=req.get(f'https://{url}/v3/versions/loader/{ver}/{loader}/profile/json',timeout=10,verify=False)
    if rs.status_code==200:
        v=rs.json()['id']
        p=pj(d,'versions',v1 if v1 else v)
        #if os.path.exists(p):raise RuntimeError('已经安装过了')
        mkdir(p)
        with open(pj(p,(v1 if v1 else v)+'.json'),'wb') as f:
            f.write(rs.content)
        return v
    else:raise RuntimeError(f'没有支持该版本的quilt!\nres_code={rs.status_code},res_text={rs.text}')
#optifine版本列表
#由于官方没有提供api获取版本列表,只能通过暴力查找下载页面来获取
def optilist(url='https://optifine.net/downloads'):
    res=req.get(url,verify=False,timeout=100)
    if res.status_code!=200:raise RuntimeError('Optifine的服务器炸了!程序无法从服务器获得版本清单!')
    html=res.text
    mcs=(i.split('_')[-1] for i in re.findall('(?<="http://optifine.net/adloadx\\?f=).+(?=_HD)',html))
    urls=re.findall('(?<=colMirror\'><a href=").+(?=">\\(Mirror\\))',html)
    forgs=re.findall('(?<=colForge\'>).+(?=</td>)',html)
    return zip(mcs,urls,forgs)
#注意optilist返回的url并非真实的下载地址,需要使用fmopurl(返回地址)来获取真的下载地址
def fmopurl(dlurl,url='optifine.net'):
    html=req.get(dlurl,verify=False,timeout=100).text
    return 'https://'+url+'/'+re.findall('(?<=a href=\').+(?=\' onclick=)',html)[0]
def opdlurl(ver,fm=1):#此处的ver为mc版本
    for mc,url,fg in optilist():
        if mc==ver:
            if fm:return fmopurl(url)
            else:return url
    raise RuntimeError('没有支持该版本的optifine!')
def instoptifine(instp,java,d='.minecraft'):
    arg=[java,'-Duser.home='+os.path.abspath(pj(d,'..')),'-cp',instp,'optifine.Installer']
    print(arg);sub.run(arg,env={})#windows系统中的optifine安装程序会读取环境变量中的APPDATA目录拼接.minecraft来获取mc目录,所以这里把它定义为空,安装程序就会读取user.home的值,以此来实现自定义mc目录
#neoforge版本列表
def neolist(url='maven.neoforged.net/releases'):
    met=req.get(f'https://{url}/net/neoforged/neoforge/maven-metadata.xml',verify=False,timeout=100).text
    return re.findall("(?<=<version>).+(?=</version>)", met)
def getneov(ver,url='maven.neoforged.net/releases'):
    v=0;print(ver)#此处的ver为mc版本
    #neoforge旧版本命名: mc版本后两位.neoforge版本(-beta)
    #新版本命名: mc版本.neoforge版本(-beta)
    for i in neolist(url):
        v1=i.split('-')[0].split('.');mcv,fgv='.'.join(v1[0:-1]),int(v1[-1])
        if mcv in ver and fgv>v:rt,v=i,fgv
    try:return rt
    except:raise RuntimeError('没有支持该版本的neoforge!')
def neodlurl(ver,url='maven.neoforged.net/releases'):
    fgn=getneov(ver,url)#此处的ver为mc版本
    return f"https://{url}/net/neoforged/neoforge/{fgn}/neoforge-{fgn}-installer.jar",fgn
#forge版本列表
def forgelist(url='files.minecraftforge.net'):
    met=req.get(f'https://{url}/maven/net/minecraftforge/forge/maven-metadata.xml',verify=False,timeout=100).text
    return re.findall("(?<=<version>).+(?=</version>)", met)
def getforgev(ver,url='files.minecraftforge.net'):
    v=0;print(ver)#此处的ver为mc版本
    for i in forgelist(url):
        mcv,fgv=i.split('-')[0:2]
        fgv=findver(fgv)
        if mcv==ver and fgv>v:rt,v=i,fgv
    try:return rt
    except:raise RuntimeError('没有支持该版本的forge!')
def forgedlurl(ver,url='files.minecraftforge.net'):
    fgn=getforgev(ver,url)#此处的ver为mc版本
    return f"https://{url}/maven/net/minecraftforge/forge/{fgn}/forge-{fgn}-installer.jar",fgn

#重要提醒!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#安装forge先运行part1,补全一遍文件再运行part2
#这些代码也支持安装neoforge
def instforge_part1(instp,d='.minecraft',v1=None):#part1
    print('安装forge第一步:基础文件');print('安装json及运行库')
    zf=zipfile.ZipFile(instp,'r')
    with zf.open('install_profile.json','r') as f:
        dc=loads(f.read())#dc为格式化为dict的install_profile.json
    ###获取版本###
    ins=dc['install'] if 'install' in dc else dc#区分老版本
    v,mcv,ins=ins['version'],ins['minecraft'],None#forge版本号和对应的mc版本号
    #if os.path.exists(pj(d,'versions',v)):zf.close();raise RuntimeError(f'已经安装过了!ver={v}')
    ###解压版本json###
    print('解压json')
    verp=pj(d,'versions',v1 if v1 else v)
    try:extzf(zf,'version.json',pj(verp,(v1 if v1 else v)+'.json'))#新版本
    except:#旧版本不含version.json所以从dc中提取
        with open(pj(verp,v+'.json'),'w') as f:
            f.write(dumps(dc['versionInfo']))
    #d=readv(v)
    ###解压运行库###
    print('解压运行库')
    extzff(zf,'maven',pj(d,'libraries'))
    ###解压主文件(旧版本)###
    try:extzf(zf,dc['install']['filePath'],pj(d,'libraries',*fmname(dc['install']['path'])))
    except:pass
    ###解压lzma###
    mkdir('mhc/temp');lzp=pj('mhc/temp',v+'client.lzma')
    try:
        if not os.path.exists(lzp):extzf(zf,'data/client.lzma',lzp)
    except:lzp=''
    zf.close()
    return lzp,dc,v
def get_jar_mainclass(path):#获取jar的mainclass,该段代码参考了minecraft-launcher-lib第三方包的_helper.py
    """
    Returns the mainclass of a given jar
    """
    zf,content=zipfile.ZipFile(path),{}
    # Parse the MANIFEST.MF
    with zf.open("META-INF/MANIFEST.MF") as f:lines = f.read().decode("utf-8").splitlines()
    zf.close()
    for i in lines:
        try:
            key, value = i.split(":")
            content[key] = value[1:]
        except Exception:pass
    return content["Main-Class"]
def instforge_part2(instp,lzp,dc,java,d='.minecraft'):#part2
    print('安装forge第二步:forge_processors')
    if not 'processors' in dc:print('旧版本无需第二步,已取消');return
    av={'{MINECRAFT_JAR}':pj(d,'versions',dc['minecraft'],dc['minecraft']+'.jar'),
        '{INSTALLER}':instp,
        '{ROOT}':'mhc/temp',
        '{SIDE}':'client'
    }
    for k in dc['data']:#这一步必须得有
        v=dc['data'][k]
        if v['client'][0]=='[':v=pj(d,'libraries',*fmname(v['client'][1:-1]))
        else:v=v['client']
        av['{'+k+'}']=v
    av['{BINPATCH}'],cs=lzp,getcs()#这个放在后面修改因为上面那一步会把binpatch改成data/client.lzma,而这个路径应该为lzp,即mhc/temp版本+client.lzma
    for p in dc['processors']:
        if not 'client' in p.get('sides','client'):continue#跳过服务端的process
        args,cps=[java,'-cp'],''
        for cp in p['classpath']:
            cps+=pj(d,'libraries',*fmname(cp))+cs#拼接classpath
        j=pj(d,'libraries',*fmname(p['jar']));cps+=j
        args.append(cps);args.append(get_jar_mainclass(j))
        for a in p['args']:
            if a[0]=='[':a=pj(d,'libraries',*fmname(a[1:-1]))#格式化arg
            else:
                for i in av:a=a.replace(i,av[i])
            args.append(a)
        print('运行',args);sub.run(args)#运行arg
