

'''



9:nnt 参演评分 小于 x
10:nnt 电影类型
11:nnt nnr 合作 电影列表
12:nnt 电影数量
13:nnt 出生日期
'''
from query import Query
import re

class QuestionTemplate():
    def __init__(self):
        self.q_template_dict={
            0:self.get_disease_info,
            1:self.get_symptom,
            2:self.get_treatment,
            3:self.get_checklist,
            4:self.get_department,
            5:self.get_curerate,
            6:self.get_period}

        # 连接数据库
        self.graph = Query()
        # 测试数据库是否连接上
        # result=self.graph.run("match (m:Movie)-[]->() where m.title='卧虎藏龙' return m.rating")
        # print(result)
        # exit()

    def get_question_answer(self,question,template):
        # 如果问题模板的格式不正确则结束
        # assert len(str(template).strip().split("\t"))==2
        template_id,template_str=int(str(template).strip().split("\t")[0]),str(template).strip().split("\t")[1]
        self.template_id=template_id
        self.template_str2list=str(template_str).split()

        # 预处理问题
        question_word,question_flag=[],[]
        for one in question:
            word, flag = one.split("/")
            question_word.append(str(word).strip())
            question_flag.append(str(flag).strip())
        # assert len(question_flag)==len(question_word)
        self.question_word=question_word
        self.question_flag=question_flag
        self.raw_question=question
        print('函数里面这里得到的id',template_id)
        # 根据问题模板来做对应的处理，获取答案
        answer=self.q_template_dict[template_id]()
        print('answer:',answer)
        return answer

    # 获取疾病信息
    def get_disease_name(self):
        ## 获取n在原问题中的下标
        tag_index = self.question_flag.index("n")
        print('tag_index is :',tag_index)
        ## 获取疾病名称
        disease_name = self.question_word[tag_index]
        return disease_name
    # def get_name(self,type_str):
    #     name_count=self.question_flag.count(type_str)
    #     if name_count==1:
    #         ## 获取n在原问题中的下标
    #         tag_index = self.question_flag.index(type_str)
    #         ## 获取疾病名称
    #         name = self.question_word[tag_index]
    #         return name
    #     else:
    #         result_list=[]
    #         for i,flag in enumerate(self.question_flag):
    #             if flag==str(type_str):
    #                 result_list.append(self.question_word[i])
    #         return result_list
    #
    # def get_num_x(self):
    #     x = re.sub(r'\D', "", "".join(self.question_word))
    #     return x
    # 0:查询疾病
    def get_disease_info(self):
        # 获取疾病名称，这个是在原问题中抽取的
        disease_name=self.get_disease_name()
        print('disease_name',disease_name)
        cql = f"match (m:Disease_attr)-[]->() where m.disease_name='{disease_name}' return m.atrrs"
        print(cql)
        answer= self.graph.run(cql)
        print(answer)
        # answer = round(answer, 2)
        final_answer=disease_name+"的特点主要有"+str(answer)+"！"
        return final_answer
    # 1:查询症状
    def get_symptom(self):
        disease_name = self.get_disease_name()
        cql = f"match(m:Disease)-[r:diseaseTOsymptom]->(n:Symptom) where m.disease_name='{disease_name}' return n.symptom"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = disease_name + "的基本症状包括但不限于" + str(answer) + "！"
        return final_answer
    # 2:查询治疗方案
    def get_treatment(self):
        disease_name = self.get_disease_name()
        cql = f"match (m:Disease)-[]->() where m.disease_name='{disease_name}' return m.treatment"
        print(cql)
        answer = self.graph.run(cql)[0]
        answer_set=set(answer)
        answer_list=list(answer_set)
        answer="、".join(answer_list)
        final_answer = disease_name + "主流的治疗方法有：" + str(answer) + "！"
        return final_answer
    # 3:查询检查项目
    def get_checklist(self):
        disease_name = self.get_disease_name()
        cql = f"match (m:Disease)-[]->() where m.disease_name='{disease_name}' return m.checklist"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = disease_name + "一般会建议做如下检查：" + str(answer) + "！"
        return final_answer
    # 4:查询科室
    def get_department(self):
        disease_name=self.get_disease_name()
        cql = f"match (m:Disease)-[]->() where m.disease_name='{disease_name}' return m.department"
        print(cql)
        answer = self.graph.run(cql)[0]
        answer_set = set(answer)
        answer_list = list(answer_set)
        answer = "、".join(answer_list)
        final_answer = disease_name + "可以挂" + str(answer) + "等科室，或者咨询导医台！"
        return final_answer
    # 5:查询治愈率
    def get_curerate(self):
        disease_name = self.get_disease_name()
        cql = f"match (m:Disease)-[]->() where m.disease_name='{disease_name}' return m.rate"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = disease_name + "根据目前医疗水平被治疗的概率估计为：" + str(answer) + "！"
        return final_answer
    # 6:治疗周期
    def get_period(self):
        disease_name = self.get_disease_name()
        # 查询电影名称
        cql = f"match (m:Disease)-[]->() where m.disease_name='{disease_name}' return m.period"
        print(cql)
        answer = self.graph.run(cql)[0]
        final_answer = disease_name + "一般的治疗周期为：" + str(answer) + "，主要还是针对检查结果由医生确定！"
        return final_answer
