import requests as req
#modrinth爬取,作者_MhwsChina_
#下载:https://cdn.modrinth.com/data/{project_id}/versions/{id}/{filename}
#获取mod的mc版本(所有版本)https://api.modrinth.com/v2/project/{mod}/version
#搜索:https://api.modrinth.com/v2/search?limit={搜索数量}&index={排序方式}&query={搜索文本}&page={搜索页码}&new_filters=project_types%20%3D%20{搜索内容}
#搜索文本若无去掉&query=
'''
排序方式(index)
relevance关联性
downloads下载量
follows点赞数
newest发布日期
updated更新日期
搜索内容(nlimit)
mod模组
resourcepack资源包
datapack数据包
shader光影包
modpack整合包
'''
def fmsearch(text=None,limit=20,index='relevance',page=1,nlimit=None,url='api.modrinth.com'):
    print('search',text,'num=',limit,'page=',page,'type=',nlimit,'from=',url)
    url=url=f'https://{url}/v2/search?limit={limit}&index={index}&offset={(page-1)*limit}'
    if text:url+=f'&query={text}'
    if nlimit:url+=f'&new_filters=project_types = '+nlimit
    for i in req.get(url,timeout=1000).json()['hits']:
        yield i['project_id'],i['title'],i['versions'],i['icon_url']
def getprjv2(project_id,url='api.modrinth.com'):
    print('getprjv2',project_id,'url=',url)
    url=f'https://{url}/v2/project/{project_id}/version'
    return req.get(url,timeout=1000).json()
def fmprjv2(json,mcv,loader=None):
    for i in json:
        if mcv in i['game_versions'] and (loader in i['loaders'] if loader else 1):
            yield i['files'],i['name'],i['date_published']
def getprjv3(project_id,url='api.modrinth.com'):
    print('getprjv3',project_id,'url=',url)
    url=f'https://{url}/v3/project/{project_id}/version'
    return req.get(url,timeout=1000).json()
def fmprjv3(json,mcv,loader=None,version_number=None):
    for i in json:
        if mcv in i['game_versions'] and (loader in i['loaders'] if loader else 1) and (i['version_numver']==version_number if version_number else 1):
            yield i['files'],i['name'],i['date_published'],i['dependencies']
def getfilev3(ids,url='api.modrinth.com'):#此处ids为作品id的列表
    url=f'https://{url}/v3/versions?ids={ids}'
    return req.get(url,timeout=1000).json()
def fmprjml(json):
    lds=()
    for i in json:
        #mcs+=tuple(j for j in i['game_versions'] if j not in mcs)
        lds+=tuple(j for j in i['loaders'] if j not in lds)
    return lds
def search(text=None,limit=20,index='downloads',page=1,nlimit=None):
    url=f'https://api.modrinth.com/v2/search?limit={limit}&index={index}&page={page}'
    if text:url+=f'&query={text}'
    if nlimit:url+=f'&new_filters=project_types%20%3D%20'+nlimit
    return req.get(url,timeout=timeout).json()['hits']     
def formatsc(sd):
    for i in sd:
        yield i['title'],i['versions'],i['project_id'],i['icon_url']
'''
fmsearch(文本,数量,排序方式,页码,搜索内容(以上均可选)) -> generator
[
    (
        project_id->str,
        资源标题->str,
        支持的mc版本->str,
        图标网址->str
    ),
    ......
]
getprjv2返回版本信息v2
fmprjv2(版本信息v2,mc版本,加载器(可选)) -> generator
[
    (
        文件列表->list[
            文件信息->dict{
                'url':下载地址->str,
                'filename':文件名->str,
                'hashes':hash值->dict{'sha1':sha1值->str,......}
            },
            ......
        ],
        资源版本名->str,
        发布日期->str
    )
    ......
]
getprjv3返回版本信息v3
fmprjv3(版本信息v3,mc版本,加载器(可选),资源版本(可选)) -> generator
[
    (
        文件列表->list[
            文件信息->dict{
                'url':下载地址->str,
                'filename':文件名->str,
                'hashes':hash值->dict{'sha1':sha1值->str,......}
            },
            ......
        ],
        资源版本名->str,
        发布日期->str,
        前置资源->dict{
            'version_id':前置资源版本(可能为None)->str,
            'project_id':前置资源id->str,
            'file_name':应保存到本地的文件名->str,
            'dependency_type':是否必需(若为"required"说明必需,否则为可选)->str
        }
    )
    ......
]
search(文本,数量,排序方式,页码,搜索内容(以上均可选)) -> list
[
    版本信息过长省略，包含project_id,作者,名称,加载器列表,支持的mc版本等,自己去试
    ......
]
formatsc(sd) -> generator #sd=tuple(search())
[
    (
        资源标题->str,
        支持的mc版本->list['1.20.1','1.21'......],
        project_id->str,
        图标网址->str
    )
    ......
]
'''
