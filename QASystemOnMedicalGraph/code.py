

import sys
import web
from preprocess_data import Question
render = web.template.render('templates/')

urls = ('/', 'index','/add','add')
app = web.application(urls, globals())
que = Question()
print("create question object finish! ")

# 主页显示类
class index:
    def GET(self):
        return render.index()

    def POST(self):
        text=web.input()
        print(text)
        raise web.seeother('/')

# 处理问题类
class add:
    def __init__(self):
        self.main_words = ''
    # get方式处理问题
    def GET(self):
        self.main_words = ''
        # pass

    # post方式处理问题
    def POST(self):

        def enablePrint():
            sys.stdout = sys.__stdout__
        enablePrint()

        text=web.input()
        # 简单的过滤掉无效post请求
        if text['id']=="bei":
            question=text['q']
            print("received question:",question)
            print("now get answer!")
            answer,sendcond=dealquestion(question,self.main_words)
            self.main_words = sendcond
            print("得到的答案是：",answer)
            if len(str(answer).strip())==0:
                answer="我也不知道，请联系主治医师或咨询门诊咨询控制台 ：）"
            print("return answer!")
            return answer
        else:
            pass


# 处理问题的方法
def dealquestion(question,main_words):
    # 查询知识图谱

    answer,sendcond=que.question_process(question,  main_words)
    # answer=12

    return answer,sendcond

if __name__=="__main__":
    web.internalerror = web.debugerror

    app.run()