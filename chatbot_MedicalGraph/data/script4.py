
with open('./vocab_jieba.txt','r',encoding='utf-8') as f:
    data = f.readlines()
    f.close()

write_in = open('./vocab_jieba_pog.txt','w',encoding='utf-8')
for word in data:
    word = word.strip()
    word = word + ' ' + 'nr' + '\n'
    write_in.write(word)

