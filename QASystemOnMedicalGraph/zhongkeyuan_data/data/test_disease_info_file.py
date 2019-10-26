


with open('./disease_info.csv','r',encoding='utf-8') as f:
    data = f.readlines()
for line in data:
    line = line.strip()
    line = line.split(',')
    if len(line) != 9:
        print(222)