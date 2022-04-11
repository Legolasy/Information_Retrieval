import pypinyin

# 返回输入字符串的首字母，中文返回拼音首字母
def getFirstLetter(str):
    if (str[0] >= 'a' and str[0] <= 'z') or (str[0] >= 'A' and str[0] <= 'Z'):
        return str[0].upper()
    else:
        first_character = pypinyin.pinyin(str, style=pypinyin.NORMAL)
        return first_character[0][0][0].upper()

