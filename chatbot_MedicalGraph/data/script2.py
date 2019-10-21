
####alias word proposing
with open('alias_vocab.txt','r',encoding='utf-8') as f:
    alias = f.readlines()
    f.close()

alias_vocab = open('./new_data/alias.txt','w',encoding='utf-8')

words = []
for word in alias:
    word = word.strip()
    words.append(word)
words = list(set(words))
for i in range(len(words)):
    if str(words[i]) != '':
        alias_vocab.write(str(i) + ',' + str(words[i]) + '\n')

####complications words proposing
# with open('complications_vocab.txt','r',encoding='utf-8') as f:
#     complications = f.readlines()
#     f.close()
#
# complications_vocab = open('./new_data/complications.txt','w',encoding='utf-8')
#
# words = []
# for word in complications:
#     word = word.strip()
#     words.append(word)
# words = list(set(words))
# for i in range(len(words)):
#     if str(words[i]) != '':
#         complications_vocab.write(str(i) + ',' + str(words[i]) + '\n')


###symptom words procesing
# with open('symptom_vocab.txt','r',encoding='utf-8') as f:
#     symptom = f.readlines()
#     f.close()
#
# symptom_vocab = open('./new_data/symptom.txt','w',encoding='utf-8')
#
# words = []
# for word in symptom:
#     word = word.strip()
#     words.append(word)
# words = list(set(words))
# for i in range(len(words)):
#     if str(words[i]) != '':
#         symptom_vocab.write(str(i) + ',' + str(words[i]) + '\n')

