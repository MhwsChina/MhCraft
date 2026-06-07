import requests as req
from re import findall
from os.path import split
import sys
auther='MhwsChina'
project='MhCraft'
url=f'https://api.github.com/repos/{auther}/{project}/releases'
def getupdate(nowver,find='mhcraft.exe',_zip=0):
    json=req.get(url,timeout=10,verify=False).json()
    newver,nowver=None,int("".join(findall(r"\d+",nowver)))
    i=json[0]
    newver,dic=int(''.join(findall(r"\d+",i['tag_name']))),i
    if nowver>=newver or not newver:return 0,0,0
    if _zip:return dic['zipball_url'],0,dic['tag_name']+'.zip'
    for i in dic['assets']:
        if i['name']==find:
            return i['browser_download_url'],i['size'],split(sys.argv[0])[1]
    return 0,0,0
