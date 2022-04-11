import pickle
import function_lib
# all_freq = {}   # 总词频
# all_posting_1 = {}   # 总posting 1  A - F
# all_posting_2 = {}   # 总posting 2  G - K
# all_posting_3 = {}   # 总posting 3  L - P
# all_posting_4 = {}   # 总posting 4  Q - U
# all_posting_5 = {}   # 总posting 5  V - Z

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

with open('./storage/song_freq.data','rb') as f:
    song_freq = pickle.load(f)
with open('./storage/singer_freq.data','rb') as f:
    singer_freq = pickle.load(f)
with open('./storage/style_freq.data','rb') as f:
    style_freq = pickle.load(f)
with open('./storage/words_freq.data','rb') as f:
    words_freq = pickle.load(f)



# 对指定某个posting list 进行update
def all_posting_update(word, passageID, freq_num, posting_index):
    if posting_index == 1:
        if word not in all_posting_1.keys():
            all_posting_1[word] = dict()
            all_posting_1[word][passageID] = freq_num
        else:
            if passageID not in all_posting_1[word].keys():
                all_posting_1[word][passageID] = freq_num

    if posting_index == 2:
        if word not in all_posting_2.keys():
            all_posting_2[word] = dict()
            all_posting_2[word][passageID] = freq_num
        else:
            if passageID not in all_posting_2[word].keys():
                all_posting_2[word][passageID] = freq_num

    if posting_index == 3:
        if word not in all_posting_3.keys():
            all_posting_3[word] = dict()
            all_posting_3[word][passageID] = freq_num
        else:
            if passageID not in all_posting_3[word].keys():
                all_posting_3[word][passageID] = freq_num

    if posting_index == 4:
        if word not in all_posting_4.keys():
            all_posting_4[word] = dict()
            all_posting_4[word][passageID] = freq_num
        else:
            if passageID not in all_posting_4[word].keys():
                all_posting_4[word][passageID] = freq_num

    if posting_index == 5:
        if word not in all_posting_5.keys():
            all_posting_5[word] = dict()
            all_posting_5[word][passageID] = freq_num
        else:
            if passageID not in all_posting_5[word].keys():
                all_posting_5[word][passageID] = freq_num


# parser 的工作，将新的键值对提交给 Inverter
def parserAnalyze(word_list, passageID_list, freq_list):
    for i in range(0, len(word_list)):
        letter = function_lib.getFirstLetter(word_list[i])

        if letter >= "A" and letter <= 'F':
            all_posting_update(word_list[i], passageID_list[i], freq_list[i], 1)
            print('New job allocated to Inverter ' + str(1))
        elif letter >= "G" and letter <= 'K':
            all_posting_update(word_list[i], passageID_list[i], freq_list[i], 2)
            print('New job allocated to Inverter ' + str(2))
        elif letter >= "L" and letter <= 'P':
            all_posting_update(word_list[i], passageID_list[i], freq_list[i], 3)
            print('New job allocated to Inverter ' + str(3))
        elif letter >= "Q" and letter <= 'U':
            all_posting_update(word_list[i], passageID_list[i], freq_list[i], 4)
            print('New job allocated to Inverter ' + str(4))
        elif letter >= "V" and letter <= 'Z':
            all_posting_update(word_list[i], passageID_list[i], freq_list[i], 5)
            print('New job allocated to Inverter ' + str(5))



def updateNewPassage(fileName, passageID):
    print("\n\n-------------------------\n Master Node Starting Updating : ")
    with open(fileName, "r", encoding='UTF-8') as f:  # 打开文件
        data = f.read()  # 读取文件
        temp = data.split()  # temp中存放file中所有词

    single_doc = {}  # 单篇文章中出现的词
    for j in temp:
        if j != '$END':
            if j not in single_doc.keys():
                single_doc[j] = 1
            else:
                single_doc[j] += 1

    i = 0
    while i < len(single_doc.keys()) - 10:
        assignment_keys = list(single_doc.keys())[i:i+9]
        print("New assignment indexing from " + str(i) + " to " + str(i + 9) + " is assigned to a parser.")
        # parser job
        freq_sublist = [single_doc[key] for key in assignment_keys]
        parserAnalyze(assignment_keys, [passageID for i in range(0, 10)], freq_sublist)
        i += 10

    assignment_keys = list(single_doc.keys())[i:len(single_doc.keys())]
    print("New assignment indexing from " + str(i) + " to " + str(len(single_doc.keys())) + " is assigned to a parser.")
    freq_sublist = [single_doc[key] for key in assignment_keys]
    parserAnalyze(assignment_keys, [passageID for i in range(0, len(assignment_keys))], freq_sublist)


# 对指定某个 zone posting 进行update
def zone_posting_update(word, passageID, freq_num, posting_index):
    if posting_index == 1:  # song
        if word not in song_freq.keys():
            song_freq[word] = dict()
            song_freq[word][passageID] = freq_num
        else:
            if passageID not in song_freq[word].keys():
                song_freq[word][passageID] = freq_num

    if posting_index == 2:  # singer
        if word not in singer_freq.keys():
            singer_freq[word] = dict()
            singer_freq[word][passageID] = freq_num
        else:
            if passageID not in singer_freq[word].keys():
                singer_freq[word][passageID] = freq_num

    if posting_index == 3:  # style
        if word not in style_freq.keys():
            style_freq[word] = dict()
            style_freq[word][passageID] = freq_num
        else:
            if passageID not in style_freq[word].keys():
                style_freq[word][passageID] = freq_num

    if posting_index == 4:  # words
        if word not in words_freq.keys():
            words_freq[word] = dict()
            words_freq[word][passageID] = freq_num
        else:
            if passageID not in words_freq[word].keys():
                words_freq[word][passageID] = freq_num



# update the zone structure
def updateZones(fileName, passageID):
    print("\n\n-------------------------\n Starting Parsing Zone File Updates: ")
    with open(fileName, "r", encoding='UTF-8') as f:  # 打开文件
        data = f.read()  # 读取文件
        temp = data.split()  # temp中存放file中所有词

    if len(temp) < 4:
        print("Error found in " + fileName)
        return

    # song
    zone_posting_update(temp[0], passageID, 1, 1)
    print('New job allocated to Inverter "Song"')
    # singer
    zone_posting_update(temp[1], passageID, 1, 2)
    print('New job allocated to Inverter "Singer"')
    # style
    temp_index = 2
    while temp[temp_index] != "$END":
        zone_posting_update(temp[temp_index], passageID, 1, 3)
        print('New job allocated to Inverter "Style"')
        temp_index += 1

    # words
    single_doc = {}
    for j in range(temp_index + 1, len(temp)):
        word = temp[j]
        if word not in single_doc.keys():
            single_doc[word] = 1
        else:
            single_doc[word] += 1

    i = 0
    while i < len(single_doc.keys()) - 10:
        assignment_keys = list(single_doc.keys())[i:i+9]
        print("New assignment indexing from " + str(i) + " to " + str(i + 9) + " is assigned to a parser.")
        # parser job
        freq_sublist = [single_doc[key] for key in assignment_keys]

        # parser's work
        for x in range(0, len(assignment_keys)):
            zone_posting_update(assignment_keys[x], passageID, freq_sublist[x], 4)
            print('New job allocated to Inverter "Word"')

        i += 10

    assignment_keys = list(single_doc.keys())[i:len(single_doc.keys())]
    print("New assignment indexing from " + str(i) + " to " + str(len(single_doc.keys())) + " is assigned to a parser.")
    freq_sublist = [single_doc[key] for key in assignment_keys]

    # parser's work
    for i in range(0, len(assignment_keys)):
        zone_posting_update(assignment_keys[i], passageID, freq_sublist[i], 4)
        print('New job allocated to Inverter "Word"')





print("system load finished.")
updateNewPassage("./75.txt", 75)
updateZones("./75.txt", 75)
print('update complete')
print(all_freq)
print(all_posting_1)
#print(words_freq['风'])
#print(all_posting_1)

