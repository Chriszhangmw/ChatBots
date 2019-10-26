import  jieba.posseg
jieba.load_userdict("./vocab_jieba_pog.txt")
clean_question = '急性硫化氢中毒一般吃什么样的药'

question_seged=jieba.posseg.cut(str(clean_question))
for word,pog in question_seged:
    print(word)
    print(pog)
# print(question_seged)