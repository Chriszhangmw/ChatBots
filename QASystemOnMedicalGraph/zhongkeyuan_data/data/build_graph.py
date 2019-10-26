import os
import json
from py2neo import Graph,Node
from pandas.core.frame import DataFrame

disease_info = open('./disease_info.csv','w',encoding='utf-8')
drugs = open('./drugs.csv','w',encoding='utf-8')
foods = open('./foods.csv','w',encoding='utf-8')
checks = open('./checks.csv','w',encoding='utf-8')
departments = open('./departments.csv','w',encoding='utf-8')
producers = open('./producers.csv','w',encoding='utf-8')
diseases = open('./diseases.csv','w',encoding='utf-8')
symptoms = open('./symptoms.csv','w',encoding='utf-8')

data_path = './medical.json'
# drugs = ['未知']
# foods = ['未知']
# checks = ['未知']
# departments = ['未知']
# producers = []
# diseases = []
# symptoms = []

disease_infos = []#疾病信息

rels_department = open('./rels_department.csv','w',encoding='utf-8')
rels_noteat = open('./rels_noteat.csv','w',encoding='utf-8')
rels_doeat = open('./rels_doeat.csv','w',encoding='utf-8')
rels_recommandeat = open('./rels_recommandeat.csv','w',encoding='utf-8')
rels_commonddrug = open('./rels_commonddrug.csv','w',encoding='utf-8')
rels_recommanddrug = open('./rels_recommanddrug.csv','w',encoding='utf-8')
rels_check = open('./rels_check.csv','w',encoding='utf-8')
rels_drug_producer = open('./rels_drug_producer.csv','w',encoding='utf-8')
rels_rate_cure = open('./rels_rate_cure.csv','w',encoding='utf-8')
rels_cure_lasttime = open('./rels_cure_lasttime.csv','w',encoding='utf-8')
rels_symptom = open('./rels_symptom.csv','w',encoding='utf-8')
rels_acompany = open('./rels_acompany.csv','w',encoding='utf-8')
rels_category = open('./rels_category.csv','w',encoding='utf-8')

# rels_department = [] #　科室－科室关系
# rels_noteat = [] # 疾病－忌吃食物关系
# rels_doeat = [] # 疾病－宜吃食物关系
# rels_recommandeat = [] # 疾病－推荐吃食物关系
# rels_commonddrug = [] # 疾病－通用药品关系
# rels_recommanddrug = [] # 疾病－热门药品关系
# rels_check = [] # 疾病－检查关系
# rels_drug_producer = [] # 厂商－药物关系
# rels_rate_cure = [] #疾病治疗的概率
# rels_cure_lasttime = [] #疾病需要治疗的时间
# rels_symptom = [] #疾病症状关系
# rels_acompany = [] # 疾病并发关系
# rels_category = [] #　疾病与科室之间的关系

count = 0
for data in open(data_path,encoding='utf-8'):
    # disease_dict = {}
    count +=1
    data_json = json.loads(data)
    disease = data_json['name']
    name = disease.strip()
    diseases.write(name + '\n')
    print(disease)

    desc = '未知'
    prevent = '未知'
    cause = '未知'
    easy_get = '未知'
    cure_department= '未知'
    cure_way = '未知'
    cure_lasttime = '未知'
    symptom = '未知'
    cured_prob = '未知'

    if 'symptom' in data_json:
        for symptom in data_json['symptom']:
            if symptom != '':
                symptoms.write(symptom+'\n')
                rels_symptom.write(disease + ',' + symptom + '\n')


    if 'acompany' in data_json:
        for acompany in data_json['acompany']:
            if acompany != '':
                rels_acompany.write(disease+','+ acompany + '\n')

    if 'desc' in data_json:
        desc = str(data_json['desc']).strip()
        desc = desc.replace(',','')

    if 'prevent' in data_json:
        prevent = str(data_json['prevent']).strip()
        prevent = prevent.replace(',','')

    if 'cause' in data_json:
        cause = str(data_json['cause']).strip()
        cause = cause.replace(',','')

    if 'get_prob' in data_json:
        get_prob = str(data_json['get_prob']).strip()

    if 'easy_get' in data_json:
        easy_get = str(data_json['easy_get']).strip()
        easy_get = easy_get.replace(',','')

    if 'cure_department' in data_json:
        cure_department = data_json['cure_department']
        if len(cure_department) == 1:
            departments.write(cure_department[0] + '\n')
            rels_category.write(disease+','+ cure_department[0] + '\n')
        if len(cure_department) == 2:
            big = cure_department[0]
            small = cure_department[1]
            departments.write(small + '\n')
            departments.write(big + '\n')
            rels_department.write(small+ ',' + big + '\n')
            rels_category.write(disease+','+ small+'\n')

        cure_department = str(cure_department).strip()
        cure_department = cure_department.replace(',','')

    if 'cure_way' in data_json:
        cure_way = str(data_json['cure_way']).strip()
        cure_way = cure_way.replace(',','')

    if 'cure_lasttime' in data_json:
        cure_lasttime = str(data_json['cure_lasttime']).strip()
        cure_lasttime = cure_lasttime.replace(',','')
        rels_cure_lasttime.write(disease+','+cure_lasttime+'\n')

    if 'cured_prob' in data_json:
        cured_prob = str(data_json['cured_prob']).strip()
        cured_prob = cured_prob.replace(',','')
        rels_rate_cure.write(disease+','+cured_prob+'\n')

    if 'common_drug' in data_json:
        common_drug = data_json['common_drug']
        for drug in common_drug:
            if drug != '':
                drugs.write(drug + '\n')
            rels_commonddrug.write(disease+','+ drug+'\n')


    if 'recommand_drug' in data_json:
        recommand_drug = data_json['recommand_drug']
        for drug in recommand_drug:
            if drug != '':
                drugs.write(drug + '\n')
            rels_recommanddrug.write(disease+','+drug+'\n')

    if 'not_eat' in data_json:
        not_eat = data_json['not_eat']
        for _not in not_eat:
            if _not != '':
                foods.write(_not + '\n')
            rels_noteat.write(disease+','+ _not +'\n')

    if 'do_eat' in data_json:
        do_eat = data_json['do_eat']
        for _do in do_eat:
            if _do != '':
                foods.write(_do + '\n')
            rels_doeat.write(disease+','+ _do+'\n')

    if 'recommand_eat' in data_json:
        recommand_eat = data_json['recommand_eat']

        for _recommand in recommand_eat:
            if _recommand != '':
                foods.write(_recommand + '\n')
            rels_recommandeat.write(disease+','+_recommand+'\n')

    if 'check' in data_json:
        check = data_json['check']
        for _check in check:
            if _check != '':
                checks.write(_check + '\n')
            rels_check.write(disease+','+ _check+'\n')
    if 'drug_detail' in data_json:
        drug_detail = data_json['drug_detail']
        producer = [i.split('(')[0] for i in drug_detail]
        for p in producer:
            if p != '':
                producers.write(p + '\n')
        a = [[i.split('(')[0], i.split('(')[-1].replace(')', '')] for i in drug_detail]
        for (a,b) in a:
            rels_drug_producer.write(a+','+b +'\n')


    disease_info.write(disease.strip()+','+
                         desc + ',' +
                         prevent + ',' +
                         cause + ',' +
                         easy_get + ',' +
                         cure_department + ',' +
                         cure_way + ',' +
                         cure_lasttime + ',' +
                         cured_prob + '\n')







# disease_infos=DataFrame(disease_infos)
# disease_infos.to_csv('./disease_info.csv',index=False,encoding='utf-8')



















