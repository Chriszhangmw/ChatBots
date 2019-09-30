
import  numpy as np
with open('./train.tsv','r',encoding='utf-8') as f:
    X_train = f.readlines()
    X_train = np.array(X_train)
    f.close()
from collections import Counter
nums = []
for i in range(1,X_train.shape[0]):
    nums.append(len(str(X_train[i]).split('\t')[1]))
sum(nums) / len(nums)
max(nums)
cc = Counter(nums)
def less_than_percent(n):
    n_ = 0
    for k, v in cc.items():
        if k <= n:
            n_ += v
    return n_ / len(nums)
print(less_than_percent(64))