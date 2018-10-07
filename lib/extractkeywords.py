import MeCab

import jtalk


def extract_keywords(text):
    tagger = MeCab.Tagger('-Ochasen -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
    tagger.parse('')
    node = tagger.parseToNode(text)
    keyword = []

    while node:
        if node.feature.split(',')[0] == '感動詞':
            keyword.append(node.surface)
            print(keyword[0])
            jtalk.jtalk(keyword[0])
            break
        elif node.feature.split(',')[0] == '名詞':
            keyword.append(node.surface)

        node = node.next

    return keyword
