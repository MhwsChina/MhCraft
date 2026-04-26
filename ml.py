from tools import *
def fabric_latestloader():
    return req.get('https://meta.fabricmc.net/v2/versions/loader',verify=False,timeout=100).json()[0]['version']
#安装fabric很简单,不必多讲,就是下载文件即可
def instfabric(ver,loader,d='.minecraft'):#ver为要安装fabric的mc版本,安装完后记得补全文件
    #print('获取最新版fabric-loader')
    #lt=fabric_latestloader()
    url=f'https://meta.fabricmc.net/v2/versions/loader/{ver}/{loader}/profile/json'
    rs=req.get(url,timeout=1000,verify=False)
    if rs.status_code==200:
        v=rs.json()['id']
        mkdir(d,'versions',v)
        with open(pj(d,'versions',v,v+'.json'),'wb') as f:
            f.write(rs.content)
        return v
    else:raise RuntimeError(f'没有支持该版本的Fabric,res_code={rs.status_code},res_text={rs.text}')
def forgelist():
    met=req.get('https://files.minecraftforge.net/maven/net/minecraftforge/forge/maven-metadata.xml',verify=False,timeout=100).text
    return re.findall("(?<=<version>).*?(?=</version>)", met)
def getforgev(ver):
    v=0
    for i in forgelist():
        mcv,fgv=i.split('-')[0:2]
        fgv=findver(fgv)
        if mcv==ver and fgv>v:rt,v=i,fgv
    return rt
def forge_inst_url(ver):
    fgn=getforgev(ver)
    return f"https://files.minecraftforge.net/maven/net/minecraftforge/forge/{fgn}/forge-{fgn}-installer.jar",fgn

#重要提醒!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#安装forge先运行part1,根据返回的最后一个变量v,也就是mc版本,补全一遍文件再运行part2
def instforge_part1(instp,d='.minecraft'):#part1
    print('安装forge第一步:基础文件');print('安装json及运行库')
    zf=zipfile.ZipFile(instp,'r')
    with zf.open('install_profile.json','r') as f:
        dc=loads(f.read())#dc为格式化为dict的install_profile.json
    ###获取版本###
    ins=dc['install'] if 'install' in dc else dc#区分老版本
    v,mcv,ins=ins['version'],ins['minecraft'],None#forge版本号和对应的mc版本号
    if os.path.exists(pj(d,'versions',v)):zf.close();return 0,0,0#已经安装过了
    ###解压版本json###
    print('解压json')
    verp=pj(d,'versions',v)
    try:extzf(zf,'version.json',pj(verp,v+'.json'))#新版本
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
    lzp=pj('mhc/forge',v+'client.lzma')
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
def instforge_part2(lzp,dc,v,instp,java,d='.minecraft'):#part2
    print('安装forge第二步:forge_processors')
    if not 'processors' in dc:print('旧版本无需第二步,已取消');return
    av={'{MINECRAFT_JAR}':pj(d,'versions',dc['minecraft'],dc['minecraft']+'.jar'),
        '{INSTALLER}':instp,
        '{ROOT}':'mhc/forge/temp',
        '{SIDE}':'client'
    }
    for k in dc['data']:#这一步必须得有
        v=dc['data'][k]
        if v['client'][0]=='[':v=pj(d,'libraries',*fmname(v['client'][1:-1]))
        else:v=v['client']
        av['{'+k+'}']=v
    av['{BINPATCH}'],cs=lzp,getcs()#这个放在后面修改因为上面那一步会把binpatch改成data/client.lzma,而这个路径应该为lzp,即mhc/forge版本+client.lzma
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
