import os
import pickle
import function_lib
import simpleSearch
with open('./storage/all_freq.data','rb') as f:
    all_freq = pickle.load(f)
with open('./storage/all_posting_1.data','rb') as f:
    all_posting_1 = pickle.load(f)
with open('./storage/all_posting_2.data','rb') as f:
    all_posting_2 = pickle.load(f)
with open('./storage/all_posting_3.data','rb') as f:
    all_posting_3 = pickle.load(f)
with open('./storage/all_posting_4.data','rb') as f:
    all_posting_4 = pickle.load(f)
with open('./storage/all_posting_5.data','rb') as f:
    all_posting_5 = pickle.load(f)

def simpleParse(tar_string):
    letter = function_lib.getFirstLetter(tar_string)
    if "A" <= letter and letter <= 'F':
        return 1
    elif 'G' <= letter and letter <= 'K':
        return 2
    elif 'L' <= letter and letter <= 'P':
        return 3
    elif 'Q' <= letter and letter <= 'U':
        return 4
    elif 'V' <= letter and letter <= 'Z':
        return 5


def simpleSearch(key_str):
    posting_ID = simpleParse(key_str)
    if posting_ID == 1:
        if key_str in all_posting_1.keys():
            return all_posting_1[key_str]
        else:
            return {}
    if posting_ID == 2:
        if key_str in all_posting_2.keys():
            return all_posting_2[key_str]
        else:
            return {}
    if posting_ID == 3:
        if key_str in all_posting_3.keys():
            return all_posting_3[key_str]
        else:
            return {}
    if posting_ID == 4:
        if key_str in all_posting_4.keys():
            return all_posting_4[key_str]
        else:
            return {}
    if posting_ID == 5:
        if key_str in all_posting_5.keys():
            return all_posting_5[key_str]
        else:
            return {}

# ------- Test ----------------
test = simpleSearch('风')
print(test)
test = simpleSearch('爱情')
print(test)