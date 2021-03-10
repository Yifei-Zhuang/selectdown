import requests
import re
from requests import session
import os
import multiprocessing
from time import sleep


class DownPic:
    proxies = {
        # 这是我找到的一个免费的ip地址，你也可以使用自己的ip地址
        'http': 'http://49.85.48.102:21866'
    }
    headers = {
        # 设置请求头
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.88 Safari/537.36',
        'referer': 'https://www.pixiv.net/tags/{}/artworks?s_mode=s_tag'
    }
    tar = ''
    # 存储下载失败的图片
    totalerr = []
    # print提示信息的时候使用
    repeat = 1
    # 多进程
    pool = ''

    # 获取url列表并传给下载器
    def geturllist(self, thispagenum):
        url = 'https://www.pixiv.net/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag&ty\
                pe=all&lang=zh'.format(tar, tar, thispagenum)
        page = requests.get(url=url, headers=downmachine.headers)
        page.encoding = 'utf-8'
        regex = re.compile('"id":"(\d+)","title"')
        idlist = re.findall(regex, page.text)
        urllist = ['https://www.pixiv.net/artworks/' + temp for temp in idlist]
        print(urllist)
        self.from_urllist_download(urllist)

    # 通过传入的url获取图片并保存
    def getandsavepic(self, url):
        temp = session()
        try:
            page = temp.get(url, headers=self.headers, proxies=self.proxies)
            titleregex = re.compile('"illustTitle":"(.*?)",')
            title = re.findall(titleregex, page.text)
            print(title)
            regex = re.compile('"regular":"(.*?)","original"')
            getpic = re.findall(regex, page.text)
            print(getpic[0])
            if title[0] == "****":
                title[0] = url
            print("开始下载第%d组画" % self.repeat + title[0])
            self.headers['referer'] = url
            sleep(1)
            picdata = temp.get(url=getpic[0], headers=self.headers, proxies=self.proxies).content
            with open("./img/{}/{}.{}".format(self.tar, title[0], getpic[0][-3:]), 'wb') as fp:
                fp.write(picdata)
            print(title[0] + "下载成功！！！！！")
            self.repeat += 1
        except FileNotFoundError:
            self.totalerr.append(url)

    def __init__(self, mytar, nums):
        self.tar = mytar
        self.pool = multiprocessing.Pool(nums)
        self.headers['referer'] = mytar

    def from_urllist_download(self, urllist):
        self.pool.map(self.getandsavepic, urllist)

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']

        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)

    # 在当前目录的子目录创建图片文件夹
    @staticmethod
    def gendir():
        if not os.path.exists('./img'):
            os.mkdir('./img')
            os.mkdir('./img/' + tar)


if __name__ == '__main__':
    # 获取关键字
    print("您要查询的关键字是什么")
    tar = input()

    print("请输入下载图片的起止页面")
    ini, pagenum = map(int, input().split())

    # 获取线程数用来初始化downmachine对象
    print("请输入想要开启的线程数（数量越多越快，但是可能ip会被封(比如我自己)）")
    poolnum = int(input())

    # 初始化下载器对象
    downmachine = DownPic(tar, poolnum)

    # 创建文件夹
    downmachine.gendir()

    # 通过循环获取指定页数的图片
    for count in range(ini, pagenum + 1):
        downmachine.geturllist(count)
    print("{}幅画下载失败" + "".join(downmachine.totalerr))
