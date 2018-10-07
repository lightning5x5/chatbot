import random


# 入力された文に名詞が含まれなかった時に使用される関数
def reply1():
    reply1 = [
        '名詞がないよ。',
        '名詞がないようです。',
        '名詞が見つかりません。'
    ]

    return random.sample(reply1, 1)


# 抽出された名詞がDB上に存在した時に使用される関数
def reply2(input_meishi, zokusei_sql, meishi_str):
    reply2 = [
        input_meishi + 'って\"' + zokusei_sql + '\"だよね！！',
        input_meishi + 'は\"' + zokusei_sql + '\"ですよね。',
        '\"' + zokusei_sql + '\"といえば\"' + meishi_str + '\"だよね。',
        '\"' + zokusei_sql + '\"といえば\"' + meishi_str + '\"ですよね。',
        '\"' + input_meishi + '\"といえば\"' + zokusei_sql + '\"だけど、\"' + zokusei_sql + '\"といえば\"' + meishi_str + '\"だよね。',
        '\"' + input_meishi + '\"といえば\"' + zokusei_sql + '\"ですが、\"' + zokusei_sql + '\"といえば\"' + meishi_str + '\"ですよね。',
        '\"' + input_meishi + '\"といえば\"' + zokusei_sql + '\"だけど、他にも\"' + meishi_str + '\"とかあるよね。',
        '\"' + input_meishi + '\"といえば\"' + zokusei_sql + '\"ですが、他にも\"' + meishi_str + '\"とかありますよね。'
    ]

    return random.sample(reply2, 1)


# 抽出された名詞がDB上に存在しなかった時に使用される関数
def reply3(input_meishi):
    reply3 = [
        '\"' + input_meishi + '\"って何？\n' + '次の中から選んで！！\n',
        '\"' + input_meishi + '\"とは何でしょう。\n' + '次の中から選んでいただけませんか？\n'
    ]

    return random.sample(reply3, 1)


# お礼を表示する時に使用される関数
def reply4():
    reply4 = [
        'ありがとう。',
        'ありがとうございます。'
    ]

    return random.sample(reply4, 1)
