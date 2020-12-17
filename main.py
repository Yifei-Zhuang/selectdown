import requests
import re
from requests import session
import os
from urllib import parse
import multiprocessing
from time import sleep
totalerr = []
repeat =0
proxies = {
    'http':'http://49.85.48.102:21866'
}
def getandsavepic(url):
    global repeat
    repeat+=1
    global totalerr
    temp = session()
    global headers
    try:
        page = temp.get(url = url,headers = headers,proxies  = proxies)
        titleregex = re.compile('"illustTitle":"(.*?)",')
        title = re.findall(titleregex,page.text)
        print(title)
        regex = re.compile('"regular":"(.*?)","original"')
        getpic = re.findall(regex,page.text)
        print(getpic[0])
        if title[0] =="****":
            title[0] = url
        print("开始下载第%d组画"%repeat+title[0])
        headers['referer'] = url
        sleep(1)
        picdata = temp.get(url = getpic[0],headers = headers,proxies  = proxies).content
        with open("./img/{}.{}".format(title[0],getpic[0][-3:]),'wb') as fp:
            fp.write(picdata)
        print(title[0]+"下载成功！！！！！")
    except FileNotFoundError:
        pass

print("please input the keyword you want to search")
tar = input()
if (not os.path.exists('/Users/fuko/Desktop/img/')):
    os.mkdir('/Users/fuko/Desktop/img')
    os.mkdir('/Users/fuko/Desktop/img/'+tar)
tar = parse.quote(tar)
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'referer': 'https://www.pixiv.net/tags/{}/artworks?s_mode=s_tag'.format(tar)
}
print("input the ini page and end page you want to download")
ini,pagenum  = map(int,input().split())
print("请输入想要开启的线程数（数量越多越快，但是可能ip会被封）")
poolnum = int(input())
pool = multiprocessing.Pool(poolnum)
for count in range(ini,pagenum+1):
    url ='https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag&type=all&lang=zh'.format(tar,tar,count)
    page = requests.get(url =url,headers =headers,proxies  = proxies)
    page.encoding = 'utf-8'
    regex = re.compile('"id":"(\d+)","title"')
    idlist = re.findall(regex,page.text)
    idlist = ['https://www.pixiv.net/artworks/' + temp for temp in idlist]
    print(idlist)
    pool.map(getandsavepic,idlist)
