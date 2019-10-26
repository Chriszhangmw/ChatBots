

# write_1 = open('./data_for_neo4j/acompany.csv','w',encoding='utf-8')
write_2 = open('./data_for_neo4j/relation/rels_acompany.csv','w',encoding='utf-8')
# write_3 = open('./data_for_neo4j/acompany.csv','w',encoding='utf-8')


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

with open('./data_for_neo4j/acompany.csv','r',encoding='utf-8') as f2:
    acompany = f2.readlines()
f2.close()
acompany_dic = {}
for line in acompany:
    line = line.strip()
    line = line.split(',')
    name = line[1]
    id = line[0]
    acompany_dic[name] = id

with open('./rels_acompany.csv','r',encoding='utf-8') as f:
    data = f.readlines()

words = []
for line in data:
    line = line.strip()
    line = line.split(',')
    name = line[0]
    acompany = line[1]
    if (name in diseases_dic.keys()) & (acompany in acompany_dic.keys()):
        id1 = diseases_dic[name]
        id2 = acompany_dic[acompany]
        write_2.write(str(id1) + ',' + str(id2) + '\n')



    # write_1.write(str(count) + ',' + acompany + '\n')
    # if name in diseases_dic.keys():
    #     write_2.write(str(diseases_dic[name]) + ',' + str(count) + '\n')
