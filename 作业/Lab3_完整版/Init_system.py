import os
import pickle
import function_lib

#data路径
path="./data"
s=[]#文件名
files = os.listdir(path)  # 得到文件夹下的所有文件名称
for file in files:  # 遍历文件夹
    s.append(file)
# for i in range(len(s)):
#     s[i]=s[i].split('.')[0]

all_posting_1 = {}   # 总posting 1  A - F
all_posting_2 = {}   # 总posting 2  G - K
all_posting_3 = {}   # 总posting 3  L - P
all_posting_4 = {}   # 总posting 4  Q - U
all_posting_5 = {}   # 总posting 5  V - Z

words_num={}#总词频


song_freq = {}   # 歌曲名
singer_freq = {}   # 歌手名
style_freq = {}  # 风格
words_freq = {}   # 歌词


def readFile():
    # initial all_posting list
    for i in range(1,len(os.listdir(path)) + 1):
        with open(path+'/'+str(i)+".txt", "r", encoding='UTF-8') as f:  # 打开文件
            data = f.read()  # 读取文件
            temp=data.split()#temp中存放file中所有词
            #print(temp)

        single_doc = {}  # 单篇文章中出现的词
        for j in temp:
            if j != '$END':
                if j not in single_doc.keys():
                    single_doc[j] = 1
                else:
                    single_doc[j] += 1

        #统计总词频
        for k in temp:
            if k != '$END':
                if k not in words_num:
                    words_num[k]=1
                else:
                    words_num[k]+=1

        #统计词出现的文章，加入posting
        for key in single_doc.keys():
            firstLetter = function_lib.getFirstLetter(key)
            if 'A' <= firstLetter <= 'F':
                if key not in all_posting_1.keys():
                    all_posting_1[key] = dict()
                    all_posting_1[key][i] = single_doc[key]
                else:
                    all_posting_1[key][i] = single_doc[key]

            elif 'G' <= firstLetter <= 'K':
                if key not in all_posting_2.keys():
                    all_posting_2[key] = dict()
                    all_posting_2[key][i] = single_doc[key]
                else:
                    all_posting_2[key][i] = single_doc[key]

            elif 'L' <= firstLetter <= 'P':
                if key not in all_posting_3.keys():
                    all_posting_3[key] = dict()
                    all_posting_3[key][i] = single_doc[key]
                else:
                    all_posting_3[key][i] = single_doc[key]

            elif 'Q' <= firstLetter <= 'U':
                if key not in all_posting_4.keys():
                    all_posting_4[key] = dict()
                    all_posting_4[key][i] = single_doc[key]
                else:
                    all_posting_4[key][i] = single_doc[key]

            elif 'V' <= firstLetter <= 'Z':
                if key not in all_posting_5.keys():
                    all_posting_5[key] = dict()
                    all_posting_5[key][i] = single_doc[key]
                else:
                    all_posting_5[key][i] = single_doc[key]


    # save data
    with open('./storage/all_posting_1.data','wb') as f:
        pickle.dump(all_posting_1,f)
    with open('./storage/all_posting_2.data','wb') as f:
        pickle.dump(all_posting_2,f)
    with open('./storage/all_posting_3.data','wb') as f:
        pickle.dump(all_posting_3,f)
    with open('./storage/all_posting_4.data','wb') as f:
        pickle.dump(all_posting_4,f)
    with open('./storage/all_posting_5.data','wb') as f:
        pickle.dump(all_posting_5,f)


# init zone files
def init_zones():
    for i in range(1, len(os.listdir(path)) + 1):
        with open(path+'/'+str(i)+".txt", "r", encoding='UTF-8') as f:  # 打开文件
            data = f.read()  # 读取文件
            temp=data.split()#temp中存放file中所有词

        if len(temp) < 4:
            print("Error found in " + os.listdir(path)[i])
            return

        # song
        if temp[0] not in song_freq.keys():
            song_freq[temp[0]] = {i : 1}

        # singer
        if temp[1] not in singer_freq.keys():
            singer_freq[temp[1]] = dict()
        singer_freq[temp[1]][i] = 1

        # style
        temp_index = 2
        while temp[temp_index] != "$END":
            if temp[temp_index] not in style_freq.keys():
                style_freq[temp[temp_index]] = dict()
            style_freq[temp[temp_index]][i] = 1
            temp_index += 1

        # words
        single_doc = {}
        for j in range(temp_index + 1, len(temp)):
            word = temp[j]
            if word not in single_doc.keys():
                single_doc[word] = 1
            else:
                single_doc[word] += 1

        #统计词出现的文章，加入posting
        for key in single_doc.keys():
            if key not in words_freq.keys():
                words_freq[key] = dict()
            words_freq[key][i] = single_doc[key]



    # save data
    with open('./storage/all_freq.data','wb') as f:
        pickle.dump(words_num,f)

    with open('./storage/all_posting_1.data','wb') as f:
        pickle.dump(all_posting_1,f)
    with open('./storage/all_posting_2.data','wb') as f:
        pickle.dump(all_posting_2,f)
    with open('./storage/all_posting_3.data','wb') as f:
        pickle.dump(all_posting_3,f)
    with open('./storage/all_posting_4.data','wb') as f:
        pickle.dump(all_posting_4,f)
    with open('./storage/all_posting_5.data','wb') as f:
        pickle.dump(all_posting_5,f)

    # save zone data
    with open('./storage/song_freq.data','wb') as f:
        pickle.dump(song_freq,f)
    with open('./storage/singer_freq.data','wb') as f:
        pickle.dump(singer_freq,f)
    with open('./storage/style_freq.data','wb') as f:
        pickle.dump(style_freq,f)
    with open('./storage/words_freq.data','wb') as f:
        pickle.dump(words_freq,f)



if __name__ == '__main__':
    readFile()
    init_zones()
    # #总词频
    # print(words_num)
    # #词出现的文档
    # print(words_doc)
    # #各篇文章中的词频
    print('finished')







