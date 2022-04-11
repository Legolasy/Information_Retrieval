import re
import jieba

# 对一个中文字符串进行分词、筛选操作
# 读取指定文件名的文本内容
# 读取指定文件名的文本内容
def readFromFile(filename, encoding_way='utf-8'):
    dataFrame = []
    with open(filename, 'r', encoding=encoding_way) as f:
        for line in f.readlines():
            # print(line)
            line = line.strip('\n')
            dataFrame.append(line)
    return dataFrame

def processChineseSentence(sentence):
    # 获得停用词表
    stopList = readFromFile('./Models/中文停用词表.txt', '936')

    cutTextList = []
    # 过滤掉非中文字符
    rule = re.compile(r"[^\u4e00-\u9fa5]")
    sentence_CN = rule.sub("", sentence)
    # 将每封邮件出现的词保存在wordsList中
    textList = list(jieba.cut(sentence_CN))
    # 过滤单个字符
    # textList = [tok for tok in textList if len(tok) >= 2]
    for i in textList:
        if i not in stopList and i.strip() != '' and i != None:
            cutTextList.append(i)

    # 获得英文字符
    eng_list = re.findall('[a-zA-Z0-9]+', sentence)

    cutLine = ''
    for word in cutTextList:
        cutLine += word + ' '
    for eng in eng_list:
        cutLine += eng + ' '
    return cutLine


if __name__ == '__main__':
    print(processChineseSentence("王者荣耀真好玩"))