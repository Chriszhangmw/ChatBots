
#
# def hello():
#     print("hello")
#
# def bye():
#     print("bye")
# b={0:hello,1:bye}
#
# b[0]()
#
# exit()

import sys
import pandas as pd
from pandas import Series, DataFrame
from preprocess_data import Question
# 创建问题处理对象，这样模型就可以常驻内存
que=Question()
# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
enablePrint()
result=que.question_process("肝炎有哪些症状？")
print(result)