




#diseases
# with open('diseases.csv','r',encoding='utf-8') as f:
#     diseases_ = f.readlines()
#     f.close()
#
# diseases = open('./data_for_neo4j/diseases.csv','w',encoding='utf-8')
#
# words = []
# for word in diseases_:
#     word = word.strip()
#     words.append(word)
# words = list(set(words))
# for i in range(len(words)):
#     if str(words[i]) != '':
#         diseases.write(str(i) + ',' + str(words[i]) + '\n')


# #checks
# with open('checks.csv','r',encoding='utf-8') as f:
#     diseases_ = f.readlines()
#     f.close()
#
# diseases = open('./data_for_neo4j/checks.csv','w',encoding='utf-8')
#
# words = []
# for word in diseases_:
#     word = word.strip()
#     words.append(word)
# words = list(set(words))
# for i in range(len(words)):
#     if str(words[i]) != '':
#         diseases.write(str(i) + ',' + str(words[i]) + '\n')


#departments
# with open('symptoms.csv','r',encoding='utf-8') as f:
#     diseases_ = f.readlines()
#     f.close()
#
# diseases = open('./data_for_neo4j/symptoms.csv','w',encoding='utf-8')
#
# words = []
# for word in diseases_:
#     word = word.strip()
#     words.append(word)
# words = list(set(words))
# for i in range(len(words)):
#     if str(words[i]) != '':
#         diseases.write(str(i) + ',' + str(words[i]) + '\n')


with open('./data_for_neo4j/diseases.csv','r',encoding='utf-8') as f1:
    diseases = f1.readlines()
f1.close()
diseases_dic = {}
for line in diseases:
    line = line.strip()
    line = line.split(',')
    name = line[1]
    id = line[0]
    diseases_dic[name] = id


with open('./data_for_neo4j/departments.csv','r',encoding='utf-8') as f0:
    departments = f0.readlines()
f0.close()
departments_dic = {}
# print(departments)
for line in departments:
    line = line.strip()
    line = line.split(',')
    name = line[1]
    id = line[0]
    # print(name)
    departments_dic[name] = id
# print(departments_dic)


with open('./data_for_neo4j/checks.csv','r',encoding='utf-8') as f00:
    checks = f00.readlines()
f00.close()
checks_dic = {}
for line in checks:
    line = line.strip()
    line = line.split(',')
    name = line[1]
    id = line[0]
    checks_dic[name] = id
with open('./data_for_neo4j/drugs.csv','r',encoding='utf-8') as f01:
    drugs = f01.readlines()
drugs_dic = {}
for line in drugs:
    line = line.strip()
    line = line.split(',')
    name = line[1]
    id = line[0]
    drugs_dic[name] = id
with open('./data_for_neo4j/foods.csv','r',encoding='utf-8') as f02:
    foods = f02.readlines()
foods_dic = {}
for line in foods:
    line = line.strip()
    line = line.split(',')
    name = line[1]
    id = line[0]
    foods_dic[name] = id
with open('./data_for_neo4j/producers.csv','r',encoding='utf-8') as f03:
    producers = f03.readlines()
producer_dic = {}
for line in producers:
    line = line.strip()
    line = line.split(',')
    name = line[1]
    id = line[0]
    producer_dic[name] = id
with open('./data_for_neo4j/symptoms.csv','r',encoding='utf-8') as f04:
    dymptoms = f04.readlines()
symptoms_dic = {}
for line in dymptoms:
    line = line.strip()
    line = line.split(',')
    name = line[1]
    id = line[0]
    symptoms_dic[name] = id


write_in = open('./data_for_neo4j/disease_info.csv','w',encoding='utf-8')

with open('./disease_info.csv','r',encoding='utf-8') as f2:
    data = f2.readlines()
f2.close()
for line in data:
    line = line.strip()
    line = line.split(',')
    name = line[0]
    # name = line[1:]
    if name in diseases_dic.keys():
        id = str(diseases_dic[name])
        write_in.write(id + ',' + ','.join(line) + '\n')













