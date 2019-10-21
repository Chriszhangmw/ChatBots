import pandas as pd
import re
# disease = pd.read_csv('./disease.csv','r')
# with open('./disease.csv','r',encoding='utf-8') as f:
#     disease = f.readlines()
#     f.close()

# disease_info = open('./new_data/disease_info.csv','w',encoding='utf-8')
# n = 0
# for i in range(1,len(disease)):
#     line = str(disease[i].strip()).split(',')
#     if len(line) != 20:
#         print(len(line))

all_data = pd.read_csv('./disease.csv', encoding='utf-8').loc[:, :].values
print(len(all_data))

disease_info = open('./new_data/disease_info.csv','w',encoding='utf-8')
disease_alias = open('./new_data/disease_alias.csv','w',encoding='utf-8')
disease_complication = open('./new_data/disease_complication.csv','w',encoding='utf-8')
disease_symptom = open('./new_data/disease_symptom.csv','w',encoding='utf-8')


alias_dic = {}
with open('./new_data/alias.csv','r',encoding='utf-8') as f1:
    data1 = f1.readlines()
    f1.close()
for line in data1:
    line = line.strip().split(',')
    alias_dic[line[1]] = line[0]

complication_dic = {}
with open('./new_data/complications.csv','r',encoding='utf-8') as f2:
    data2 = f2.readlines()
    f2.close()
for line in data2:
    line = line.strip().split(',')
    complication_dic[line[1]] = line[0]

symptom_dic = {}
with open('./new_data/symptom.csv','r',encoding='utf-8') as f3:
    data3 = f3.readlines()
    f3.close()
for line in data3:
    line = line.strip().split(',')
    symptom_dic[line[1]] = line[0]



i = 1
for data in all_data:
    # 疾病
    disease = str(data[0]).replace("...", " ").strip()
    # 别名
    temp_alias = []
    line = re.sub("[，、；,.;]", " ", str(data[1]).replace("...", " ")) if str(data[1]).replace("...", " ") else "未知"
    for alias in line.strip().split():
        if alias in alias_dic.keys():
            disease_alias.write(str(i) + ',' + str(alias_dic[alias]) + '\n')
        temp_alias.append(alias)
    temp_alias = ' '.join(temp_alias)
    # 部位
    temp_parts = []
    part_list = str(data[2]).replace("...", " ").strip().split() if str(data[2]) else "未知"
    for part in part_list:
        temp_parts.append(part)
    temp_parts = ' '.join(temp_parts).strip()
    # 年龄
    temp1 = str(data[3]).replace("...,", " ").strip()
    temp1 = temp1.replace(',','')
    age = temp1 if temp1 else "未知"
    # 传染性
    infect = str(data[4]).replace("...", " ").strip() if str(data[4]) else "未知"
    # 医保
    insurance = str(data[5]).replace("...", " ").strip() if str(data[5]) else "未知"
    # 科室
    temp_apartment = []
    department_list = str(data[6]).replace("...", " ").strip().split()
    for department in department_list:
        temp_apartment.append(department)
    if len(temp_apartment) == 0:
        temp_apartment.append('咨询导医台')
    temp_apartment = ' '.join(temp_apartment).strip()
    # 检查项
    check = str(data[7]).replace("...", " ").strip() if str(data[7]) else "未知"
    # 症状
    temp_symptom = []
    symptom_list = str(data[8]).replace("...", " ").strip().split()[:-1]
    for symptom in symptom_list:
        if symptom in symptom_dic.keys():
            disease_complication.write(str(i) + ',' + str(symptom_dic[symptom]) + '\n')
        temp_symptom.append(symptom)
    if len(temp_symptom) == 0:
        temp_symptom.append('未知')
    temp_symptom = ' '.join(temp_symptom).strip()
    # 并发症
    temp_complication = []
    complication_list = str(data[9]).replace("...", " ").strip().split()[:-1] if str(data[9]) else "未知"
    for complication in complication_list:
        if complication in complication_dic.keys():
            disease_symptom.write(str(i) + ',' + complication_dic[complication] + '\n')
        temp_complication.append(complication)
    if len(temp_complication) == 0:
        temp_complication.append('未知')
    temp_complication = ' '.join(temp_complication).strip()
    # 治疗方法
    temp5 = str(data[10]).replace("...", " ").strip()
    temp5 = temp5.replace(',','')
    treat = temp5[:-4] if temp5[:-4] else "未知"
    # 药品
    temp_drug = []
    drug_string = str(data[11]).replace("...", " ").strip()
    for drug in drug_string.split()[:-1]:
        temp_drug.append(drug)
    if len(temp_drug) ==0:
        temp_drug.append('未知')
    temp_drug = ' '.join(temp_drug).strip()
    # 治愈周期
    temp4 = str(data[12]).replace("...", " ").strip()
    temp4 = temp4.replace(',','')
    period =  temp4 if temp4 else "未知"
    # 治愈率
    temp2 = str(data[13]).replace("...", " ").strip()
    temp2 = temp2.replace(',','')
    rate = temp2 if temp2 else "未知"
    # 费用
    temp3 = str(data[14]).replace("...", " ").strip()
    temp3 = temp3.replace(',','')
    money = temp3 if temp3 else "未知"

    line = str(i) + ','+disease+','+temp_parts+','+age+','+infect+','+insurance\
           +','+temp_apartment+','+check+','+treat+','+temp_drug+','+period+','+rate+','+money + '\n'
    disease_info.write(line)
    i +=1















