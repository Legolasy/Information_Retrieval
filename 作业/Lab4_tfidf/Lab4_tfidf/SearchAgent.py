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
    tfidf_vectors = {}  # 各篇文章对应的向量
    wfidf1_vectors = {}
    wfidf2_vectors = {}

    def readFile(self):
        # 记录向量空间大小
        for i in range(1, len(os.listdir(self.path))):
            with open(self.path + '/' + str(i) + ".txt", "r", encoding='UTF-8') as f:  # 打开文件
                data = f.read()  # 读取文件
                temp = data.split()  # temp中存放file中所有词
            # 统计每篇文章term个数
            temp.remove('$END')
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


    def SimpleSeach(self, search_str):
        search_content = search_str.split()

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

