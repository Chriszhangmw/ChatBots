

'''



9:nnt 参演评分 小于 x
10:nnt 电影类型
11:nnt nnr 合作 电影列表
12:nnt 电影数量
13:nnt 出生日期
'''
from query import Query
import re
from sentence_calssification import QuestionClassifier

class QuestionTemplate():
    def __init__(self):
        # self.q_template_dict={
        #     0:self.disease_symptom,
        #     1:self.symptom_disease,
        #     2:self.disease_cause,
        #     3:self.disease_acompany,
        #     4:self.disease_not_food,
        #     5:self.disease_do_food,
        #     6:self.food_not_disease,
        #     7: self.food_do_disease,
        #     8: self.disease_drug,
        #     9: self.drug_disease,
        #     10: self.disease_check,
        #     11: self.check_disease,
        #     12: self.disease_prevent,
        #     13: self.disease_lasttime,
        #     14: self.disease_cureway,
        #     15: self.disease_cureprob,
        #     16: self.disease_easyget,
        #     17: self.disease_desc,
        #     18: self.symptom_disease}
        # 连接数据库
        self.graph = Query()


    def get_question_answer(self,question,main_words):

        qc = QuestionClassifier()
        print('77777777777777')
        data = qc.classify(question)
        print('888888888888')
        print(main_words)
        print(data)
        if len(data['args'].keys()) > 0:
            for key in data['args'].keys():
                main_words = key
        # main_words = data['args'].keys()
        print('999999999999999999')
        print(main_words)
        question_type = data['question_types'] #可能是个包含多个查询关系
        for question in question_type:
            print(question)
            print(main_words)
            answer = self.answer_prettify(question,main_words)
            print('answer:', answer)

        return answer,main_words

    def answer_prettify(self, question_type,main_words):
        final_answer = []
        if question_type == 'disease_symptom':
            result = self.disease_symptom(main_words)
            final_answer = '{0}的症状包括：{1}'.format(main_words, ''.join(list(set(result))))
        elif question_type == 'symptom_disease':
            result = self.symptom_disease(main_words)
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(main_words, ''.join(list(set(result))))
        elif question_type == 'disease_cause':
            result = self.disease_cause(main_words)
            final_answer = '{0}可能的成因有：{1}'.format(main_words, ''.join(list(set(result))))

        elif question_type == 'disease_prevent':
            result = self.disease_prevent(main_words)
            final_answer = '{0}的预防措施包括：{1}'.format(main_words,''.join(list(set(result))))
        elif question_type == 'disease_lasttime':
            result = self.disease_lasttime(main_words)
            final_answer = '{0}治疗可能持续的周期为：{1}'.format(main_words,''.join(list(set(result))))

        elif question_type == 'disease_cureway':
            result = self.disease_cureway(main_words)
            final_answer = '{0}可以尝试如下治疗：{1}'.format(main_words, ''.join(list(set(result))))

        elif question_type == 'disease_cureprob':
            result = self.disease_cureprob(main_words)
            final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(main_words, ''.join(list(set(result))))

        elif question_type == 'disease_easyget':
            result = self.disease_easyget(main_words)
            final_answer = '{0}的易感人群包括：{1}'.format(main_words, ''.join(list(set(result))))

        elif question_type == 'disease_desc':
            result = self.disease_desc(main_words)
            final_answer = '{0},熟悉一下：{1}'.format(main_words,''.join(list(set(result))))

        elif question_type == 'disease_acompany':
            result = self.disease_acompany(main_words)
            final_answer = '{0}的并发症状包括：{1}'.format(main_words, ''.join(list(set(result))))

        elif question_type == 'disease_not_food':
            result = self.disease_not_food(main_words)
            final_answer = '{0}忌食的食物包括有：{1}'.format(main_words, ''.join(list(set(result))))

        elif question_type == 'disease_do_food':
            result = self.disease_do_food(main_words)
            final_answer = '{0}宜食的食物包括有：{1}'.format(main_words, ''.join(list(set(result))))

        elif question_type == 'food_not_disease':
            result = self.food_not_disease(main_words)
            final_answer = '患有{0}的人最好不要吃{1}'.format(main_words, ''.join(list(set(result))))

        elif question_type == 'food_do_disease':
            result = self.food_do_disease(main_words)
            final_answer = '患有{0}的人建议多试试{1}'.format(main_words, ''.join(list(set(result))))

        elif question_type == 'disease_drug':
            result = self.disease_drug(main_words)
            final_answer = '{0}通常的使用的药品包括：{1}'.format(main_words, ''.join(list(set(result))))

        elif question_type == 'drug_disease':
            result = self.drug_disease(main_words)
            final_answer = '{0}主治的疾病有{1},可以试试'.format(main_words, ''.join(list(set(result))))

        elif question_type == 'disease_check':
            result = self.disease_check(main_words)
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(main_words, ''.join(list(set(result))))

        elif question_type == 'check_disease':
            result = self.check_disease(main_words)
            final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(main_words, ''.join(list(set(result))))

        return final_answer
    def disease_symptom(self,main_word):
        # 获取疾病名称，这个是在原问题中抽取的
        disease_name=main_word
        cql = f"match (m:disease)-[r:rels_symptom]->(n:symptom) where m.diseaseName='{disease_name}' return n.symptomName"
        print(cql)
        answer= self.graph.run(cql)
        result = []
        for word in answer:
            result.append(word)
        answer = '、'.join(result)
        return answer
    def symptom_disease(self,main_word):
        symptom = main_word
        cql = f"match(m:symptom)-[r:rels_symptom]->(n:disease) where m.symptomName='{symptom}' return n.diseaseName"
        print(cql)
        answer = self.graph.run(cql)
        result = []
        for word in answer:
            result.append(word)
        answer = '、'.join(result)
        return answer
    def disease_cause(self,main_word):
        disease_name = main_word
        cql = f"match (m:disease_info) where m.diseaseName='{disease_name}' return m.diseaseCause"

        print(cql)
        answer = self.graph.run(cql)[0]
        return answer
    def disease_prevent(self,main_word):
        disease_name = main_word
        cql = f"match (m:disease_info) where m.diseaseName='{disease_name}' return m.diseasePrvent"
        print(cql)
        answer = self.graph.run(cql)[0]
        return answer
    def disease_lasttime(self,main_word):
        disease_name=main_word
        cql = f"match (m:disease_info) where m.diseaseName='{disease_name}' return m.diseaseLasttime"
        print(cql)
        answer = self.graph.run(cql)[0]
        return answer
    def disease_cureway(self,main_word):
        disease_name = main_word
        cql = f"match (m:disease_info) where m.diseaseName='{disease_name}' return m.diseaseCure_way"
        print(cql)
        answer = self.graph.run(cql)[0]
        return answer
    def disease_cureprob(self,main_word):
        disease_name = main_word
        cql = f"match (m:disease_info) where m.diseaseName='{disease_name}' return m.diseaseCure_pro"
        print(cql)
        answer = self.graph.run(cql)[0]
        return answer
    def disease_easyget(self,main_word):
        disease_name = main_word
        cql = f"match (m:disease_info) where m.diseaseName='{disease_name}' return m.diseaseEasy_get"
        print(cql)
        answer = self.graph.run(cql)[0]
        return answer
    def disease_desc(self,main_word):
        disease_name = main_word
        cql = f"match (m:disease_info) where m.diseaseName='{disease_name}' return m.diseaseDesc"
        print(cql)
        answer = self.graph.run(cql)[0]
        return answer
    def disease_acompany(self,main_word):
        disease_name = main_word
        cql = f"match (m:disease)-[r:rels_acompany]->(n:acompany) where m.diseaseName='{disease_name}' return n.acompanyName"
        print(cql)
        answer = self.graph.run(cql)
        result = []
        for word in answer:
            result.append(word)
        answer = '、'.join(result)
        return answer
    def disease_not_food(self,main_word):
        disease_name = main_word
        cql = f"match (m:disease)-[r:rels_noeat]->(n:foods) where m.diseaseName='{disease_name}' return n.foodName"
        print(cql)
        answer = self.graph.run(cql)
        result = []
        for word in answer:
            result.append(word)
        answer = '、'.join(result)
        return answer
    def disease_do_food(self,main_word):
        disease_name = main_word
        cql = f"match (m:disease)-[r:rels_doeat]->(n:foods) where m.diseaseName='{disease_name}' return n.foodName"
        print(cql)
        answer = self.graph.run(cql)
        result = []
        for word in answer:
            result.append(word)
        answer = '、'.join(result)
        return answer
    def food_not_disease(self,main_word):
        disease_name = main_word
        cql = f"match (n:foods)-[r:rels_noeat]->(m:disease) where n.foodName='{disease_name}' return m.diseaseName"
        print(cql)
        answer = self.graph.run(cql)
        result = []
        for word in answer:
            result.append(word)
        answer = '、'.join(result)
        return answer
    def food_do_disease(self,main_word):
        disease_name = main_word
        cql = f"match (n:foods)-[r:rels_doeat]->(m:disease) where n.foodName='{disease_name}' return m.diseaseName"
        print(cql)
        answer = self.graph.run(cql)
        result = []
        for word in answer:
            result.append(word)
        answer = '、'.join(result)
        return answer
    def disease_drug(self,main_word):
        disease_name = main_word
        cql = f"match (m:disease)-[r:rels_recommanddrug]->(n:drugs) where m.diseaseName='{disease_name}' return n.drugName"
        print(cql)
        answer = self.graph.run(cql)
        result = []
        for word in answer:
            result.append(word)
        answer = '、'.join(result)
        return answer
    def disease_check(self,main_word):
        disease_name = main_word
        cql = f"match (m:disease)-[r:rels_check]->(n:checks) where m.diseaseName='{disease_name}' return n.checksName"
        print(cql)
        answer = self.graph.run(cql)
        print('first',answer)
        result = []
        for word in answer:
            result.append(word)
        answer = '、'.join(result)
        print('second', answer)
        return answer
    def check_disease(self,main_word):
        disease_name = main_word
        cql = f"match (m:checks)-[]->(n:disease) where m.checksName='{disease_name}' return n.diseaseName"
        print(cql)
        answer = self.graph.run(cql)
        result = []
        for word in answer:
            result.append(word)
        answer = '、'.join(result)
        return answer


if __name__ == "__main__":
    qt = QuestionTemplate()
    question = '肝炎一般需要做什么检查呢'
    answer = qt.get_question_answer(question)
    print(answer)