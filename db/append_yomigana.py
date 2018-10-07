import pymysql
import MeCab


def yomigana(text):
    tagger = MeCab.Tagger('-Oyomi -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
    reply_word = tagger.parse(text).rstrip('\n')
    return text


with pymysql.connect(db='kaken', user='kaken', passwd='', charset='utf8') as c:
    c.execute("SELECT 名詞 FROM meishi_tbl")
    result = c.fetchall()
    for _ in range(1):
        for word in result:
            c.execute("INSERT INTO Shiritori() VALUES(\'{0}\', \'{1}\')".format(word[0], yomigana(word[0])))
    c.execute("DELETE FROM Shiritori WHERE 名詞 = 読み")
