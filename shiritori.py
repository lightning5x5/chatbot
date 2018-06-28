import os
import pymysql
import MeCab


def Yomigana(text):
    tagger = MeCab.Tagger('-Oyomi -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
    reply_word = tagger.parse(text).rstrip('\n')
    return reply_word


def headChar(Str):
    str_h = Str[len(Str) - 1]

    if str_h == 'ァ':                #拗音の処理------ここから
        str_h = 'ア'                 #          |
    elif str_h == 'ィ':              #          |
        str_h = 'イ'                 #          |
    elif str_h == 'ゥ':              #          |
        str_h = 'ウ'                 #          |
    elif str_h == 'ェ':              #          |
        str_h = 'エ'                 #          |
    elif str_h == 'ォ':              #          |
        str_h = 'オ'                 #          |
    elif str_h == 'ャ':              #          |
        str_h = 'ヤ'                 #          |
    elif str_h == 'ュ'               #          |
        str_h = 'ユ'                 #          |
    elif str_h == 'ョ'               #          |
        str_h = 'ヨ'                 #          |
    elif str_h == 'ッ':              #          V
        str_h = 'ツ'                 #--------------ここまで
    if str_h == 'ー':                #長音の場合１つ前の文字を使用
        str_h = Str[len(Str) - 2]
    return str_h


def Shiritori():
    print('''
ルールは次に説明するようになるよ
長音「ー」は一つ前の文字が入力になるよ
「ぁぃぅぇぉゃゅょ」は「あいうえおやゆよ」として扱うよ
降参するときは「参った」または「負けました」, 「ギブアップ」っていってね！
ボクから行くね！

しりとり
''', end='')

    swap = list()
    FLAG = 0                #人工無脳から見て、勝ち : １  負け : 0
    FLAG_EXIT = 0                #勝敗が決した時のみ １

    with pymysql.connect(db='kaken', user='kaken', passwd='', charset='utf8') as c:
        last_char = 'リ'                #しりとりの「り」
        swap.append('シリトリ')

        while FLAG_EXIT == 0:                #勝敗がつくまで続ける
            word = input('\n入力: ')

            if '参った' in word:
                FLAG = 1
                FLAG_EXIT = 1
                break
            elif '負' in word:
                FLAG = 1
                FLAG_EXIT = 1
                break
            elif 'ギブアップ' in word:
                FLAG = 1
                FLAG_EXIT = 1
                break

            word = Yomigana(word)

            try:
                if word[0] != last_char:                #最初の文字が最後の文字と異なるとき
                    print('最初の文字は\"{}\"だよ'.format(last_char))
                    continue
            except IndexError as e:
                print('文字を入力してね')
                continue

            head = headChar(word)                #最後の文字をheadに代入

            if head == 'ン':                #'ん'がつくと負けのルール
                print('\"ん\"がついたから負けだよーん')
                FLAG = 1
                FLAG_EXIT = 1

            if word in swap:
                print('\"{}\"は２回目だから君の負けだよ'.format(word))                #同じ文字を２回使うと負けルール
                FLAG = 1
                FLAG_EXIT = 1
                break

            swap.append(word)

            c.execute("SELECT * FROM Shiritori WHERE 読み LIKE \'{}%\'".format(head))                #headから始まる単語をサーチ　=> data
            data = c.fetchall()
            data_n = len(data)                #data(名詞)の個数をdata_nとして格納

            if data_n == 1 or data_n == 0:
                print('\nん〜\"{}\"から始まる言葉が思いつかないなぁ\n僕の負けだね'.format(head))
                FLAG = 0
                FLAG_EXIT = 1

            for i in range(data_n - 1):
                if i == data_n and data[i] == data[data_n - 1]:
                    print('負けました')
                    FLAG = 0                #負けのフラグを立ててブレーク
                    FLAG_EXIT = 1

                if data[i][1] in str(swap):                #もしも現在の単語が一度出てきた場合
                    continue
                else:
                    last_char = headChar(data[i][1][len(data[i][1]) - 1])
                    if last_char == 'ン':
                        continue

                    print(data[i][0])
                    swap.append(data[i][1] + ',')
                    break

    if FLAG == 1:                #勝った場合
        print('\n私の勝ちですね!!\nやりました！\n')
        print('しりとりの終了\n')
    elif FLAG == 0:                #負けた場合
        print('\n負けたぁぁくうぅやしいぃぃぃぃ↑↑\n')
        print('しりとりの終了\n')
