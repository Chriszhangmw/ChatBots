


with open('./test.tsv','r',encoding='utf-8') as f:
    data = f.readlines()
    f.close()
p = 0
n = 0
m = 0
all = 0
for line in data:
    line = line.strip().split('\t')
    all +=1
    if line[0] == '0':
        p +=1
    elif line[0] == '1':
        n +=1
    elif line[0] == '2':
        m +=1

print(p,n,m,all)