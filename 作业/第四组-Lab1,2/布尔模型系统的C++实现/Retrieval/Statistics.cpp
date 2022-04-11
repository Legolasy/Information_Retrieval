#include <io.h>
#include <fstream>
#include <algorithm>
#include <Windows.h>
#include "Statistics.h"
using namespace std;


// ��ȡָ��Ŀ¼�µ������ļ�����
void getFiles(std::string path, std::vector<std::string>& files)
{
	//�ļ����
	long hFile = 0;
	//�ļ���Ϣ
	struct _finddata_t fileinfo;
	std::string p;
	//assign���� append׷�� c_strת��������C�ַ�����ָ��
	if ((hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1)
	{
		do
		{
			//�ж��Ƿ����ļ���
			if ((fileinfo.attrib & _A_SUBDIR))
			{
				//����ϵͳ�ڽ���һ����Ŀ¼ʱ��ƥ�䵽��ͷ�����ļ�(��)��"."(��ǰĿ¼)��".."(��һ��Ŀ¼)����Ҫ���Ե����������
				if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0)
					getFiles(p.assign(path).append("\\").append(fileinfo.name), files);
			}
			else
			{
				files.push_back(p.assign(path).append("\\").append(fileinfo.name));
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		_findclose(hFile);
	}
}

// �����Կո�ָ��ַ��������� vector<string>
vector<string> split(string str, string pattern)
{
	string::size_type pos;
	vector<string> result;
	str += pattern;//��չ�ַ����Է������
	int size = str.size();
	for (int i = 0; i < size; i++)
	{
		pos = str.find(pattern, i);
		if (pos < size)
		{
			string s = str.substr(i, pos - i);
			result.push_back(s);
			i = pos + pattern.size() - 1;
		}
	}
	return result;
}

// ���� term ��֮���������
bool compareTerm(const Term &p1, const Term &p2) {
	return p1.term_str < p2.term_str;   // ��������
}

// UTF-8 ����ת��
string UTF8ToGB(const char* str)
{
	string result;
	WCHAR *strSrc;
	LPSTR szRes;

	//�����ʱ�����Ĵ�С
	int i = MultiByteToWideChar(CP_UTF8, 0, str, -1, NULL, 0);
	strSrc = new WCHAR[i + 1];
	MultiByteToWideChar(CP_UTF8, 0, str, -1, strSrc, i);

	//�����ʱ�����Ĵ�С
	i = WideCharToMultiByte(CP_ACP, 0, strSrc, -1, NULL, 0, NULL, NULL);
	szRes = new CHAR[i + 1];
	WideCharToMultiByte(CP_ACP, 0, strSrc, -1, szRes, i, NULL, NULL);

	result = szRes;
	delete[]strSrc;
	delete[]szRes;

	return result;
}

// --------------------------------------------------------------------------------



// Ĭ�Ϲ��캯��
Statistics::Statistics() {
	next_doc = 0;
}                     

// �ڹ������ʱ����ָ��Ŀ¼�������ĵ�������ӽ���
Statistics::Statistics(string data_path) {       
	next_doc = 0;
	init_data(data_path);
}

// ����ָ��Ŀ¼�µ������ĵ�����
void Statistics::init_data(string path) {
	vector<string> file_names;
	getFiles(path, file_names);    // ��ȡ��·���µ������ļ�

	for (int i = 0; i < file_names.size(); i++) {
		cout << "Adding file " << file_names[i] << endl;
		addFile(file_names[i]);    // ��Ӵ��ļ�

		doc_Diction.insert(std::pair<int, string>(next_doc, file_names[i]));
		next_doc++;
	}

	cout << "Finished Adding files.\n";

	// ������ term ���������
	sort(terms.begin(), terms.end(), compareTerm);
	terms.erase(terms.begin());
}



// �����е�ͳ�������м���һ���ĵ�
void Statistics::addFile(string file_path) {
	map<string, int> word_freq;   // ͳ�Ƶ�ǰ����ĵ��Ĵ�Ƶ
	fstream f(file_path, ios::in);

	while (!f.eof()) {
		string s_line;
		getline(f, s_line);

		s_line = UTF8ToGB(s_line.c_str());
		vector<string> content = split(s_line, " ");
		for (int i = 0; i < content.size(); i++) {
			vector<Term>::iterator result = find(terms.begin(), terms.end(), Term(content[i]));

			map<string, int>::iterator it_find;
			it_find = word_freq.find(content[i]);
			if (it_find != word_freq.end()) {   // �ô��Ѿ����ֹ���
				it_find->second += 1;
			}
			else {  // �´�
				word_freq.insert(std::pair<string, int>(content[i], 1));
			}
		}
	}
	f.close();


	map<string, int>::iterator word_iter;   // ����ƪ�����еĴ�Ƶ���������ݼ���
	for (word_iter = word_freq.begin(); word_iter != word_freq.end(); word_iter++) {

		vector<Term>::iterator term_iter = find(terms.begin(), terms.end(), Term(word_iter->first));
		if (term_iter == terms.end()) {   // �½�һ�� term
			Term new_term = Term(word_iter->first);
			new_term.add_doc(next_doc, word_iter->second);
			terms.push_back(new_term);
		}
		else {    // �� term ���Ѿ�����
			(*term_iter).add_doc(next_doc, word_iter->second);
		}  
	}
}


// չʾͳ�ƽ��
void Statistics::display() {
	cout << "��Ƶͳ�ƽ������:\n";

	for (int i = 0; i < terms.size(); i++) {
		cout << terms[i].term_str << "    ���ִ���    \t" << terms[i].freq << "   \t:\n";
		map<int, int>::iterator doc_iter;
		for (doc_iter = terms[i].docs.begin(); doc_iter != terms[i].docs.end(); doc_iter++) {
			cout << "   --- �ĵ� " << doc_iter->first << "  |   \t" << doc_Diction[doc_iter->first] << "  ���ִ���  \t"
				<< doc_iter->second << "   \t\n";
		}
		cout << "------------------------\n\n";
	}
}


vector<int> Statistics::AND(vector<int> setA, vector<int> setB) {
	int p1 = 0, p2 = 0;
	vector<int> result;
	while (p1 != setA.size() && p2 != setB.size()) {
		if (setA[p1] == setB[p2]) {
			result.push_back(setA[p1]);
			p1++;
			p2++;
		}
		else if (setA[p1] < setB[p2]) {
			p1++;
		}
		else {
			p2++;
		}
	}
	return result;
}

vector<int> Statistics::OR(vector<int> setA, vector<int> setB) {
	int p1 = 0, p2 = 0;
	vector<int> result;
	while (p1 != setA.size() && p2 != setB.size()) {
		if (setA[p1] == setB[p2]) {
			result.push_back(setA[p1]);
			p1++;
			p2++;
		}
		else if(setA[p1] < setB[p2]){
			result.push_back(setA[p1]);
			p1++;
		}
		else {
			result.push_back(setB[p2]);
			p2++;
		}
	}

	while (p1 != setA.size()) {
		result.push_back(setA[p1]);
		p1++;
	}
	while (p2 != setB.size()) {
		result.push_back(setB[p2]);
		p2++;
	}

	return result;
}

vector<int> Statistics::AND_NOT(vector<int> setA, vector<int> setB) {
	int p1 = 0, p2 = 0;
	vector<int> result;
	while (p1 != setA.size() && p2 != setB.size()) {
		if (setA[p1] == setB[p2]) {
			p1++;
			p2++;
		}
		else if (setA[p1] < setB[p2]) {
			result.push_back(setA[p1]);
			p1++;
		}
		else {
			p2++;
		}
	}
	while (p1 != setA.size() && p2 == setB.size()) {
		result.push_back(setA[p1]);
		p1++;
	}
	return result;
}

vector<int> Statistics::OR_NOT(vector<int> setA, vector<int> setB) {  // A OR NOT B  == NOT [(NOT A) AND B ]
	vector<int> setC = AND_NOT(setB, setA);   // [(NOT A) AND B ]
	vector<int> full_set;
	for (int i = 0; i < next_doc; i++) {
		full_set.push_back(i);
	}

	return AND_NOT(full_set, setC);
}


bool set_comp(const vector<int> &a, const vector<int> &b)
{
	return a.size() > b.size();  // �Ӵ�С������
}

void Statistics::user_search() {
	vector<vector<int>> wants;
	vector<vector<int>> bans;
	cout << "\n\n******************************************\n��������ϣ�������Ĺؼ���(end ����������)��";
	string temp;

	char szBuf[50];
	while (true) {
		cin.getline(szBuf, 50);
		temp = string(szBuf);
		if (temp == "end") {
			break;
		}

		temp = UTF8ToGB(szBuf);

		vector<int> or_set;
		vector<string> content = split(temp, " ");
		if (content.size() != 0) {
			or_set = search_word(content[0]);
		}
		for (int i = 1; i < content.size(); i++) {
			vector<int> test = search_word(content[i]);
			or_set = OR(or_set, search_word(content[i]));
		}
		wants.push_back(or_set);
	}
	cout << "\n��������ϣ�����õĹؼ���(end ����������)��";


	while (true) {
		cin.getline(szBuf, 51);
		temp = string(szBuf);
		if (temp == "end") {
			break;
		}

		temp = UTF8ToGB(szBuf);

		vector<int> or_set;
		vector<string> content = split(temp, " ");
		if (content.size() != 0)
			or_set = search_word(content[0]);
		for (int i = 1; i < content.size(); i++) {
			or_set = OR(or_set, search_word(content[i]));
		}
		bans.push_back(or_set);
	}

	// �Լ��Ͻ��������ȶ�С�ļ��Ͻ����߼�����
	sort(wants.begin(), wants.end(), set_comp);
	sort(bans.begin(), bans.end(), set_comp);

	vector<int> result = wants.back();
	wants.pop_back();

	while (!(wants.size() == 0 && bans.size() == 0)) {
		if ((bans.size() == 0 && wants.size() != 0) || wants.size() != 0 && wants.back().size() < bans.back().size()) {
			result = AND(result, wants.back());
			wants.pop_back();
		}
		else if (bans.size() != 0) {
			result = AND_NOT(result, bans.back());
			bans.pop_back();
		}
	}

	cout << "\n\n�����������:\n";
	for (int i = 0; i < result.size(); i++) {
		cout << doc_Diction[result[i]] << endl;
	}
}


vector<int> Statistics::search_word(string word) {

	for (int i = 0; i < terms.size(); i++) {
		if (word == terms[i].term_str) {
			return terms[i].getDocs();
		}
	}

	return vector<int>();
}