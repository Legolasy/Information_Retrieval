import os
import pickle
import math
import split_word

class SearchAgent:
    path = "./data"
    s = []  # 文件名
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    for file in files:  # 遍历文件夹
        s.append(file)
    doc_number = len(s)  # 文件总数

    word_bag = []   # 记录出现的所有 term 项
    words_num = {}  # 总词频

    words_doc = {}  # 词出现的文章
    term_num_eachDoc = {}  # 每篇文章中的term个数

    # tfidf_vectors = {}  # 各篇文章对应的向量
    # wfidf1_vectors = {}
    wfidf2_vectors = {}

    # 记录各篇文章的词袋 'passage_id': {'word_term': frequency}
    word_bag_passage = {}  # 各文章的词袋 （M_d）
    word_bag_sum = {}   # 总词袋中总的term项数

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
            self.term_num_eachDoc[str(i)] = len(temp)
            for new_word in temp:                        # 计算总词袋
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
            # self.tfidf_vectors[str(i)] = [0 for x in range(0, len(self.word_bag))]
            # self.wfidf1_vectors[str(i)] = [0 for x in range(0, len(self.word_bag))]
            self.wfidf2_vectors[str(i)] = [0 for x in range(0, len(self.word_bag))]

            # 记录各篇文章的词袋
            bag_doc = {}  # 单个文章的词袋
            for j in temp:
                if j not in bag_doc.keys():
                    bag_doc[j] = 1
                else:
                    bag_doc[j] += 1
            self.word_bag_passage[str(i)] = bag_doc

            # 统计词出现的文章
            for m in temp:
                self.words_doc.setdefault(m, set()).add(i)
            # 统计总词频
            for k in temp:
                if k not in self.words_num:
                    self.words_num[k] = 1
                else:
                    self.words_num[k] += 1

            # 计算总词数
            self.word_bag_sum = 0
            for word_count in self.words_num.values():
                self.word_bag_sum += word_count

        self.calculate_vector()

    # 计算各文章向量
    def calculate_vector(self):
        for dimension in range(0, len(self.word_bag)):
            tf_list = []
            for passage_id in range(1, len(self.wfidf2_vectors) + 1):   # passageID starts from 1
                tf_list.append(self.tf(self.word_bag[dimension], passage_id))
            max_tf = max(tf_list)
            idf = self.idf(self.word_bag[dimension])

            for passage_id in range(1, len(self.wfidf2_vectors) + 1):
                tf_item = self.tf(self.word_bag[dimension], passage_id)
                # self.tfidf_vectors[str(passage_id)][dimension] = tf_item * idf

                # wf1_term = self.wf_1(tf_item)
                # self.wfidf1_vectors[str(passage_id)][dimension] = wf1_term * idf

                wf2_term = self.wf_2(tf_item, max_tf)
                self.wfidf2_vectors[str(passage_id)][dimension] = wf2_term * idf

    def tf(self, term, fileID):
        bag_passage = self.word_bag_passage[str(fileID)]
        if term in bag_passage.keys():
            num_appear = bag_passage[term]
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

    # 依据 P(X|R) 与 P(X|nonR) 计算相似性值 (sim) 中的一个对数项
    def calculate_sim_term(self, p_R, p_nonR):
        term1 = p_R / (1 - p_R)
        term1 = math.log(term1, 10)
        term2 = (1 - p_nonR) / p_nonR
        term2 = math.log(term2, 10)
        return term1 + term2

    # 存储语料库数据
    def save_corpus(self):
        with open('./storage/word_bag.data', 'wb') as f:
            pickle.dump(self.word_bag, f)
        with open('./storage/words_num.data', 'wb') as f:
            pickle.dump(self.words_num, f)
        with open('./storage/words_doc.data', 'wb') as f:
            pickle.dump(self.words_doc, f)
        with open('./storage/term_num_eachDoc.data', 'wb') as f:
            pickle.dump(self.term_num_eachDoc, f)
        with open('./storage/wfidf2_vectors.data', 'wb') as f:
            pickle.dump(self.wfidf2_vectors, f)
        with open('./storage/word_bag_passage.data', 'wb') as f:
            pickle.dump(self.word_bag_passage, f)
        with open('./storage/word_bag_sum.data', 'wb') as f:
            pickle.dump(self.word_bag_sum, f)
        with open('./storage/s.data', 'wb') as f:
            pickle.dump(self.s, f)

    # 加载已经存储了语料库信息
    def load_corpus(self):
        with open('./storage/word_bag.data', 'rb') as f:
            self.word_bag = pickle.load(f)
        with open('./storage/words_num.data', 'rb') as f:
            self.words_num = pickle.load(f)
        with open('./storage/words_doc.data', 'rb') as f:
            self.words_doc = pickle.load(f)
        with open('./storage/term_num_eachDoc.data', 'rb') as f:
            self.term_num_eachDoc = pickle.load(f)
        with open('./storage/wfidf2_vectors.data', 'rb') as f:
            self.wfidf2_vectors = pickle.load(f)
        with open('./storage/word_bag_passage.data', 'rb') as f:
            self.word_bag_passage = pickle.load(f)
        with open('./storage/word_bag_sum.data', 'rb') as f:
            self.word_bag_sum = pickle.load(f)
        with open('./storage/s.data', 'rb') as f:
            self.s = pickle.load(f)
        self.doc_number = len(self.s)  # 文件总数

    # Search using Mixed Language Model
    def search_languageModel(self, search_str):
        search_str = split_word.processChineseSentence(search_str)
        search_content = search_str.split()

        remove_list = []
        for i in search_content:
            if i not in self.word_bag:
                remove_list.append(i)
        for remove_term in remove_list:
            search_content.remove(remove_term)

        # 确定相关文章ID
        search_result = []
        for passage_id in range(1, len(os.listdir(self.path)) + 1):
            for search_term in search_content:
                if search_term in self.word_bag_passage[str(passage_id)].keys():
                    search_result.append({'docID': passage_id})
                    break

        # 计算 P(X|R) 与 P(X|nonR)
        lamda_coef = 0.5  # lamda 系数设置
        for result_index in range(0, len(search_result)):
            passage_id = search_result[result_index]['docID']
            sim_score = 0

            for search_term in search_content:
                # 仅当 query 与 doc 中均包含当前 term 项，sim 计算公式中的 w 权值才为 1
                if search_term in self.word_bag_passage[str(passage_id)].keys():
                    p_rc = float(self.words_num[search_term]) / float(self.word_bag_sum)
                    p_rd = float(self.word_bag_passage[str(passage_id)][search_term]) / float(self.term_num_eachDoc[str(passage_id)])
                    # 计算 P（X|R）
                    p_R = lamda_coef * p_rd + (1 - lamda_coef) * p_rc

                    # 计算 P(X|nonR)
                    # 基于假设 不相关的文档远多于相关文档，P(X|nonR)的概率近似为P(X)
                    # p_nonR = float(self.words_num[search_term]) / float(self.word_bag_sum)
                    p_nonR = float(self.words_num[search_term]) / float(self.word_bag_sum)

                    sim_term = self.calculate_sim_term(p_R, p_nonR)
                    sim_score += sim_term

            # store the calculated score
            search_result[result_index]['score'] = sim_score

        return search_result

    # Search using improved method 1
    def search_improved1(self, search_str):
        search_str = split_word.processChineseSentence(search_str)
        search_content = search_str.split()

        remove_list = []
        for i in search_content:
            if i not in self.word_bag:
                remove_list.append(i)
        for remove_term in remove_list:
            search_content.remove(remove_term)

        # 确定相关文章ID
        search_result = []
        for passage_id in range(1, len(os.listdir(self.path)) + 1):
            for search_term in search_content:
                if search_term in self.word_bag_passage[str(passage_id)].keys():
                    search_result.append({'docID': passage_id})
                    break

        # 计算 P(X|R) 与 P(X|nonR)
        for result_index in range(0, len(search_result)):
            passage_id = search_result[result_index]['docID']
            sim_score = 0

            for search_term in search_content:
                # 仅当 query 与 doc 中均包含当前 term 项，sim 计算公式中的 w 权值才为 1
                if search_term in self.word_bag_passage[str(passage_id)].keys():
                    # 计算 P（X|R） = 0.5
                    p_R = 0.5
                    # 计算 P(X|nonR) = ni / N
                    p_nonR = float(len(self.words_doc[search_term])) / float(self.doc_number)

                    sim_term = self.calculate_sim_term(p_R, p_nonR)
                    sim_score += sim_term

            # store the calculated score
            search_result[result_index]['score'] = sim_score

        return search_result

    # Search using improved method 2
    def search_improved2(self, search_str):
        search_str = split_word.processChineseSentence(search_str)
        search_content = search_str.split()

        remove_list = []
        for i in search_content:
            if i not in self.word_bag:
                remove_list.append(i)
        for remove_term in remove_list:
            search_content.remove(remove_term)

        # 确定相关文章ID
        search_result = []
        for passage_id in range(1, len(os.listdir(self.path)) + 1):
            for search_term in search_content:
                if search_term in self.word_bag_passage[str(passage_id)].keys():
                    search_result.append({'docID': passage_id})
                    break

        # 确定集合 V, 取 wfidf2 得分最高的前 50% 数据 ---------------------------------------
        # 将搜索请求表示为向量
        search_vec = [0 for i in range(0, len(self.word_bag))]
        for i in range(0, len(search_content)):
            if search_content[i] in self.word_bag:
                d_index = self.word_bag.index(search_content[i])
                search_vec[d_index] = 1

        # 计算搜索向量与所有文档向量的相似度
        wfidf_result = []
        for i in range(1, self.doc_number + 1):
            cos_sim = self.calculate_cos(search_vec, self.wfidf2_vectors[str(i)])
            if cos_sim != 0:
                wfidf_result.append({'docID': i, 'wfidf2': cos_sim})

        # 取 wf-idf 得分最高的前 50% 条数据作为集合 V
        wfidf_score_list = [term['wfidf2'] for term in wfidf_result]
        wfidf_score_list.sort()
        threshold = wfidf_score_list[int(len(wfidf_score_list)/2)]   # 中位数对应的 wfidf 得分

        V_result = []
        for term in wfidf_result:
            if term['wfidf2'] > threshold:
                V_result.append(term['docID'])

        # 计算集合 V 与 Vi
        V_num = len(V_result)
        Vi_num = {}
        for search_term in search_content:
            Vi_num[search_term] = 0
            for passage_id in V_result:
                if search_term in self.word_bag_passage[str(passage_id)].keys():
                    Vi_num[search_term] += 1

        # 计算 P(X|R) 与 P(X|nonR)
        for result_index in range(0, len(search_result)):
            passage_id = search_result[result_index]['docID']
            sim_score = 0

            for search_term in search_content:
                # 仅当 query 与 doc 中均包含当前 term 项，sim 计算公式中的 w 权值才为 1
                if search_term in self.word_bag_passage[str(passage_id)].keys():
                    # 计算 P（X|R）= Vi / V
                    p_R = float(Vi_num[search_term]) / float(V_num)

                    # 计算 P(X|nonR) = (ni - Vi) / (N - V)
                    p_nonR = float(len(self.words_doc[search_term]) - Vi_num[search_term]) / float(self.doc_number - V_num)
                    # p_nonR 在实际情况下很有可能为 0， 如果为0，我们将它的分子用0.1代替 ------------------------------------
                    if p_nonR == 0:
                        p_nonR = 0.1 / float(self.doc_number - V_num)

                    sim_term = self.calculate_sim_term(p_R, p_nonR)
                    sim_score += sim_term

            # store the calculated score
            search_result[result_index]['score'] = sim_score

        return search_result

    # Search using improved method 3
    def search_improved3(self, search_str):
        search_str = split_word.processChineseSentence(search_str)
        search_content = search_str.split()

        remove_list = []
        for i in search_content:
            if i not in self.word_bag:
                remove_list.append(i)
        for remove_term in remove_list:
            search_content.remove(remove_term)

        # 确定相关文章ID
        search_result = []
        for passage_id in range(1, len(os.listdir(self.path)) + 1):
            for search_term in search_content:
                if search_term in self.word_bag_passage[str(passage_id)].keys():
                    search_result.append({'docID': passage_id})
                    break

        # 计算集合 V 与 Vi
        V_num = len(search_result)
        Vi_num = {}
        for search_term in search_content:
            Vi_num[search_term] = 0
            for result_index in range(0, len(search_result)):
                passage_id = search_result[result_index]['docID']
                if search_term in self.word_bag_passage[str(passage_id)].keys():
                    Vi_num[search_term] += 1

        # 计算 P(X|R) 与 P(X|nonR)
        for result_index in range(0, len(search_result)):
            passage_id = search_result[result_index]['docID']
            sim_score = 0

            for search_term in search_content:
                # 仅当 query 与 doc 中均包含当前 term 项，sim 计算公式中的 w 权值才为 1
                if search_term in self.word_bag_passage[str(passage_id)].keys():
                    # 计算 P（X|R）= Vi + 0.5 / V + 1
                    p_R = (float(Vi_num[search_term]) + 0.5) / (float(V_num) + 1)
                    # 计算 P(X|nonR) = (ni - Vi + 0.5) / (N - V + 1)
                    p_nonR = (float(len(self.words_doc[search_term]) - Vi_num[search_term]) + 0.5) / (float(self.doc_number - V_num) + 1)

                    sim_term = self.calculate_sim_term(p_R, p_nonR)
                    sim_score += sim_term

            # store the calculated score
            search_result[result_index]['score'] = sim_score

        return search_result


if __name__ == '__main__':
    # obj = SearchAgent()
    # obj.readFile()
    # obj.save_corpus()

    obj = SearchAgent()
    obj.load_corpus()   # 加载已经计算好的语料库数据
    result0 = obj.search_languageModel("王菲与Beyond合唱的歌")
    result0=obj.search_languageModel("王菲 合 唱的歌 Beyond ")
    result1 = obj.search_improved1("王菲与Beyond合唱的歌")
    result2 = obj.search_improved2("王菲与Beyond合唱的歌")
    result3 = obj.search_improved3("王菲与Beyond合唱的歌")
    result0.sort(key=lambda k: k['score'],reverse=True)
    result1.sort(key=lambda k: k['score'], reverse=True)
    result2.sort(key=lambda k: k['score'], reverse=True)
    result3.sort(key=lambda k: k['score'], reverse=True)
    #result0 = dict(sorted(result0.items(), key=lambda d: d[1], reverse=True))
    #print(result0[0].get('docID'))
    print(result0)
    print(result1)
    print(result2)
    print(result3)
    print('finished')

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