import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mess
from tkinter import filedialog
import psutil,auth
from getargs import *
from dl import *
from java import *
from files import *
from ml import *
from modrinth import *
from update import getupdate
fg,ffg='black','#cce4f7'
def lb(b,**kw):return tk.Label(b,**kw,fg=fg)
def lsx(b,**kw):return tk.Listbox(b,**kw,fg=fg)
def tx(b,**kw):return tk.Text(b,**kw,fg=fg)
def bt(b,**kw):return tk.Button(b,**kw,activebackground=ffg,relief='groove',fg=fg)
def entry(b,**kw):return tk.Entry(b,**kw,fg=fg)
def combox(b,**kw):return ttk.Combobox(b,**kw,foreground=fg,background=fg)
def spinx(b,**kw):return ttk.Spinbox(b,**kw,foreground=fg)
def radiobt(b,**kw):return tk.Radiobutton(b,**kw,fg=fg,relief='flat')
def checkbt(b,**kw):return tk.Checkbutton(b,**kw,fg=fg,relief='flat')
def frm(a,**k):return tk.Frame(a,**k)
def lbfrm(a,**k):return tk.LabelFrame(a,fg=fg,**k)
def scale(a,orient='horizontal',**k):return tk.Scale(a,**k,fg=fg,relief='flat',orient=orient)
class var(tk.Variable):
    def __init__(self,name,value,typ=str):
        self.type=typ
        value=getjs((name,value));self._default=value
        tk.Variable.__init__(self,value=value,name=name)
        self.trace_add('write',self.settojs)
    def settojs(self,*args):
        setjs((self._name,self.type(self._tk.globalgetvar(self._name))))
    def set(self,value):
        setjs((self._name,self.type(value)))
        super().set(value)
    def get(self):
        return self.type(getjs(self._name))
    def reset(self):
        self.set(self._default)
class ui:
    def __init__(self):
        self.ver='v3'
        self.text='公告:作者开了个mc服务器,地址为folia.cc.cd:22222,无需正版账号,游戏版本为26.1.2'
        self.srs,self.step=[],0
        self.reg={'fabric':self.instfab,'forge':self.instfg,'quilt':self.instquilt,'neoforge':self.instneo,'optifine':self.instopti}
        self.createW()
    def show(self):
        w.mainloop()
    def createW(self):
        global w
        w=tk.Tk();w.resizable(0,0)
        w.title(f'MhCraft {self.ver}')
        ttk.Style().configure('m.TNotebook.Tab',foreground=fg);ttk.Style().configure('m.TNotebook', tabposition='sw')
        ttk.Style().configure('m1.TNotebook.Tab',foreground=fg);ttk.Style().configure('m1.TNotebook', tabposition='nw')
        self.nt=ttk.Notebook(w,style='m.TNotebook')
        self.rn=tk.Frame();self.nt.add(self.rn,text='启动')
        self.dl=tk.Frame();self.nt.add(self.dl,text='下载')
        self.prf=tk.Frame();self.nt.add(self.prf,text='角色')
        self.st=ttk.Notebook(style='m1.TNotebook');self.nt.add(self.st,text='设置')
        self.ab=tk.Frame();self.nt.add(self.ab,text='关于')
        self.nt.grid(padx=10,pady=7)
        ###启动页面
        r1=lbfrm(self.rn,text='所有版本')
        self._vls=tk.Scrollbar(r1,orient='vertical');self._vls.pack(side='right',fill='y')
        self.vl=lsx(r1,width=40,height=11,yscrollcommand=self._vls.set);self.vl.pack(side='left')
        self._vls.config(command=self.vl.yview)
        self.vl.bind('<<ListboxSelect>>',self.setinfo)
        r1.grid(row=0,column=0,rowspan=2)
        r2=lbfrm(self.rn,text='操作')
        bt(r2,text='启动',width=5,command=self.runmc).grid(row=0,column=0)
        bt(r2,text='删除',width=5,command=self.rmmc).grid(row=0,column=1)
        bt(r2,text='复制',width=5,command=self.copymc).grid(row=0,column=2)
        bt(r2,text='重命名',width=5,command=self.rnmc).grid(row=0,column=3)
        bt(r2,text='修复缺损文件',width=12,command=self.bqmc).grid(row=1,columnspan=2)
        bt(r2,text='导出启动脚本',width=12,command=self.outmc).grid(row=1,column=2,columnspan=2)
        bt(r2,text='操作存档',width=12,command=self.csaves).grid(row=2,columnspan=2)
        bt(r2,text='导出整合包',width=12,command=self.export).grid(row=2,column=2,columnspan=2)
        #bt(r2,text='刷新版本列表').grid(row=3,column=0,columnspan=3)
        r2.grid(row=0,column=1,sticky='nw')
        r3=lbfrm(self.rn,text='资源')
        bt(r3,text='模组文件夹',width=12,command=lambda:self.openvfd('mods')).grid(row=0)
        bt(r3,text='光影文件夹',width=12,command=lambda:self.openvfd('shaderpacks')).grid(row=0,column=1)
        bt(r3,text='资源包文件夹',width=12,command=lambda:self.openvfd('resourcepacks')).grid(row=1)
        bt(r3,text='截图文件夹',width=12,command=lambda:self.openvfd('screenshots')).grid(row=1,column=1)
        bt(r3,text='存档文件夹',width=12,command=lambda: self.openvfd('saves')).grid(row=2)
        bt(r3,text='版本文件夹',width=12,command=lambda: self.openvfd('')).grid(row=2,column=1)
        #bt(r3,text='导出整合包',width=12).grid(row=6)
        r3.grid(row=1,column=1,sticky='nw')
        r4=lbfrm(self.rn,text='版本信息')
        self.v1=tk.StringVar();self.v1.set('版本号:无')#self.v1.set(mc版本号信息)
        lb(r4,textvariable=self.v1,width=26).grid(row=1)
        self.ml=tk.StringVar();self.ml.set('模组加载器:无')#self.ml.set(mc模组加载器名称)
        lb(r4,textvariable=self.ml,width=26).grid(row=2)#self.mlv.set(mc模组加载器版本)
        self.mlv=tk.StringVar();self.mlv.set('加载器版本:无')
        lb(r4,textvariable=self.mlv,width=26).grid(row=3)
        r4.grid(row=1,column=2,sticky='nw')
        r5=lbfrm(self.rn,text='模组加载器')
        self.scm=tk.StringVar();self.scm.set('fabric')
        radiobt(r5,text='fabric',variable=self.scm,value='fabric',width=9).grid(row=0)
        radiobt(r5,text='quilt',variable=self.scm,value='quilt',width=9).grid(row=0,column=1)
        radiobt(r5,text='forge',variable=self.scm,value='forge',width=9).grid(row=1)
        radiobt(r5,text='neoforge',variable=self.scm,value='neoforge',width=9).grid(row=1,column=1)
        radiobt(r5,text='optifine',variable=self.scm,value='optifine',width=9).grid(row=2)
        bt(r5,text='安装',width=12,command=self.instml).grid(row=3)
        bt(r5,text='更新',width=12,command=self.updml).grid(row=3,column=1)
        r5.grid(row=0,column=2,sticky='nw',rowspan=2)
        ###下载界面
        self.d1=lbfrm(self.dl,text='下载列表')#d1.config(text='asdfasdf') 更改"下载列表"标题
        self._dls=tk.Scrollbar(self.d1,orient='vertical');self._dls.pack(side='right',fill='y')
        self.dll=lsx(self.d1,width=40,height=11,yscrollcommand=self._dls.set);self.dll.pack(side='left')
        self._dls.config(command=self.dll.yview)#self.dll:listbox 下载列表
        self.d1.grid(row=0,column=0,rowspan=2)
        d2=lbfrm(self.dl,text='mc')
        self.dlt=tk.StringVar();self.dlt.set('release')#self.dlt.get() 下载的mc版本种类
        radiobt(d2,text='正式版',variable=self.dlt,value='release',command=self.redl).grid(row=1)
        radiobt(d2,text='测试版',variable=self.dlt,value='snapshot',command=self.redl).grid(row=1,column=1)
        radiobt(d2,text='远古版',variable=self.dlt,value='old',command=self.redl,width=12).grid(row=1,column=2)
        bt(d2,text='刷新列表',width=12,command=self.redl).grid(row=2)
        bt(d2,text='下载',width=12,command=lambda:th.Thread(target=self.dlmc).start()).grid(row=2,column=1)
        d2.grid(row=0,column=1,sticky='nw')
        d3=lbfrm(self.dl,text='资源搜索')
        lb(d3,text='搜索内容:').grid(row=0)
        self.src=entry(d3,width=26);self.src.grid(row=0,column=1,columnspan=2)
        lb(d3,text='搜索条件:').grid(row=1)#self.src.get() 搜索内容
        self.srt=tk.StringVar();self.srt.set('模组')#self.srt.get() 搜索条件
        combox(d3,values=['模组','资源包','数据包','光影'],textvariable=self.srt,width=23).grid(row=1,column=1,columnspan=2,sticky='w')
        lb(d3,text='页码').grid(row=2)
        self.srp=tk.IntVar();self.srp.set(1)#self.srp.get() 搜索页码
        spinx(d3,textvariable=self.srp,from_=1,to=10000,width=24).grid(row=2,column=1,columnspan=2,sticky='w')
        bt(d3,text='刷新列表',width=12,command=self.resr).grid(row=3)
        bt(d3,text='搜索',width=12,command=self.srch).grid(row=3,column=1)
        self.srbt=bt(d3,text='选择',width=12,command=self.dlmod);self.srbt.grid(row=3,column=2)
        d3.grid(row=1,column=1,sticky='w')
        ###角色界面
        u1=lbfrm(self.prf,text='角色列表')
        self._prfs=tk.Scrollbar(u1,orient='vertical');self._prfs.pack(side='right',fill='y')
        self.prfl=lsx(u1,width=40,height=11,yscrollcommand=self._prfs.set);self.prfl.pack(side='left')
        self._prfs.config(command=self.prfl.yview)
        u1.grid(row=0,column=0,rowspan=2)
        u0=lbfrm(self.prf,text='操作')
        u2=lbfrm(u0,text='离线用户')
        lb(u2,text='角色名',width=5).grid(row=0)
        self.adprf=tk.StringVar();entry(u2,width=20,textvariable=self.adprf).grid(row=0,column=1)
        u2.grid(row=0,columnspan=2)
        u3=lbfrm(u0,text='第三方用户')
        lb(u3,text='服务器',width=5).grid(row=0)
        self.adsv=tk.StringVar();entry(u3,width=20,textvariable=self.adsv).grid(row=0,column=1)
        self.adsv.set('https://littleskin.cn/api/yggdrasil')
        lb(u3,text='邮箱',width=5).grid(row=1)
        self.adem=tk.StringVar();entry(u3,width=20,textvariable=self.adem).grid(row=1,column=1)
        lb(u3,text='密码',width=5).grid(row=2)
        self.adps=tk.StringVar();entry(u3,width=20,textvariable=self.adps).grid(row=2,column=1)
        u3.grid(row=1,columnspan=2)
        bt(u0,text='登录并添加',width=10,command=self.addprf).grid(row=2)
        bt(u0,text='使用(从左侧选择)',width=15,command=self.useprf).grid(row=2,column=1)
        bt(u0,text='微软登录',width=10,command=lambda:self.noadd('微软登录')).grid(row=3,sticky='w')
        bt(u0,text='删除(从左侧选择)',width=15,command=self.rmprf).grid(row=3,column=1,sticky='w')
        u0.grid(row=0,column=1)
        u4=lbfrm(self.prf,text='信息')
        lb(u4,text='当前使用:').grid(row=0)
        self.prfn=tk.StringVar();self.prfn.set('无')
        lb(u4,textvariable=self.prfn,width=11).grid(row=0,column=1)
        lb(u4,text='角色类型:').grid(row=1)
        self.prftp=tk.StringVar();self.prftp.set('未知')
        lb(u4,textvariable=self.prftp,width=11).grid(row=1,column=1)
        u4.grid(row=0,column=2,sticky='nw')
        ###设置界面
        #设置-游戏界面
        self.sg=tk.Frame();self.st.add(self.sg,text='游戏')
        lb(self.sg,text='运行内存(GB)').grid(row=0)
        #self.mem.get() 游戏运行内存(等于剩余内存GB整除3)
        mem=psutil.virtual_memory().total//1073741824;self.mem=var('mem',mem//4,int)
        scale(self.sg,from_=1,to=mem,width=10,length=400,variable=self.mem).grid(row=0,column=1,columnspan=10)
        #self.isgl=tk.IntVar()
        #checkbt(self.sg,variable=self.isgl,text='默认启用版本隔离').grid(row=0,column=2)
        self.deepbq=var('deepbq',0,int)
        lb(self.sg,text='补全文件').grid(row=1)
        radiobt(self.sg,variable=self.deepbq,text='快速',value=0).grid(row=1,column=1)
        radiobt(self.sg,variable=self.deepbq,text='深度(硬盘不好会卡好久)',value=1).grid(row=1,column=2,columnspan=4)
        lb(self.sg,text='游戏目录').grid(row=2)
        bt(self.sg,text='选择',command=self.choose_d).grid(row=2,column=1)
        bt(self.sg,text='重置',command=self.resetd).grid(row=2,column=2)
        bt(self.sg,text='设为官方启动器目录',command=self.resetd_default).grid(row=2,column=4,columnspan=6)
        self.d=var('d','.minecraft')
        lb(self.sg,textvariable=self.d,width=50,anchor='w').grid(row=2,column=10,columnspan=10,sticky='w')
        #设置-启动器界面
        self.sl=tk.Frame();self.st.add(self.sl,text='启动器')
        lb(self.sl,text='下载源').grid(row=0)
        self.isu=var('isu',0,int)#self.isu.get() 下载源
        radiobt(self.sl,variable=self.isu,value=0,text='官方').grid(row=0,column=1)
        radiobt(self.sl,variable=self.isu,value=1,text='国内').grid(row=0,column=2)
        self.upd=var('upd',1,int)
        checkbt(self.sl,variable=self.upd,text='启动时检查更新').grid(row=0,column=3)
        lb(self.sl,text='下载线程数').grid(row=1)
        self.thd=var('thread',128,int)#self.thd.get() 下载线程数
        scale(self.sl,from_=8,to=256,width=10,length=400,resolution=8,variable=self.thd).grid(row=1,column=1,columnspan=10)
        sg1=lbfrm(self.sl,text='java列表')
        self._js=tk.Scrollbar(sg1,orient='vertical');self._js.pack(fill='y',side='right')
        self.jvls=lsx(sg1,height=5,width=60,yscrollcommand=self._js.set);self.jvls.pack(side='left')
        self._js.config(command=self.jvls.yview)
        sg1.grid(row=2,columnspan=5)#self.jvls:listbox java列表
        bt(self.sl,text='下载java',command=self.dljava).grid(row=2,column=5)
        #关于界面
        lb(self.ab,text=f'###########{self.text}###########').grid(sticky='w')
        lb(self.ab,text='作者:_MhwsChina_').grid(sticky='w')
        lb(self.ab,text='项目:https://github.com/MhwsChina/MhCraft').grid(sticky='w')
        lb(self.ab,text=f'版本:{self.ver}').grid(sticky='w')
        lb(self.ab,text='开源协议:GPL-3.0').grid(sticky='w')
        if 'b' in self.ver:lb(self.ab,text='注:该版本为测试版,可能会出现部分问题,你可以前往github进行反馈').grid(sticky='w')
        lb(self.ab,text='注:若更新下载太慢或无法更新,可前往https://wwbxb.lanzouw.com/b00yb7zrij进行下载,提取密码为2026').grid(sticky='w')
        bt(self.ab,text='检查更新',command=self.checkupdate).grid(sticky='w')
        ###end
    def showt(self):
        t=int(time.time())
        if t-getjs(('t1',0))>=3600*24*7:
            if not mess.askokcancel('公告',self.text+'\n提示:按下"取消"一周内不再显示'):setjs(('t1',t))
    def export(self):
        self.noadd('导出整合包')
    def checkupdate(self,show=1):
        t=time.strftime('%Y-%m-%d',time.localtime())
        if getjs(('t',0))==t and not show:print('今天已经检查过更新了');return
        setjs(('t',t))
        try:url,size,fn=getupdate(self.ver,_zip='.py' in sys.argv[0])
        except Exception as ex:mess.showerror('错误','检查更新时遇到了以下错误:'+str(ex))
        if not url:
            if show:mess.showwarning('警告','已是最新版本了!')
            else:print('已是最新版本了!')
            return False
        if not '.py' in sys.argv[0]:
            #shutil.move(sys.argv[0],'mhc/RemoveMe')
            mess.showinfo('将自动下载','发现可用更新')
            try:self.dlfile(url,'mhc/upd',chunk_size=1024,timeout=10,rs=1)
            except Exception as ex:mess.showerror('下载失败','不好!下载发生了错误!({ex})\n请重试或前往https://wwbxb.lanzouw.com/b00yb7zrij手动下载,提取密码为2026');return 0
            os.rename(sys.argv[0],'mhc/RemoveMe')
            if 'zip'in fn:extzfa('mhc/upd','./')
            else:os.rename('mhc/upd',sys.argv[0])
            mess.showinfo('提示','更新完成,请重启程序!');os._exit(0)
        else:mess.showinfo('MhDown','检测到以源码形式运行,将为你下载最新版本的压缩包!');self.dlfile(url,'最新版源代码压缩包.zip',chunk_size=1024)
        return 1
    def dljava(self):
        rp=self.getrp()
        url='https://launchermeta.mojang.com/v1/products/java-runtime/2ec0cc96c44e5a76b9c8b7c39df7210883d12871/all.json'
        if rp:url=url.replace('launchermeta.mojang.com',rp)
        osn1=fmosn(self.choose_list('windows','linux','mac-os',text='请选择系统',default=getosname().replace('osx','mac-os')))#;print(osn1);return
        d=urljson(url,timeout=5)[osn1];name=self.choose_list(*(i for i in d),text='请选择版本')
        url1=d[name][0]['manifest']['url']
        if rp:url1=url1.replace('piston-meta.mojang.com',rp)
        self.dl.dls+=getjavaf(name,p='mhc/java'+getosname(),d=urljson(url1))
        self.startdl(1,title='下载java')
        self.loadjava()
    def resr(self):
        if not self.srs:self.srs=tuple(fmsearch(nlimit='mod',url=self.getmu()));
        self.resr1()
        self.d1.config(text='下载列表')
        self.dll.delete(0,'end')
        for i in self.srs:
            self.dll.insert('end',i[1])
    def srch(self):
        self.srs=tuple(fmsearch(self.src.get(),page=int(self.srp.get()),nlimit=self.srtp,url=self.getmu()))
        self.resr1();self.resr()
    def resr1(self):
        self.d1.config(text='下载列表')
        self.step=0
        self.srbt.config(text='选择')
    def getmu(self):return 'mod.mcimirror.top/modrinth' if self.isu.get() else 'api.modrinth.com'
    def getmu1(self):return 'mod.mcimirror.top' if self.isu.get() else 'cdn.modrinth.com'
    def dlmod(self):
        if self.step==0:
            print(self.srs[self.getscdl()][0:2])
            self.srid,title,self.srmcl,icon=self.srs[self.getscdl()]
            self.srprj=getprjv2(self.srid,self.getmu())
            self.srmcl,self.srml=self.srmcl[::-1],fmprjml(self.srprj)
            self.step=1
            if self.srml!=['minecraft']:
                self.d1.config(text='模组加载器')
                self.dll.delete(0,'end')
                for i in self.srml:
                    self.dll.insert('end',i)
                return
        if self.step==1:
            if self.srml!=['minecraft']:self.srm=self.srml[self.getscdl('请在左侧选择加载器!')]
            else:self.srm=None
            print(self.srm)
            self.step=2
            self.d1.config(text='mc版本')
            self.dll.delete(0,'end')
            for i in self.srmcl:
                self.dll.insert('end',i)
            return
        if self.step==2:
            self.srmc=self.srmcl[self.getscdl('请在左侧选择mc版本!')]
            print(self.srmc)
            self.srprj1=sorted(fmprjv2(self.srprj,self.srmc,self.srm),key=lambda i:i[2],reverse=True)
            self.d1.config(text='资源版本')
            self.dll.delete(0,'end')
            self.srbt.config(text='下载')
            for i in self.srprj1:
                self.dll.insert('end',i[1])
            self.step=3;return
        if self.step==3:
            srfl=self.srprj1[self.getscdl('请在左侧选择资源版本!')][0][0]
            print(srfl)
            mkdir(self.d.get(),'versions')
            sv=filedialog.asksaveasfilename(initialdir=pj(self.d.get(),'versions'),initialfile=srfl['filename'])
            if not sv:return
            url=srfl['url'].replace('cdn.modrinth.com',self.getmu1())
            print(url,sv);self.dlfile(url,sv,join=0,chunk_size=2048)
            self.resr1();self.resr()
    def instml(self):
        ver=self.getscver()
        if '无' not in self.ml.get():mess.showerror('错误',f'无法安装!该版本已经安装过{self.ml.get()}了!\n若要更新,请点击"更新"按钮');return
        try:self.reg[self.scm.get()](ver)
        except Exception as ex:mess.showerror('错误','安装时发生了错误:'+str(ex));raise
    def updml(self):
        ver=self.getscver()
        if '无' in self.ml.get():mess.showerror('错误','无法更新!更新操作只能对安装过模组加载器的版本使用!\n若要安装,请点击"安装"按钮');return
        #if self.scm.get() not in self.ml.get():mess.showerror('错误',f'无法更新!该版本已经安装过其他的{self.ml.get()}了!');return
        try:self.reg[self.ml.get()[6:]](ver,upd=1)
        except Exception as ex:mess.showerror('错误','安装时发生了错误:'+str(ex));raise
    def instfab(self,ver,upd=0):
        d=self.d.get();v1,vd,fbv=ver+'-fabric',readv(ver,d),None
        if upd:v1,ver,fbv=ver,vd['inheritsFrom'] if 'inheritsFrom' in vd else vd['clientVersion'],findver(fmlver(vd)['fabric'])
        url=self.u+'/fabric-meta' if self.isu.get() else 'meta.fabricmc.net'
        lt=latest_fabricloader(url)
        if fbv:
            if fbv>=findver(lt):raise RuntimeError('已经是最新版了')
            else:print(fbv,'<',lt);self.rmmc1(v1,rm=0)
        v=instfabric(ver,lt,url,d,v1)
        self.remcl();mess.showinfo('提示',v1+'安装完成')
    def instquilt(self,ver,upd=0):
        d=self.d.get();v1,vd,fbv=ver+'-quilt',readv(ver,d),None,None
        if upd:v1,ver,fbv=ver,vd['inheritsFrom'] if 'inheritsFrom' in vd else vd['clientVersion'],findver(fmlver(vd)['quilt'])
        #url=url=self.u+'/quilt-meta' if self.isu.get() else 'meta.quiltmc.net'
        lt=latest_quiltloader()
        if fbv:
            if fbv>=findver(lt):raise RuntimeError('已经是最新版了')
            else:print(fbv,'<',lt);self.rmmc1(v1,rm=0)
        v=instquilt(ver,lt,d=d,v1=v1)
        self.remcl();mess.showinfo('提示',v1+'安装完成')
    def instopti(self,ver,upd=0):
        if not mess.askokcancel('提示','安装即将开始,程序可能会未响应,请勿关闭,这属于正常现象!\n是否确认安装OptiFine?'):return
        d=self.d.get();vd,tag,opv=readv(ver,d),None,None
        if upd:ov,ver,opv=ver,vd['inheritsFrom'] if 'inheritsFrom' in vd else vd['clientVersion'],fmlver(vd)['optifine']
        url,instp=opdlurl(ver),pj('mhc/temp','optifine-'+ver+'.jar')
        if opv:
            nv='_'.join(url.split('OptiFine_')[-1].split('.jar')[0].split('_')[1:])
            if opv>=nv:raise RuntimeError('已经是最新版了')
            else:print(opv,'<',nv);tag=f'{ver}-OptiFine_{nv}'
        if not os.path.exists(instp):self.dlfile(url,instp,tishi=0,chunk_size=16384)
        self.bqwj(ver,chsha1=1,join=1);java=self.getjava()
        mess.showinfo('安装即将开始第二步','程序将会未响应,弹出黑色窗口并闪出一些文字,这是正常的,请勿关闭!否则将会安装失败,游戏将无法启动!\n整个过程需要1至两分钟,请耐心等待!')
        instoptifine(instp,java,d)
        if tag:self.rmmc1(ov,rm=0);mergemc(ov,tag,d)
        self.remcl();mess.showinfo('提示','安装完成!')
    def instfg(self,ver,upd=0):
        mess.showinfo('提示','安装即将开始,程序可能会未响应,请勿关闭,这属于正常现象!')
        d=self.d.get();vd,fgv,v1=readv(ver,d),None,ver+'-forge'
        if upd:v1,ver,fgv=ver,vd['inheritsFrom'] if 'inheritsFrom' in vd else vd['clientVersion'],findver(fmlver(vd)['forge'])
        url,lt=forgedlurl(ver,self.u if self.isu.get() else 'files.minecraftforge.net')
        if fgv:
            if fgv>=findver(lt.split('-')[1]):raise RuntimeError('已经是最新版了')
            else:print(fgv,'<',lt);self.rmmc1(v1,rm=0)
        instp=pj('mhc/temp','forge'+lt+'.jar')
        if not os.path.exists(instp):self.dlfile(url,instp,tishi=0,chunk_size=16384)
        lzp,fvd=instforge_part1(instp,d,v1)[0:2]
        if 'libraries' in fvd:self.bqwj(v1,chsha1=1,vd=fvd,join=0)
        self.bqwj(v1,chsha1=1,join=1);java=self.getjava()
        mess.showinfo('安装即将开始第二步','程序将会未响应,弹出黑色窗口并闪出一些文字,这是正常的,请勿关闭!否则将会安装失败,游戏将无法启动!\n整个过程需要1至两分钟,请耐心等待!')
        instforge_part2(instp,lzp,fvd,java,d)
        self.remcl();mess.showinfo('提示',v1+'安装完成')
    def instneo(self,ver,upd=0):
        mess.showinfo('提示','安装即将开始,程序可能会未响应,请勿关闭,这属于正常现象!')
        d=self.d.get();vd,fgv,v1=readv(ver,d),None,ver+'-neoforge'
        if upd:v1,ver,fgv=ver,vd['inheritsFrom'] if 'inheritsFrom' in vd else vd['clientVersion'],findver(fmlver(vd)['neoforge'])
        url,lt=neodlurl(ver,self.u+'/maven' if self.isu.get() else 'maven.neoforged.net/releases')
        if fgv:
            if fgv>=findver(lt):raise RuntimeError('已经是最新版了')
            else:print(fgv,'<',lt);self.rmmc1(v1,rm=0)
        instp=pj('mhc/temp','neoforge'+lt+'.jar')
        if not os.path.exists(instp):self.dlfile(url,instp,tishi=0,chunk_size=16384)
        lzp,fvd=instforge_part1(instp,d,v1)[0:2]
        if 'libraries' in fvd:self.bqwj(v1,chsha1=1,vd=fvd,join=1)
        self.bqwj(v1,chsha1=1,join=1);java=self.getjava()
        mess.showinfo('安装即将开始第二步','程序将会未响应,弹出黑色窗口并闪出一些文字,这是正常的,请勿关闭!否则将会安装失败,游戏将无法启动!\n整个过程需要1至两分钟,请耐心等待!')
        instforge_part2(instp,lzp,fvd,java,d)
        self.remcl();mess.showinfo('提示',v1+'安装完成')
    def rnmc(self):
        ver=self.getscver()
        if 'inheritsFrom' not in readv(ver,self.d.get()):mess.showwarning('警告','该版本为原版,无法直接重命名!\n提示:复制该版本后,重命名复制的版本可达到一样的效果');return
        nver=self.input_box(ver)
        p=pj(self.d.get(),'versions',ver)
        os.rename(pj(p,ver+'.json'),pj(p,nver+'.json'))
        try:os.rename(pj(p,ver+'.jar'),pj(p,nver+'.jar'))
        except:pass
        os.rename(p,pj(d,'versions',nver))
        self.remcl()
    def copymc(self):
        ver=self.getscver()
        vd,p=readv(ver,self.d.get()),pj(self.d.get(),'versions')
        if '_copy' in ver:ver=ver.split('_copy')[0]
        txt,i=ver+'_copy',1;tag=os.path.exists(pj(p,txt))
        while tag:
            path=pj(p,txt+str(i))
            if not os.path.exists(path):txt+=str(i);break
            i+=1
        mkdir(p,txt)
        with open(pj(p,txt,txt+'.json'),'w') as f:
            if 'inheritsFrom' in vd:f.write(dumps(vd))
            else:f.write(f'{{"id":"{ver}","inheritsFrom":"{ver}","libraries":[]}}')
        self.remcl();mess.showinfo('提示',f'{txt}已生成!')
    def rmmc(self):
        ver,d=self.getscver(),self.d.get()
        for i in mclist(d):
            if readv(i,d).get('inheritsFrom',None)==ver:
                mess.showerror('错误','该版本被复制过或安装过模组加载器,导致有其他版本为该版本的附属版本!\n要删除附属版本才能删除该版本,否则会导致附属版本无法启动!');return
        if not mess.askokcancel('警告','真的要删除吗?该版本的存档、截图等资源将全部丢失!'):return
        if not mess.askokcancel('警告','再次确认,真的要删除吗?'):return
        self.rmmc1(ver)
    def rmmc1(self,ver,rm=1):
        d=self.d.get()
        for i in listlib(d).items():
            if i[1]==[ver]:
                path=pj(d,'libraries',i[0])
                try:os.remove(path);print('delete',path)
                except Exception as ex:print(ex)
        for i in listass(d).items():
            if i[1]==[ver]:
                path=pj(d,'assets/objects',i[0][0:2],i[0])
                try:os.remove(path);print('delete',path)
                except Exception as ex:print(ex)
        if rm:shutil.rmtree(pj(d,'versions',ver))
        rmemptdir('.minecraft')
        if rm:self.remcl()
    def dlmc(self):
        ver=self.dll.get(self.getscdl())
        #mess.showinfo('提示','按下"确认"开始下载'+ver+',程序会在后台下载')
        self.dl.dls+=dlver(self.vdc,ver,self.d.get(),*self.getrpl())
        self.startdl(1)
        self.remcl()
        mess.showinfo('提示',ver+'下载完毕')
    def runmc(self,rt=0):
        ver,prf,d=self.getscver(),getjs('scprf'),self.d.get()
        if not prf:mess.showwarning('警告','未检测到使用中的角色!\n若没有添加,请在"角色"选项卡内添加并使用\n若已添加,请在"角色"选项卡内选择你要使用的角色并使用');return
        self.bqwj(ver,self.deepbq.get());jvm=self.getmem()
        if 'type' in prf and prf['type']=='mojang':
            try:prf=self.checkprf(prf)
            except Exception as ex:mess.showerror('错误','登陆时发生了错误:'+str(ex)+',可以尝试删除并重新添加该角色,确保账号正确再重试!');raise
            self.bqauthlib()
            srv=getjs(prf['sv'])
            if not srv:srv=auth.fmapi();setjs((prf['sv'],srv))
            jvm+=[f'-javaagent:{os.path.abspath("mhc/authlib-injector.jar")}={prf["sv"]}','-Dauthlibinjector.yggdrasil.prefetched='+srv]
        args,jv=getarg(ver,prf,d,jvm,1)  
        args[0]=os.path.abspath(self.getjava(jv))
        if rt:return args,ver,pj(d,'versions',ver)
        th.Thread(target=mess.showinfo,args=('提示','启动完成,请等待游戏窗口出现!')).start()
        th.Thread(target=sbrun,args=(args,),kwargs={'cwd':pj(d,'versions',ver)}).start()
    def checkprf(self,prf):
        if auth.check(prf['token'],prf['sv']):print('token right,end check token=',prf['token']);return prf
        rf,nprf,tag=auth.refresh(prf['token'],prf['sv']),[],0
        if 'error' in rf:
            new=auth.login(prf['em'],prf['ps'],prf['sv'])
            print('latestprofile=',new)
            for i in new['availableProfiles']:
                if i['id']==prf['uuid']:prf['name'],prf['token'],tag=i['name'],new['accessToken'],1;break
        else:
            prf['token'],new,tag=rf,{'accessToken':rf},1
            print('refresh token=',new)
        for i in allprf():
            if i.get('em','')==prf['em'] and i.get('sv','')==prf['sv']:i['token']=new['accessToken']
            if tag and i.get('uuid')==prf['uuid']:i['name']=prf['name']
            nprf.append(i)
        updprf(nprf)
        if tag:
            if getjs('scprf')['uuid']==prf['uuid']:setjs(('scprf',prf))
            return prf
        else:raise RuntimeError('该角色已经失效')
    def bqauthlib(self):
        if os.path.exists('mhc/authlib-injector.jar'):
            n,v=getjs(('authlib-sha',('sha256','eaf14bc5acffc7d885bd5bd5942b99f36d6299302beae356b2fc5807fe42652b')))
            if chksha('mhc/authlib-injector.jar',mode=n)==v:return
        url='https://bmclapi2.bangbang93.com/mirrors/authlib-injector/' if self.isu.get() else 'https://authlib-injector.yushi.moe/'
        json=urljson(url+'/artifact/latest.json',timeout=10)
        dlurl=json['download_url'];setjs(('authlib-sha',tuple(json['checksums'].items())[0]))
        self.dlfile(dlurl,'mhc/authlib-injector.jar',title='补全文件',chunk_size=1024,timeout=10,tishi=0)
    def outmc(self):
        args,ver,rd=self.runmc(1)
        path='run'+ver+'.bat' if os.name=='nt' else '.sh'
        with open(path,'w') as f:
            f.write(f'cd {"/D " if os.name=="nt" else ""}{os.path.abspath(rd)}\n')
            for i in args:
                if ' ' in i:i='"'+i+'"'
                try:tag;f.write(' ')
                except:tag=1
                f.write(i)
        mess.showinfo('提示',f'启动脚本"{path}"已在启动器所在目录生成!')
    def bqmc(self):
        self.bqwj(self.getscver(),1,join=1)
    def csaves(self):
        ver=self.getscver()
        p=pj(self.d.get(),'versions',ver,'saves')
        if not os.path.exists(p):mess.showerror('错误','存档文件夹不存在!');return
        ls=os.listdir(p)
        if not ls:mess.showwarning('警告','存档文件夹为空,无法操作!');return
        save=self.choose_list(*ls,text='请选择存档')
        ch=self.choose_list('删除','重命名','转移到其他版本',text='选择操作')
        if ch=='删除':
            if not mess.askokcancel('警告','真的要删除吗?该存档将永久消失!'):return
            if not mess.askokcancel('警告','再次确认,真的要删除吗?'):return
            shutil.rmtree(pj(p,save))
            mess.showinfo('提示',save+'已删除!')
        if ch=='重命名':
            n=self.input_box(save)
            os.rename(pj(p,save),pj(p,n))
            mess.showinfo('提示',save+'已重命名为'+n)
        if ch=='转移到其他版本':
            v=self.choose_list(*mclist(self.d.get()),text='请选择版本')
            shutil.move(pj(p,save),pj(self.d.get(),'versions',v,'saves',save))
            mess.showinfo('提示',save+'已移动至'+v)
    def getjava(self,java={'component':'java-runtime-epsilon','majorVersion':25}):
        try:return self.jls[java['majorVersion']]
        except:
            self.dl.dls+=getjavaf(java['component'],rp=self.getrp())
            self.startdl(1,title='下载java')
            self.loadjava()
            return self.jls[java['majorVersion']]
    def bqwj(self,ver,chsha1=1,vd=None,join=1):
        self.dl.dls+=dlver(self.vdc,ver,self.d.get(),*self.getrpl(),vd)
        self.startdl(join,title='补全文件')
    def getrpl(self):return (self.u+'/maven',self.u+'/assets') if self.isu.get() else ('','')
    def getrp(self):return self.u if self.isu.get() else ''
    def getmem(self):return ['java',f'-Xmx{self.mem.get()}g',f'-Xms{self.mem.get()}g']
    def choose_d(self):
        path1=os.path.abspath(self.d.get())
        path=filedialog.askdirectory(initialdir=path1)
        if path and pj(path)!=pj(path1):
            self.d.set(path)
            self.remcl()
    def resetd(self):
        self.d.set('.minecraft')
        self.remcl()
    def resetd_default(self):
        self.d.set(defaultmcpath())
        self.remcl()
    def noadd(self,txt='此'):mess.showinfo('抱歉',txt+'功能还未添加,敬请期待!')
    def choose_list(self,*a,text='请选择',default=None):
        w1,res,row=tk.Toplevel(w),tk.StringVar(),1
        ds=lambda x:w1.destroy()
        lb(w1,text=text).grid(row=0)
        if default:res.set(default)
        for i in a:
            if not default and not res.get():res.set(i)
            radiobt(w1,text=i,variable=res,value=i).grid(row=row,columnspan=2)
            row+=1
        bt(w1,text='确定',command=w1.destroy).grid(row=row)
        bt(w1,text='取消',command=lambda:ds(res.set(''))).grid(row=row,column=1)
        w1.protocol("WM_DELETE_WINDOW",lambda:ds(res.set('')))
        w.wait_window(w1)
        if not res.get():raise RuntimeError('用户取消了操作或输入为空')
        return res.get()
    def input_box(self,default=''):
        w1=tk.Toplevel(w)
        ds=lambda x:w1.destroy()
        res=tk.StringVar();res.set(default)
        entry(w1,textvariable=res).grid(row=0,columnspan=2)
        bt(w1,text='取消',command=lambda:ds(res.set(''))).grid(row=1)
        bt(w1,text='确定',command=w1.destroy).grid(row=1,column=1)
        w1.protocol("WM_DELETE_WINDOW",lambda:ds(res.set('')))
        w.wait_window(w1)
        if not res.get():raise RuntimeError('用户取消了操作或输入为空')
        return res.get()
    def crtprog(self,title='文件下载'):
        a=tk.Toplevel(w);a.title(title);a.resizable(0,0)
        a.protocol("WM_DELETE_WINDOW",lambda:1)
        lb(a,text='剩余').grid(row=0)
        b=tk.StringVar()
        lb(a,textvariable=b).grid(row=0,column=1)
        prg=ttk.Progressbar(a,length=340,mode='indeterminate')
        prg.grid(row=1,columnspan=2);prg.start(100)
        th.Thread(target=self.updprog,args=(a,b)).start()
        w.wait_window(a)
    def updprog(self,a,b):
        while self.dl.threads:
            b.set(len(self.dl.dls)+len(self.dl.threads)+len(wrt))
            sleep(0.1)
        a.destroy()
    def startdl(self,join=0,title='文件下载'):
        t=(self.dl.threads==[])
        self.dl.start(self.thd.get())
        if t:
            #self.crtprog()#if join:self.dl.join()#else:th.Thread(target=self.dl.join).start()
            th.Thread(target=self.dl.join).start()
            if join:self.crtprog(title)
            else:th.Thread(target=self.crtprog,args=(title,)).start()
        else:
            if join:self.dl.join()
    def loadjava(self):
        self.jls=findjava('mhc')
        self.jvls.delete(0,'end')
        for v,p in self.jls.items():
            self.jvls.insert('end',f'{v}->{p}')
    def load(self):
        self.dl,self.u,self.vdc=xcdl(),'bmclapi2.bangbang93.com',{}
        try:self.loadprf_to_ui()
        except:pass
        if not os.path.exists(self.d.get()):
            try:os.makedirs(self.d.get())
            except:
                self.d.set('.minecraft')
                mess.showwarning('警告','游戏目录不存在!已自动重置!')
        self.remcl();self.loadjava()
        if self.isu.get():vdurl='https://'+self.u+'/mc/game/version_manifest.json'
        else:vdurl='http://launchermeta.mojang.com/mc/game/version_manifest.json'
        self.vdc=urljson(vdurl,timeout=5);self.redl()
        try:os.remove('mhc/RemoveMe')
        except:pass
        try:os.remove('mhc/upd')
        except:pass
        try:shutil.rmtree('mhc/temp')
        except:pass
        try:shutil.rmtree('logs')
        except:pass
        self.showt()
        if self.upd.get():self.checkupdate(0)
    def redl(self):
        self.resr1()
        self.dll.delete(0,'end')
        for i in findmcv(self.vdc,self.dlt.get()):
            self.dll.insert('end',i['id'])
    def loadprf_to_ui(self):
        oldprf=getjs('scus')
        if oldprf:setjs(('scprf',oldprf),'scus')
        prfs,name,prf=allprf(),getjs('name'),getjs(('scprf',{}))
        if prf and prf not in prfs:prf={};setjs(('scprf',{}))
        if prf:
            self.prfn.set([prf['name']])
            self.prftp.set({'msa':'微软','mojang':'第三方','legacy':'离线'}[(prf['type'] if 'type' in prf else 'legacy').lower()])
        else:self.prfn.set('无'),self.prftp.set('未知')
        if name:
            self.addlprf(name)
            setjs('name','uuid','token')
        self.prfl.delete(0,'end')
        for i in prfs:
            self.prfl.insert('end',i['name'])
    def useprf(self):
        if not allprf():mess.showerror('错误','你没添加角色!');return
        sc=self.prfl.curselection()
        if not sc:mess.showerror('错误','请在左侧选择一个角色!');return
        setjs(('scprf',allprf()[sc[0]]))
        self.loadprf_to_ui()
    def addlprf(self,prfn=None,data=None):
        if not data:
            uuid=caluuid(prfn)
            data={'name':prfn,'uuid':uuid,'token':uuid}
        if data in allprf():return 1
        addprf(data)
    def addprf(self):
        global js
        prfn,sv,em,ps=self.adprf.get(),self.adsv.get(),self.adem.get(),self.adps.get()
        if prfn:
            if not prfn:mess.showwarning('警告','角色名长度不能小于1且不能为空!');return
            for i in prfn.lower():
                if i not in 'qwertyuiopasdfghjklzxcvbnm_1234567890':
                    mess.showerror('输入不正确','角色名除了英文、数字、英文下划线"_"之外都不能包含!');return
            self.adprf.set('')
            if self.addlprf(prfn):mess.showerror('错误','该角色已存在!');return
            self.loadprf_to_ui()
        elif sv and em and ps:
            try:prfs=self.addtu(em,ps,sv)
            except Exception as ex:mess.showerror('错误','发生了错误:'+str(ex));return
            #mess.showinfo('抱歉','添加第三方角色还无法使用,后续会添加!你可以先使用离线角色!')
            self.adem.set('');self.adps.set('')
            self.loadprf_to_ui()
            mess.showinfo('完成','角色'+','.join(prfs)+'已添加')
        else:mess.showerror('错误','请填写完整的用户信息!')
    def addtu(self,em,ps,sv):
        res=auth.login(em,ps,sv);print(res)
        if 'error' in res:raise RuntimeError(res['errorMessage'])
        allu,u1=res['availableProfiles'],[]
        if allu==[]:raise RuntimeError('没有添加过角色!')
        for u in allu:
            data={'name':u['name'],'token':res['accessToken'],'uuid':u['id'],'type':'mojang','em':em,'ps':ps,'sv':sv}
            if data in allprf():continue
            addprf(data);u1.append(u['name'])
        return u1
    def rmprf(self):
        if not allprf():mess.showerror('错误','你没添加角色!');return
        sc=self.prfl.curselection()
        if not sc:mess.showerror('错误','请在左侧选择一个角色!');return
        if not mess.askyesno('再次确认','真的要删除该角色吗?'):return
        rmprf(sc[0])
        self.loadprf_to_ui()
    def remcl(self):
        self.vl.delete(0,'end')
        for i in mclist(self.d.get()):
            self.vl.insert('end',i)
    def getscver(self,rs=1):
        sc=self.vl.curselection()
        if rs and not sc:mess.showerror('错误','请在左侧选择mc版本!');raise RuntimeError('未选择mc版本!')
        return self.vl.get(sc[0])
    def getscdl(self,text='请在左侧选择下载内容!'):
        sc=self.dll.curselection()
        if not sc:mess.showerror('错误',text);raise RuntimeError(text)
        return sc[0]
    def openvfd(self,name):
        try:openfd(pj(self.d.get(),'versions',self.getscver(),name))
        except FileNotFoundError:mess.showerror('错误','该文件夹不存在!')
    def setinfo(self,*a):
        try:vd=readv(self.getscver(0),self.d.get())
        except:return
        self.v1.set('版本号:'+vd['id']);ml=fmlver(vd)
        if ml:
            for i in ml:self.ml.set('模组加载器:'+i),self.mlv.set('加载器版本:'+ml[i])
        else:self.ml.set('模组加载器:无');self.mlv.set('加载器版本:无')
    def dlfile(self,url,path,title='文件下载',join=1,chunk_size=32768,timeout=100,tishi=1,rs=0):
        a=tk.Toplevel(w);a.title(title);a.resizable(0,0)
        a.protocol("WM_DELETE_WINDOW",lambda:1)
        t,z=tk.IntVar(),tk.IntVar()
        lb(a,textvariable=t).grid(row=0)
        lb(a,text='/').grid(row=0,column=1)
        lb(a,textvariable=z).grid(row=0,column=2)
        prg=ttk.Progressbar(a,length=340,mode='determinate')
        prg.grid(row=1,columnspan=3)#prg.start(100)
        th.Thread(target=self.dlfilep,args=(url,path,a,t,z,prg,chunk_size,timeout,tishi,rs)).start()
        if join:w.wait_window(a)
    def dlfilep(self,u,p,a,t,z,prg,chunk_size=32768,timeout=100,tishi=1,rs=0):
        mkdir(os.path.split(p)[0]);print('dl',u)
        while 1:
            try:
                rs=req.get(u,timeout=timeout,verify=False,headers=hd,stream=True)
                if rs.status_code!=200:print(f'{u},resp code!=200')
                size=int(rs.headers.get('Content-Length',0));z.set(size)
                if size:prg['maximum']=size
                else:prg['mode']='indeterminate';prg.start(100)
                with open(p,'wb') as f:
                    for c in rs.iter_content(chunk_size=chunk_size):
                        f.write(c)
                        tt=f.tell();t.set(tt)
                        if size:prg['value']=tt
                break
            except Exception as ex:
                if rs:raise
                print(ex)
        a.destroy()
        if tishi:mess.showinfo('提示','下载完成!')
mui=ui()
th.Thread(target=mui.load,name='loading').start()
w.mainloop()
os._exit(0)
