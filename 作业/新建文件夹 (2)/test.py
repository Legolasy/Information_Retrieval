import requests
def requests_html(url):
    # 我们增加一个headers，如果不加，网易云会认为我们是爬虫程序，从而拒绝我们的请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
    }
    # 利用requests模块请求网易云的歌词页面
    demo = requests.get(url, headers=headers)
    # 如果正确获取到网页则返回文本内容
    if demo.status_code == 200:
        return  demo.text
    else:
        print(url,"请求失败")
def parser_html(txt):
    # 这里我就不异常处理了，直接获取内容，eval函数把文本内容转换为字典
    dic = eval(text)
    print("文本当前的数据类型是:",type(dic))
    # 字典是键值对类型的，获取歌词部分
    lyric = dic['lyric']
    for line in lyric.split('\n'):
        temp=str(line)
        temp1=temp.split(']')
        result2txt = str(temp1[1])  # data是前面运行出的数据，先将其转为字符串才能写入
        with open('result.txt', 'a') as file_handle:  # .txt可以不自己新建,代码会自动新建
            file_handle.write(result2txt)  # 写入
            file_handle.write('\n')

        print(temp1[1])

if __name__ == '__main__':

    # url中的信息就是歌词链接，可以试试你自己的链接，更改ID即可
    url = 'http://music.163.com/api/song/media?id=483282394'
    # text里就是网页的内容了
    text = requests_html(url)
    # 把text里的内容交给parser_html函数解析
    parser_html(text)