import os
import pickle
import function_lib
import simpleSearch
import time
#data路径
path="./data"
s=[]#文件名
files = os.listdir(path)  # 得到文件夹下的所有文件名称
for file in files:  # 遍历文件夹
    s.append(file)

#Zone
with open('./storage/song_freq.data','rb') as f:
    song_freq = pickle.load(f)
with open('./storage/singer_freq.data','rb') as f:
    singer_freq = pickle.load(f)
with open('./storage/style_freq.data','rb') as f:
    style_freq = pickle.load(f)
with open('./storage/words_freq.data','rb') as f:
    words_freq = pickle.load(f)


words_num={}#总词频
words_num_doc={}#各篇文章中词频
words_doc={}#词出现的文章
k_gram_doc={}
term_num_eachDoc={}#每篇文章中的term个数
def readFile():
    for i in range(1,len(os.listdir(path))):
        with open(path+'/'+str(i)+".txt", "r", encoding='UTF-8') as f:  # 打开文件
            data = f.read()  # 读取文件
            temp=data.split()#temp中存放file中所有词
            #print(temp)
        # 统计每篇文章term个数
        term_num_eachDoc[str(i) + ".txt"] = len(temp)

        #统计各篇文章中的词频
        for j in temp:
            words_num_doc.setdefault(j,{})[s[i].split('.')[0]]=0
        for j in temp:
            words_num_doc.setdefault(j,{})[s[i].split('.')[0]]+=1
        #统计词出现的文章
        for m in temp:
            words_doc.setdefault(m,set()).add(s[i].split('.')[0])
        #统计总词频
        for k in temp:
            if k not in words_num:
                words_num[k]=1
            else:
                words_num[k]+=1
        #k_gram_index
        for k in temp:
            tlist=[]
            if is_Chinese(k):
                for i in range(len(k)):
                    tlist.append(k[i])
                for i in tlist:
                    k_gram_doc.setdefault(i,set()).add(k)
            else:
                for i in range(len(k)):
                    tlist.append(k[i])
                for i in range(len(k)-1):
                    tchar=tlist[i]+tlist[i+1]
                    k_gram_doc.setdefault(tchar, set()).add(k)







def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False



def funcAND(p1,p2):
    #返回result set
    t1=[int(x) for x in words_doc[p1]]
    t1.sort()
    t2 = [int(x) for x in words_doc[p2]]
    t2.sort()
    result=set()
    #先比较短的 优化操作
    if len(t1)>len(t2):
        temp=t1
        t1=t2
        t2=temp
    for i,val1 in enumerate(t1):
        for j,val2 in enumerate(t2):
            if val1==val2:
                result.add(val1)
            if val1<val2:
                i+=1
            if val1>val2:
                j+=1
    # print("-----And操作结果为-----")
    # print(t1)
    # print(t2)
    result_print=[int(x) for x in result]
    result_print.sort()
    print(result_print)
    return result


def funcOR(p1,p2):
    result=set()
    t1 = [int(x) for x in words_doc[p1]]
    t1.sort()
    t2 = [int(x) for x in words_doc[p2]]
    t2.sort()
    # 先比较短的 优化操作
    if len(t1) > len(t2):
        temp = t1
        t1 = t2
        t2 = temp
        i=j=0
    while j<len(t2):
        if i==len(t1)-1:
            result.add(t2[j])
            j+=1
        elif t1[i]==t2[j]:
            result.add(t1[i])
            i+=1
            j+=1
        elif t1[i]<t2[j]:
            result.add(t1[i])
            i+=1
        elif t1[i]>t2[j]:
            result.add(t2[j])
            j+=1



    print("-----Or操作结果为-----")
    print(t1)
    print(t2)
    result_print = [int(x) for x in result]
    result_print.sort()
    print(result_print)
    return result


def func_AND_NOT(p1,p2):
    t1 = [int(x) for x in words_doc[p1]]
    t1.sort()
    t2 = [int(x) for x in words_doc[p2]]
    t2.sort()
    result = set()
    # 先比较短的 优化操作
    if len(t1) > len(t2):
        temp = t1
        t1 = t2
        t2 = temp
    i=0
    j=0
    while i<len(t1) :
        if j==len(t2)-1:
            result.add(t1[i])
            i+=1
        elif t1[i]==t2[j]:
            i+=1
            j+=1
        elif t1[i]<t2[j]:
            result.add(t1[i])
            i+=1
        elif t1[i]>t2[j]:
            j+=1
    print("-----AND_NOT操作结果为-----")
    print(t1)
    print(t2)
    result_print = [int(x) for x in result]
    result_print.sort()
    print(result_print)
    return result





def funcFind(p):
    result=set()
    for i in words_doc[p]:
        result.add(i)
    t1 = [int(x) for x in words_doc[p]]
    t1.sort()
    print("包含"+str(p)+"的文档为：")
    for i in t1:
        print(i, end="")
        print(" ", end="")
    print("")

    return result

def funcOR_NOT(p1,p2):
    result=list()
    for i in range(1,len(os.listdir(path))):
        result.append(i)
    t1 = set([int(x) for x in words_doc[p1]])
    t2=[int(x) for x in words_doc[p2]]
    t2.sort()
    print("-----OR_NOT操作结果为-----")
    print(t2)
    t2 = set([int(x) for x in words_doc[p2]])


    t2=set(result)-t2
    result=set(result)
    result=t1|t2
    result=[int(x) for x in result]
    result.sort()
    t1=list(t1)
    t2=list(t2)
    t1.sort()
    t2.sort()

    print(t1)

    print(result)
def getStatistics():
    with open('倒排索引.txt','a') as f:
        for i in words_num:
            print("Term: ",end="")
            print(i,end="")
            print(" Total_Freq=",end="")
            print(words_num[i],end="")
            print(" ",end="")
            print(" DocID[",end="")
            temp=[int(x) for x in words_doc[i]]
            temp.sort()
            for m in temp:
                print(m,end="")
                if m==temp[-1]:
                    print("] ", end="")
                else:
                    print(",",end="")
            #print(list(words_doc[i]),end="")
            print(" ",end="")
            print(" Freq:",end="")
            print(words_num_doc.get(i))
            f.write("Term: "+str(i)+" Total_Freq"+str(words_num[i])+"  DocID:"+str(words_doc[i])+" Freq:"+str(words_num_doc[i]))
            f.write('\n')


def search(state1,state2,state3):
    #必须的查询关键词 可包含的查询关键词 排除的关键词
    list1=list()
    list1=state1.split()
    if len(list1)>1:
        result=funcAND(list1[0],list1[1])
        for i in range(1,len(list1)-1):
            result=result&funcAND(list1[i],list1[i+1])
    if len(list1) == 1:
        result=words_doc[list1[0]]
    #print(result)
    #RESULT 必须的
    #Result1 可包含的
    list2=list()
    list2=state2.split()
    if len(list2)>1:
        result1=funcOR(list2[0],list2[1])
        for i in range(1,len(list2)-1):
            result1=result1|funcOR(list2[i],list2[i+1])
    if len(list2) == 1:
        result1=words_doc[list2[0]]
    if len(list2) == 0:
        result1=set()

    #result3 排除
    list3 = list()
    list3 = state3.split()
    if len(list3) > 1:
        result2 = func_AND_NOT(list3[0], list3[1])
        for i in range(1, len(list3) - 1):
            result2 = result2|funcOR(list3[i], list3[i + 1])
    if len(list3) == 1:
        result2 = words_doc[list3[0]]
    if len(list3) == 0:
        result2=set()
    resultAll=(result|result1)-result2
    temp = [int(x) for x in resultAll]
    temp.sort()
    print("-----查询结果为-----")
    print(temp)

def search_pro():
    #default zone weight
    title_weight=5
    author_weight=3
    style_weight=1
    word_weight=1
    flag_t={}
    flag_a={}
    flag_s = {}
    flag_w = {}
    state=input('输入查询语句')
    a=input('输入标题权重1-10 默认5')
    b=input('输入歌手权重1-10 默认3')
    c=input('输入风格权重1-10 默认1')
    d=input('输入歌词权重1-10 默认1')
    if a!='':
        title_weight=int(a)
    if b!='':
        author_weight=int(b)
    if c!='':
        style_weight=int(c)
    if d!='':
        word_weight=int(d)
    lstate=state.split()
    doc_score={}
    #存放搜索匹配标题
    doc_title=[]
    doc_author= []
    doc_style= []
    doc_word = []
    # print('Before')
    # print(lstate)
    #k-gram补全用户输入潜在信息
    for i in lstate:
        #中文
        if is_Chinese(i):
            if len(i)==1:
                for m in k_gram_doc[i]:
                    if m not in lstate:
                        lstate.append(m)
        #英文
        else:
            if len(i)==2:
                for m in k_gram_doc[i]:
                    if m not in lstate:
                        lstate.append(m)
    # print("After k gram")
    # print(lstate)


    for i in lstate:
        #title
        if i in song_freq.keys():
            #print('title')
            # print(song_freq[i])
            doc_title+=list(song_freq[i].keys())

            #print(doc_title)
        #author
        if i in singer_freq.keys():
            #print('singer')
            #print(singer_freq[i])
            doc_author+=list(singer_freq[i].keys())
        # style
        if i in style_freq.keys():
            #print('style')
            #print(style_freq[i])
            doc_style+=list(style_freq[i].keys())
        # word
        if i in words_freq.keys():
            #print('word')
            #print(words_freq[i])
            doc_word+=list(words_freq[i].keys())

    #init flag
    for i in doc_title:
        flag_t[i]=True
    for i in doc_author:
        flag_a[i]=True
    for i in doc_style:
        flag_s[i]=True
    for i in doc_word:
        flag_w[i]=True


    #计算score 每个Zone得分只记一次
    #title
    if doc_title:
        for i in doc_title:
            if flag_t[i]==True:
                if i not in doc_score:
                    doc_score[i]=title_weight
                    flag_t[i]=False
                else:
                    doc_score[i]+=title_weight
                    flag_t[i] = False
    #author
    if doc_author:
        for i in doc_author:
            if flag_a[i] == True:
                if i not in doc_score:
                    doc_score[i]=author_weight
                    flag_a[i] = False
                else:
                    doc_score[i]+=author_weight
                    flag_a[i] = False
    #style
    if doc_style:
        for i in doc_style:
            if flag_s[i] == True:
                if i not in doc_score:
                    doc_score[i]=style_weight
                    flag_s[i] = False
                else:
                    doc_score[i]+=style_weight
                    flag_s[i] = False
    # word
    if doc_word:
        for i in doc_word:
            if flag_w[i] == True:
                if i not in doc_score:
                    doc_score[i] = word_weight
                    flag_w[i] = False
                else:
                    doc_score[i] += word_weight
                    flag_w[i] = False
    sorted_doc_score = ((k, doc_score[k]) for k in sorted(doc_score, key=doc_score.get, reverse=True))

    #输出排序后的doc score

    i=1
    for k, v in sorted_doc_score:
        print("docID=",end="")
        print(k,end="")
        print(" 得分:",end="")
        print(float(v/(title_weight+author_weight+style_weight+word_weight)))
        i+=1
        if i==11:
            break

def simple():
    state=input('简单查询输入：')
    temp=state.split()
    t=simpleSearch.simpleSearch(temp[0])
    i=1
    doctemp=set()
    doctemp=simpleSearch.simpleSearch(temp[0]).keys()
    #doctemp存放docID交集
    while i<len(temp):
        doctemp=doctemp&simpleSearch.simpleSearch(temp[i]).keys()
        i+=1
    #计算词频 各个关键词词频相加
    docScore={}
    for i in doctemp:
        for j in temp:
            print(j,end="")
            print(" docID=",end="")
            print(i,end="")
            print(" 词频： ",end="")
            print(simpleSearch.simpleSearch(j)[i])
            if i not in docScore:
                docScore[i]=simpleSearch.simpleSearch(j)[i]
            else:
                docScore[i] += simpleSearch.simpleSearch(j)[i]

    print('简单查询结果------')
    print('docID 词频')
    for k in sorted(docScore, key=docScore.__getitem__,reverse=True):
        print(k, docScore[k])

# def tf(term):
#     #w=1+log(tf)|0


# def tf_idf():


if __name__ == '__main__':
    #print(is_Chinese('你好'))
    readFile()
    getStatistics()
    # print("n------gram")
    # print(k_gram_doc['风'])
    print(term_num_eachDoc)
    s=input('1-简单搜索，2-高级搜索')
    if s=='1':
        simple()
    elif s=='2':
        search_pro()

    #print(simpleSearch.simpleSearch('风'))
    #print(words_freq)
    # state1=input("请输入必须要的查询关键词:")
    # state2 = input("请输入可包含的查询关键词:")
    # state3=input("请输入禁用关键词:")
    # search(state1,state2,state3)
    # funcFind('爱情')
    # funcFind('悲伤')
    # funcFind('风')
    # funcFind('李荣浩')
    # funcAND('爱情', '悲伤')
    # funcOR('爱情', '悲伤')
    # func_AND_NOT('爱情', '悲伤')
    # funcOR_NOT('爱情', '悲伤')






