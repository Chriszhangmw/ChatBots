import  jieba.posseg

a = '前列腺炎怎么治疗呢'
question_seged=jieba.posseg.cut(str(a))
result=[]
question_word, question_flag = [], []
for w in question_seged:
    temp_word=f"{w.word}/{w.flag}"
    result.append(temp_word)
    # 预处理问题
    word, flag = w.word,w.flag
    print('*****')
    print(word)
    print(flag)
    print(temp_word)
    print('*****')
    question_word.append(str(word).strip())
    question_flag.append(str(flag).strip())

