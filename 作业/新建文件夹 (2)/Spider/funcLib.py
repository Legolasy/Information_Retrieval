# coding=utf-8

import re
import jieba

# import model


# 读取指定文件名的文本内容
def readFromFile(filename, encoding_way='utf-8'):
    dataFrame = []
    with open(filename, 'r', encoding=encoding_way) as f:
        for line in f.readlines():
            # print(line)
            dataFrame.append(line)
    return dataFrame



# 对一个中文字符串进行分词、筛选操作
def processChineseSentence(sentence):
    # 获得停用词表
    stopList = readFromFile('./BayesClassifier/Models/中文停用词表.txt', '936')

    cutTextList = []
    # 过滤掉非中文字符
    rule = re.compile(r"[^\u4e00-\u9fa5]")
    sentence = rule.sub("", sentence)
    # 将每封邮件出现的词保存在wordsList中
    textList = list(jieba.cut(sentence))
    # 过滤单个字符
    # textList = [tok for tok in textList if len(tok) >= 2]
    for i in textList:
        if i not in stopList and i.strip() != '' and i != None:
            cutTextList.append(i)

    cutLine = ''
    for word in cutTextList:
        cutLine += word + ' '
    return cutLine

