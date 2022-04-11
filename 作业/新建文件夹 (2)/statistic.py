import os

#data路径
path="C:/Users/legolas/Desktop/大三下/信息检索/作业/data"
s=[]#文件名
files = os.listdir(path)  # 得到文件夹下的所有文件名称
for file in files:  # 遍历文件夹
    s.append(file)
# for i in range(len(s)):
#     s[i]=s[i].split('.')[0]

words_num={}#总词频
words_num_doc={}#各篇文章中词频
words_doc={}#词出现的文章
def readFile():
    for i in range(1,len(os.listdir(path))):
        with open(path+'/'+str(i)+".txt", "r", encoding='UTF-8') as f:  # 打开文件
            data = f.read()  # 读取文件
            temp=data.split()#temp中存放file中所有词
            #print(temp)
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
    # for i in words_doc:
    #     words_doc[i]=list(set(words_doc[i]))




def funcAND(p1,p2):
    #     answer < -()
    #     while p1 != NIL and p2 != NIL
    #         do if docID(p1) = docID(p2)
    #     then
    #     ADD(answer, docID(p1))
    #     p1 < -next(p1)
    #     p2 < -next(p2)
    # else if docID(p1) < docID(p2)
    #     p1 < -next(p1)
    # else p2 < -next(p2)
    # return answer
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
    print("-----And操作结果为-----")
    print(t1)
    print(t2)
    result_print=[int(x) for x in result]
    result_print.sort()
    print(result_print)
    return result


def funcOR(p1,p2):
    #     answer < -()
    #     while p1 != NIL and p2 != NIL
    #         do if docID(p1) = docID(p2)
    #     then
    #     ADD(answer, docID(p1))
    #     p1 < -next(p1)
    #     p2 < -next(p2)
    #
    # else if docID(p1) < docID(p2)
    #     then
    #     ADD(answer, docID(p1))
    # p1 < -next(p1)
    # else ADD(answer, docID(p2))
    # p2 < -next(p2)
    # return answer
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
    #     answer < -()
    #     while p1 != NIL and p2 != NIL
    #         do if docID(p1) = docID(p2)
    #     p1 < -next(p1)
    #     p2 < -next(p2)
    #
    # else if docID(p1) < docID(p2)
    #     then
    #     ADD(answer, docID(p1))
    #     p1 < -next(p1)
    # else p2 < -next(p2)
    #
    # if p1 != NIL and P2 = NIL
    # then
    # ADD(answer, docID(p1))
    # p1 < -next(p1)
    # return answer
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






if __name__ == '__main__':
    readFile()
    # #总词频
    # print(words_num)
    # #词出现的文档
    # print(words_doc)
    # #各篇文章中的词频
    # print(words_num_doc)
    getStatistics()
    state1=input("请输入必须要的查询关键词:")
    state2 = input("请输入可包含的查询关键词:")
    state3=input("请输入禁用关键词:")
    search(state1,state2,state3)
    funcFind('爱情')
    funcFind('悲伤')
    funcFind('风')
    funcFind('李荣浩')
    funcAND('爱情', '悲伤')
    funcOR('爱情', '悲伤')
    func_AND_NOT('爱情', '悲伤')
    funcOR_NOT('爱情', '悲伤')






