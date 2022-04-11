import pickle

# with open('bat.data','rb') as f:
#     data = pickle.load(f)


all_freq = {}   # 总词频
with open('./storage/all_freq.data','wb') as f:
    pickle.dump(all_freq,f)

song_freq = {}   # 歌曲名
with open('./storage/song_freq.data','wb') as f:
    pickle.dump(song_freq,f)

singer_freq = {}   # 歌手名
with open('./storage/singer_freq.data','wb') as f:
    pickle.dump(singer_freq,f)

style_freq = {}  # 风格
with open('./storage/style_freq.data','wb') as f:
    pickle.dump(style_freq,f)

words_freq = {}   # 歌词
with open('./storage/words_freq.data','wb') as f:
    pickle.dump(words_freq,f)



all_posting_1 = {}   # 总posting 1  A - F
with open('./storage/all_posting_1.data','wb') as f:
    pickle.dump(all_posting_1,f)

all_posting_2 = {}   # 总posting 2  G - K
with open('./storage/all_posting_2.data','wb') as f:
    pickle.dump(all_posting_2,f)

all_posting_3 = {}   # 总posting 3  L - P
with open('./storage/all_posting_3.data','wb') as f:
    pickle.dump(all_posting_3,f)

all_posting_4 = {}   # 总posting 4  Q - U
with open('./storage/all_posting_4.data','wb') as f:
    pickle.dump(all_posting_4,f)

all_posting_5 = {}   # 总posting 5  V - Z
with open('./storage/all_posting_5.data','wb') as f:
    pickle.dump(all_posting_5,f)