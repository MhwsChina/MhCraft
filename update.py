import requests as req
from re import findall
from os.path import split
import sys
from tools import isarm,getosname
auther='MhwsChina'
project='MhCraft'
url=f'https://api.github.com/repos/{auther}/{project}/releases'
finds={'linux':('mhcraft-linux','mhcraft-linux-x64.zip'),
    'windows':('mhcraft.exe','mhcraft-windows-x64.zip'),
    'osx':('mhcraft-macos','mhcraft-macos-x64.zip'),
    'windows-arm':('mhcraft-arm64.exe','mhcraft-windows-arm64.zip'),
    'macos-arm':('mhcraft-macos-arm64','mhcraft-macos-arm64.zip')
}
def getupdate(nowver,_zip=0):
    find=finds[getosname()+('-arm' if isarm else '')]
    json=req.get(url,timeout=10,verify=False).json()
    newver,nowver=None,float(".".join(findall(r"\d+",nowver)))
    i=json[0]
    newver,dic=float('.'.join(findall(r"\d+",i['tag_name']))),i
    if nowver>=newver or not newver:return 0,0,0
    if _zip:return dic['zipball_url'],0,dic['tag_name']+'.zip'
    for i in dic['assets']:
        if i['name'] in find:
            return i['browser_download_url'],i['size'],split(sys.argv[0])[1]
    return 0,0,0
