

# new_ = open('./new.csv','w',encoding='utf-8')
with open('./new.csv','r',encoding='utf-8') as f:
    data = f.readlines()

# print(len(data))
for i in range(len(data)):
    line = data[i]
    line = line.strip()
    line = line.split(',')
    for j in range(len(line)):
        if line[j] == '':
            print(222)
            # line[j] = '未知'

    # new_.write(','.join(line) + '\n')
        # new_.write(','.join(line))
            # print(j)
            # print(data[i])