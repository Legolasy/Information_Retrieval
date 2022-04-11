#pragma once
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <map>
using namespace std;


class Term{
public:
	string term_str;  // 字符串内容
	int freq;         // 字符串频率
	map<int, int> docs;     // 记录文档频率

	Term(string s) {   // 构造函数
		term_str = s;
		freq = 0;
	}

	void add_doc(int docID, int doc_freq) {
		map<int, int>::iterator iter;
		iter = docs.find(docID);

		if (iter == docs.end())   // 新增文档不能已经存在
			docs.insert(std::pair<int, int>(docID, doc_freq));

		freq += doc_freq;
	}

	bool operator == (const Term &p) {
		return (term_str == p.term_str);
	}

	vector<int> getDocs() {
		vector<int> result;
		map<int, int>::iterator doc_iter;
		for (doc_iter = docs.begin(); doc_iter != docs.end(); doc_iter++) {
			result.push_back(doc_iter->first);
		}
		sort(result.begin(), result.end());
		return result;
	}
};



class Statistics {
public:

	Statistics();                       // 默认构造函数
	Statistics(string data_path);       // 在构造对象时，将指定目录下所有文档数据添加进来

	void init_data(string data_path);   // 读入指定目录下的所有文档数据

	void addFile(string file_path);     // 向已有的统计数据中加入一个文档

	void display();                     // 展示统计结果


	vector<int> AND(vector<int> setA, vector<int> setB);
	vector<int> OR(vector<int> setA, vector<int> setB);
	vector<int> AND_NOT(vector<int> setA, vector<int> setB);
	vector<int> OR_NOT(vector<int> setA, vector<int> setB);

	void user_search();
	vector<int> search_word(string word);

private:
	vector<Term> terms;              // 记录系统中所有的 term 数据
	map<int, string> doc_Diction;    // 记录各文档的编号
	int next_doc;
};
