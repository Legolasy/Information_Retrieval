import os
import numpy as np
import math

class SearchAgent:
    path = "./data"
    s = []  # 文件名
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    for file in files:  # 遍历文件夹
        s.append(file)
    doc_number = len(s)  # 文件总数
    word_bag = []   # 总词袋
    words_num = {}  # 总词频
    words_num_doc = {}  #各篇文章中词频
    words_doc = {}  # 词出现的文章
    term_num_eachDoc = {}  # 每篇文章中的term个数
    maxt_eachDoc={} #每篇文档term出现最多的次数
    tfidf_vectors = {}  # 各篇文章对应的向量
    wfidf1_vectors = {}
    wfidf2_vectors = {}

    def readFile(self):
        # 记录向量空间大小
        for i in range(1, len(os.listdir(self.path))+1):
            with open(self.path + '/' + str(i) + ".txt", "r", encoding='UTF-8') as f:  # 打开文件
                data = f.read()  # 读取文件
                temp = data.split()  # temp中存放file中所有词
            # 统计每篇文章term个数
            temp.remove('$END')
            #统计maxt
            maxt = temp.count(max(temp, key=temp.count))
            self.maxt_eachDoc[str(i)]=maxt
            self.term_num_eachDoc[str(i)] = len(temp)
            for new_word in temp:
                if new_word not in self.word_bag:
                    self.word_bag.append(new_word)

        # 按文档计算向量
        for i in range(1, len(os.listdir(self.path)) + 1):
            with open(self.path + '/' + str(i) + ".txt", "r", encoding='UTF-8') as f:  # 打开文件
                data = f.read()  # 读取文件
                temp = data.split()  # temp中存放file中所有词
            # 统计每篇文章term个数
            temp.remove('$END')

            # 文章向量的初始化
            self.tfidf_vectors[str(i)] = [0 for x in range(0, len(self.word_bag))]
            self.wfidf1_vectors[str(i)] = [0 for x in range(0, len(self.word_bag))]
            self.wfidf2_vectors[str(i)] = [0 for x in range(0, len(self.word_bag))]

            # 统计各篇文章中的词频
            for j in temp:
                self.words_num_doc.setdefault(j, {})[i] = 0
            for j in temp:
                self.words_num_doc.setdefault(j, {})[i] += 1
            # 统计词出现的文章
            for m in temp:
                self.words_doc.setdefault(m, set()).add(i)
            # 统计总词频
            for k in temp:
                if k not in self.words_num:
                    self.words_num[k] = 1
                else:
                    self.words_num[k] += 1
        self.calculate_vector()
    # 计算各文章向量
    def calculate_vector(self):
        for dimension in range(0, len(self.word_bag)):
            tf_list = []
            for passage_id in range(1, len(self.tfidf_vectors) + 1):   # passageID starts from 1
                tf_list.append(self.tf(self.word_bag[dimension], passage_id))
            max_tf = max(tf_list)
            idf = self.idf(self.word_bag[dimension])

            for passage_id in range(1, len(self.tfidf_vectors) + 1):
                tf_item = self.tf(self.word_bag[dimension], passage_id)
                self.tfidf_vectors[str(passage_id)][dimension] = tf_item * idf

                wf1_term = self.wf_1(tf_item)
                self.wfidf1_vectors[str(passage_id)][dimension] = wf1_term * idf

                wf2_term = self.wf_2(tf_item, max_tf)
                self.wfidf2_vectors[str(passage_id)][dimension] = wf2_term * idf
    def tf(self, term, fileID):
        list_appear = self.words_num_doc[term]
        if fileID in list_appear.keys():
            num_appear = list_appear[fileID]
            return float(num_appear)
        else:
            return 0
    def idf(self, term):
        # 公式：log(总文档数/包含term文档数)
        l = list(self.words_doc[term])
        l1 = [int(i) for i in l]
        l1.sort()
        idf_rs = self.doc_number / len(l1)
        idf_rs = math.log(idf_rs, 10)
        return idf_rs
    def wf_1(self, df):
        if df > 0:
            wf = 1 + math.log(df, 10)
            return wf
        else:
            return 0
    def wf_2(self, df, max_df):
        if df > 0:
            wf = 0.5 + (0.5 * df) / max_df
            return wf
        else:
            return 0
    def calculate_cos(self, vec1, vec2):
        if len(vec1) != len(vec2):
            print('Error happen in calculating cosine')
            exit(1)

        sum = 0
        len_vec1 = 0
        len_vec2 = 0
        for i in range(0 , len(vec1)):
            sum += vec1[i] * vec2[i]
            len_vec1 += vec1[i] * vec1[i]
            len_vec2 += vec2[i] * vec2[i]

        len_vec1 = math.sqrt(len_vec1)
        len_vec2 = math.sqrt(len_vec2)

        if sum == 0:
            return 0

        cosine = sum / (len_vec1 * len_vec2)
        return cosine
    def cosine_score(self,q,type):
        term=q.split()
        termset=list(set(term))
        if len(term)==0:
            return term
        for i in termset:
            if i not in SearchAgent.word_bag:
                termset.remove(i)
        #文章总数
        N=SearchAgent.doc_number
        #q出现最多的term的次数
        maxt=term.count(max(term, key=term.count))
        # print(max(term, key=term.count))
        # print(term.count(max(term, key=term.count)))
        #q中每个term出现的次数
        freq = dict((a, term.count(a)) for a in term);
        print(freq)
        #初始化Score为0
        Score=[0]*(N+1)
        Length=SearchAgent.term_num_eachDoc
        #print('wf1=1 wf2=2')
        num = type
        #wftd1
        if num == 1:
            for i in termset:
                # term 出现的文章数
                ni=len(SearchAgent.words_doc[i])
                #print(ni)
                wiq=(0.5+(0.5*freq[i])/maxt)*math.log(N/ni)
                #query词权重wtq搞定
                print(wiq)
                #计算wftd tf maxt 每个词及对应的文档wftd得分
                for m in SearchAgent.words_doc[i]:
                    #print(m)
                    #计算Score[m] 文档id=m的得分
                    tf=SearchAgent.tf(self,i,m)
                    #wf1
                    wftd=1+math.log(tf)
                    Score[m]+=wftd*wiq
        #wftd2
        if num==2:
            for i in termset:
                if i not in SearchAgent.word_bag:
                    continue
                # term 出现的文章数
                ni = len(SearchAgent.words_doc[i])
                #print(ni)
                wiq = (0.5 + (0.5 * freq[i]) / maxt) * math.log(N / ni)
                # query词权重wtq搞定
                print(wiq)
                # 计算wftd tf maxt 每个词及对应的文档wftd得分
                for m in SearchAgent.words_doc[i]:
                    #print(m)
                    # 计算Score[m] 文档id=m的得分
                    # wf1 wf2 tf
                    tf = SearchAgent.tf(self, i, m)
                    # max_tf本篇文档中出现最多的term的词频
                    max_tf = SearchAgent.maxt_eachDoc[str(m)]
                    #wf2
                    wftd = 0.5 + (0.5 * tf) / max_tf
                    Score[m] += wftd * wiq
        #tf
        if num==3:
            for i in termset:
                if i not in SearchAgent.word_bag:
                    continue
                # term 出现的文章数
                ni = len(SearchAgent.words_doc[i])
                #print(ni)
                wiq = (0.5 + (0.5 * freq[i]) / maxt) * math.log(N / ni)
                # query词权重wtq搞定
                print(wiq)
                # 计算wftd tf maxt 每个词及对应的文档wftd得分
                for m in SearchAgent.words_doc[i]:
                    #print(m)
                    # 计算Score[m] 文档id=m的得分
                    # wf1 wf2 tf
                    tf = SearchAgent.tf(self, i, m)
                    # max_tf本篇文档中出现最多的term的词频
                    max_tf = SearchAgent.maxt_eachDoc[str(m)]
                    #wf2
                    wftd = 0.5 + (0.5 * tf) / max_tf
                    Score[m] += tf * wiq
        ScoreDict={}
        for cnt in range(1,len(Score)):
            Score[cnt]/=SearchAgent.term_num_eachDoc[str(cnt)]
            if Score[cnt] != 0:
                ScoreDict[cnt] = Score[cnt]
        ScoreDict = dict(sorted(ScoreDict.items(), key=lambda d: d[1], reverse=True))
        return ScoreDict
    def faster_cosine_score(self,q,type):
        term = q.split()
        if len(term)==0:
            return term
        termset = list(set(term))
        for i in termset:
            if i not in SearchAgent.word_bag:
                termset.remove(i)
        # 文章总数
        N = SearchAgent.doc_number
        # q出现最多的term的次数
        maxt = term.count(max(term, key=term.count))
        # print(max(term, key=term.count))
        # print(term.count(max(term, key=term.count)))
        # q中每个term出现的次数
        freq = dict((a, term.count(a)) for a in term);
        print(freq)
        # 初始化Score为0
        Score = [0] * (N + 1)
        Length = SearchAgent.term_num_eachDoc
        #print('wf1=1 wf2=2')
        num = type
        #wftd1
        if num == 1:
            for i in termset:
                if i not in SearchAgent.word_bag:
                    continue
                #wiq不需要了
                # # term 出现的文章数
                # ni = len(SearchAgent.words_doc[i])
                # # print(ni)
                # wiq = (0.5 + (0.5 * freq[i]) / maxt) * math.log(N / ni)
                # # query词权重wtq搞定
                # print(wiq)
                # # 计算wftd tf maxt 每个词及对应的文档wftd得分
                for m in SearchAgent.words_doc[i]:
                    # print(m)
                    # 计算Score[m] 文档id=m的得分
                    tf = SearchAgent.tf(self, i, m)
                    # wf1
                    wftd = 1 + math.log(tf)
                    Score[m] += wftd
        #wftd2
        if num == 2:
            for i in termset:
                if i not in SearchAgent.word_bag:
                    continue
                # wiq不需要了
                # # term 出现的文章数
                # ni = len(SearchAgent.words_doc[i])
                # # print(ni)
                # wiq = (0.5 + (0.5 * freq[i]) / maxt) * math.log(N / ni)
                # # query词权重wtq搞定
                # print(wiq)
                # # 计算wftd tf maxt 每个词及对应的文档wftd得分
                for m in SearchAgent.words_doc[i]:
                    # print(m)
                    # 计算Score[m] 文档id=m的得分
                    # wf1 wf2 tf
                    tf = SearchAgent.tf(self, i, m)
                    # max_tf本篇文档中出现最多的term的词频
                    max_tf = SearchAgent.maxt_eachDoc[str(m)]
                    # wf2
                    wftd = 0.5 + (0.5 * tf) / max_tf
                    Score[m] += wftd
        #tf
        if num == 3:
            for i in termset:
                # wiq不需要了
                # # term 出现的文章数
                # ni = len(SearchAgent.words_doc[i])
                # # print(ni)
                # wiq = (0.5 + (0.5 * freq[i]) / maxt) * math.log(N / ni)
                # # query词权重wtq搞定
                # print(wiq)
                # # 计算wftd tf maxt 每个词及对应的文档wftd得分
                for m in SearchAgent.words_doc[i]:
                    # print(m)
                    # 计算Score[m] 文档id=m的得分
                    # wf1 wf2 tf
                    tf = SearchAgent.tf(self, i, m)
                    Score[m] += tf
        ScoreDict = {}
        for cnt in range(1, len(Score)):
            Score[cnt] /= SearchAgent.term_num_eachDoc[str(cnt)]
            if Score[cnt]!=0:
                ScoreDict[cnt] = Score[cnt]
        ScoreDict = dict(sorted(ScoreDict.items(), key=lambda d: d[1], reverse=True))
        return ScoreDict
    def SimpleSeach(self, search_str):
        search_content = search_str.split()
        for i in search_content:
            if i not in SearchAgent.word_bag:
                search_content.remove(i)
        # 将搜索请求表示为向量
        search_vec = [0 for i in range(0, len(self.word_bag))]
        for i in range(0, len(search_content)):
            if search_content[i] in self.word_bag:
                d_index = self.word_bag.index(search_content[i])
                search_vec[d_index] = 1

        # 计算搜索向量与所有文档向量的相似度
        search_result = []
        for i in range(1, self.doc_number + 1):
            cos_sim = self.calculate_cos(search_vec, self.tfidf_vectors[str(i)])
            if cos_sim != 0:
                search_result.append({'docID': i, 'tfidf': 0, 'wfidf1': 0, 'wfidf2': 0})

        for item in search_result:
            docID = item['docID']
            tf_sim = self.calculate_cos(search_vec, self.tfidf_vectors[str(docID)])
            wf1_sim = self.calculate_cos(search_vec, self.wfidf1_vectors[str(docID)])
            wf2_sim = self.calculate_cos(search_vec, self.wfidf2_vectors[str(docID)])
            item['tfidf'] = tf_sim
            item['wfidf1'] = wf1_sim
            item['wfidf2'] = wf2_sim

        return search_result

if __name__ == '__main__':
    a=SearchAgent()
    a.readFile()
    print("word bag length")
    print(len(a.word_bag))
    for i in a.word_bag:
        print(i + " ", end="")


    # print("tfidf_vectors")
    # for k,v in a.tfidf_vectors.items():
    #     print(str(k) + " = "+str(v)+" ")

    #a.cosine_score("王菲 巴啦啦小魔仙",1)
    #print(a.words_num["抒情"])


    #print(a.tfidf_vectors)
    #print(a.wfidf1_vectors)
    #a.cosine_score('爱情 爱情 悲伤 华语',1)
    #print('faster-------')
    #a.faster_cosine_score('爱情 爱情 悲伤 华语')
    #print(a.term_num_eachDoc)# 总词频
    # print("------------------------")
    #print(a.maxt_eachDoc)  # 各篇文章中词频
    # words_num = {}
    # words_num_doc = {}  # 各篇文章中词频
    # words_doc = {}  # 词出现的文章
    # term_num_eachDoc = {}  # 每篇文章中的term个数