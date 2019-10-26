import pandas as pd
#diseaseID,part,age,infect,insurance,department,checklist,treatment,drugs,period,rate,money
# data = pd.read_csv('disease_info.csv','r',encoding='utf-8')
# print(data['money'])
# print(data['part'].isnull().value_counts())

with open('./disease_info.csv','r',encoding='utf-8') as f:
    data = f.readlines()
    f.close()
for i in range(1,len(data)):
    line = data[i]
    line = line.strip().split(',')
    if len(line) != 13:
        print(len(line))
        print(data[i])

