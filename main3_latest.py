import sys
import random
import MeCab
import pymysql

import normalize
import extractKeywords
import flattenList
import reply
import jtalk
import shiritori
import weather


# 新しい単語を格納する時に候補となるリスト
genres = ['人名', '場所', '地位', '時間', '生物', '感情', '状態', '職業', '理由', '人', '環境', '社会' + \
    , '娯楽', '道具', '主体', '客体', '体', '性格', '行動', '単位', '乗り物', '数字', '自然', '学問', '方法' + \
    , '方向', '物体', '飲食物', '数量', '文化', '色', '衣類']


genres_print = '[人, 人名, 主体, 客体, 場所, 地位, 時間, 生物, 感情, 状態, 職業,' + '\n'
            + '理由, 環境, 社会, 娯楽, 道具, 体, 性格, 行動, 単位, 乗り物, 数字,' + '\n'
            + '自然, 学問, 方法, 方向, 物体, 飲食物, 数量, 文化, 色, 衣類]'


if __name__ == '__main__':
    print('''
        モード一覧
            ・会話: デフォルト
            ・しりとり: "しりとり"と入力すると起動する
            ・天気: "天気"と入力すると起動する
    ''')

    while True:
        input_sentence = input('入力: ')
        input_normed = normalize.normalizeNeologd(input_sentence)

        # モードが指定されたか判定する
        if 'しりとり' in input_normed:
            shiritori.Shiritori()
            continue
        elif '天気' in input_normed:
            print('\n' + weather.Weather() + '\n')
            jtalk.jtalk(weather.Weather())
            continue
        elif input_normed.startswith('終了'):
            sys.exit()

        word_list = extractKeywords.extractKeywords(input_normed)

        # 名詞が存在する文章が入力されるまでループする
        try:
            input_meishi = random.choice(word_list)
        except IndexError as e:
            reply = map(str, reply.Reply1())
            reply = ','.join(reply)
            print(reply)
            jtalk.jtalk(reply)
            continue

        with pymysql.connect(db='kaken', user='kaken', passwd='', charset='utf8') as c:
            # 名詞のみ(単語)が入力された場合
            if input_meishi == input_sentence:
                pass
            elif c.execute("SELECT 属性 FROM meishi_tbl WHERE 名詞 = \'{}\';".format(input_meishi)):
                # DB上に存在する名詞が入力された場合
                zokusei_list = c.fetchone()
                zokusei_sql = zokusei_list[0]
                c.execute("SELECT 名詞 FROM meishi_tbl WHERE 属性 = \'{}\';".format(zokusei_sql))
                meishi_list = c.fetchall()
                meishi_flattenlist = flattenList.flattenList(meishi_list)
                meishi_sql = random.sample(meishi_flattenlist, 1)
                meishi_sql = map(str, meishi_sql)
                meishi_str = ','.join(meishi_sql)
                reply = map(str, reply.Reply2(input_meishi, zokusei_sql, meishi_str))
                reply = ','.join(reply)
                print(reply)
                reply = reply.replace('\"', '')
                jtalk.jtalk(reply)
            else:
                # DB上に存在しない名詞が入力された場合
                reply = map(str, reply.Reply3(input_meishi))
                reply = ','.join(reply)
                print(reply)
                reply = reply.replace('\"', '')
                jtalk.jtalk(reply)
                print(genres_print)
                input_sentence = input('\n入力: ')
                input_normed = normalize.normalizeNeologd(input_sentence)

                # DBに新しい名詞を格納するため、属性情報をユーザーに入力してもらう
                while True:
                    if input_normed in genres:
                        break
                    else:
                        print('上の中から一番近いものを選んでね。')
                        jtalk.jtalk('上の中から一番近いものを選んでね。')
                        input_sentence = input('入力: ')
                        input_normed = normalize.normalizeNeologd(input_sentence)

                # お礼を言う
                c.execute("INSERT INTO meishi_tbl(名詞, 属性) VALUES(\'{0}\', \'{1}\')".format(input_meishi, input_normed))
                reply = map(str, reply.Reply4())
                reply = ','.join(reply)
                print(reply)
                jtalk.jtalk(reply)
