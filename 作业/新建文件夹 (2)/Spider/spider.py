import json
import requests
import re
import urllib
from bs4 import *
import time
import random
import funcLib

myurl = "http://music.163.com/playlist?id=2857550594"
headers = {"Host":" music.163.com",
"User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
}
request = urllib.request.Request(myurl,headers=headers)
response = urllib.request.urlopen(request)
#不decode的话text是十六进制，不是中文
html = response.read().decode('utf-8','ignore')
soup = BeautifulSoup(html)


song_id_list = []
name_list = []

for item in soup.ul.children:
    time.sleep(random.uniform(1.1,3.5))
    #取出歌单里歌曲的id  形式为：/song?id=11111111
    song_id = item('a')[0].get("href",None)
    #歌曲名称
    song_name = item.string
    #利用正则表达式提取出song_id的数字部分sid
    pat = re.compile(r'[0-9].*$')#提取模式为全都为数字的字符串
    sid = re.findall(pat,song_id)[0]#提取歌曲ID
    #打印歌曲ID以及名称
    print(sid+"-"+song_name)
    song_id_list.append(sid)
    name_list.append(song_name)


# --------------------------------------------------------------


def requests_html(url):
    # 我们增加一个headers，如果不加，网易云会认为我们是爬虫程序，从而拒绝我们的请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
    }
    # 利用requests模块请求网易云的歌词页面
    demo = requests.get(url, headers=headers)
    # 如果正确获取到网页则返回文本内容
    if demo.status_code == 200:
        return demo.text
    else:
        print(url, "请求失败")


def parser_html(txt):
    # 这里我就不异常处理了，直接获取内容，eval函数把文本内容转换为字典
    dic = eval(text)
    print("文本当前的数据类型是:", type(dic))
    # 字典是键值对类型的，获取歌词部分
    lyric = dic['lyric']
    # 通过观察文本内容发现，文本每行以 '\n'字符结束，用文本的split切割\n字符获取每行的歌词内容
    for line in lyric.split('\n'):
        print(line)


for i in range(0, len(song_id_list)):
    time.sleep(random.uniform(1.1, 3.5))
    # url中的信息就是歌词链接，可以试试你自己的链接，更改ID即可
    url = 'http://music.163.com/api/song/media?id=' + str(song_id_list[i])
    # text里就是网页的内容了
    text = requests_html(url)
    # 把text里的内容交给parser_html函数解析

    print(text)
    f = open('./data/' + name_list[i] + '.txt', 'w', encoding='utf-8')
    words = funcLib.processChineseSentence(text)

    print(words)
    f.write(words)
    f.close()
