
disease = open('./new_data/disease.csv','w',encoding='utf-8')
disease_atrr = open('./new_data/disease_atrr.csv','w',encoding='utf-8')


with open('./new_data/disease_info.csv','r',encoding='utf-8') as f:
    data = f.readlines()
    f.close()
for i in range(1,len(data)):
    line = data[i]
    line = line.strip().split(',')
    id = line[0]
    name = line[1]
    disease.write(str(id) + ',' + str(name) + '\n')
    part = '一般的发病部位为：' + line[2]
    age = '主要集中在' + line[3] +'群体中'
    infect = '传染性参考：' + line[4]
    insurance = '根据医保条列，该病纳入医保情况为：' + line[5]
    department = '所属科室：' + line[6]
    checklist = '建议检查项目：'+line[7]
    treatment = '治疗手参考：' + line[8]
    drugs = '常用药：' + line[9]
    period = '治疗周期：'+line[10]
    rate = '治愈率（仅供参考）：'+line[11]
    money = '费用（仅供参考）：'+line[12]

    disease_atrr.write(str(id) + ','+ name+','+ part+';'+age+';'+infect+';'+insurance
                       +';'+department+';'+checklist+';'+treatment+';'+drugs+';'+period+';'+rate+';'+money + '\n')
