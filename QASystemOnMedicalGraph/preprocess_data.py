
from question_template import QuestionTemplate


import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
# blockPrint()

# enablePrint()



class Question():
    def __init__(self):
        # 初始化相关设置：读取词汇表，训练分类器，连接数据库
        self.qt = QuestionTemplate()
    def question_process(self,question,  main_words):
        # 调用问题模板类中的获取答案的方法
        try:
            print('开始处理')
            answer,main_words=self.qt.get_question_answer(question,main_words)
        except:
            answer="你好,我是Chris助理小甜甜，如有回答不上，请联系Chris医生，电话是：www.github.com/chriszhang."
            main_words = ''
        return answer,main_words




