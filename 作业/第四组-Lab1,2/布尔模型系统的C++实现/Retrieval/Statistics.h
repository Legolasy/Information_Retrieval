#pragma once
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <map>
using namespace std;


class Term{
public:
	string term_str;  // �ַ�������
	int freq;         // �ַ���Ƶ��
	map<int, int> docs;     // ��¼�ĵ�Ƶ��

	Term(string s) {   // ���캯��
		term_str = s;
		freq = 0;
	}

	void add_doc(int docID, int doc_freq) {
		map<int, int>::iterator iter;
		iter = docs.find(docID);

		if (iter == docs.end())   // �����ĵ������Ѿ�����
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

	Statistics();                       // Ĭ�Ϲ��캯��
	Statistics(string data_path);       // �ڹ������ʱ����ָ��Ŀ¼�������ĵ�������ӽ���

	void init_data(string data_path);   // ����ָ��Ŀ¼�µ������ĵ�����

	void addFile(string file_path);     // �����е�ͳ�������м���һ���ĵ�

	void display();                     // չʾͳ�ƽ��


	vector<int> AND(vector<int> setA, vector<int> setB);
	vector<int> OR(vector<int> setA, vector<int> setB);
	vector<int> AND_NOT(vector<int> setA, vector<int> setB);
	vector<int> OR_NOT(vector<int> setA, vector<int> setB);

	void user_search();
	vector<int> search_word(string word);

private:
	vector<Term> terms;              // ��¼ϵͳ�����е� term ����
	map<int, string> doc_Diction;    // ��¼���ĵ��ı��
	int next_doc;
};
