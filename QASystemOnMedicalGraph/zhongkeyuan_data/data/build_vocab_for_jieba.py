

words = []
with open('./checks.csv','r',encoding='utf-8') as f1:
    data1 = f1.readlines()
for word in data1:
    word = word.strip()
    words.append(word)
with open('./departments.csv','r',encoding='utf-8') as f2:
    data2 = f2.readlines()
for word in data2:
    word = word.strip()
    words.append(word)
with open('./diseases.csv','r',encoding='utf-8') as f3:
    data3 = f3.readlines()
for word in data3:
    word = word.strip()
    words.append(word)
with open('./drugs.csv','r',encoding='utf-8') as f4:
    data4 = f4.readlines()
for word in data4:
    word = word.strip()
    words.append(word)
with open('./foods.csv','r',encoding='utf-8') as f5:
    data5 = f5.readlines()
for word in data5:
    word = word.strip()
    words.append(word)
with open('./producers.csv','r',encoding='utf-8') as f6:
    data6 = f6.readlines()
for word in data6:
    word = word.strip()
    words.append(word)
with open('./symptoms.csv','r',encoding='utf-8') as f7:
    data7 = f7.readlines()
for word in data7:
    word = word.strip()
    words.append(word)
words = list(set(words))
write_in = open('./vocab_for_jieba.txt','w',encoding='utf-8')
for word in words:
    write_in.write(word + '\n')

