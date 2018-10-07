import MeCab


def extract_keywords(text):
    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse('')
    node = tagger.parseToNode(text)
    keyword = []
    while node:
        if node.feature.split(',')[0] == '名詞':
            keyword.append(node.surface)
        node = node.next
    return keyword


txt_read = open(u'hoge.txt', 'r')
csv_write = open(u'hoge.csv', 'w')
txt_data = txt_read.read()

Subjects = extract_keywords(txt_data)
for words in Subjects:
    csv_write.write(words)
    csv_write.write(',\n')

txt_read.close()
csv_write.close()
