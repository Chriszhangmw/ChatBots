

import numpy as np
from keras.utils import to_categorical


class TextLoader(object):
    def __init__(self, dataSet,batch_size):
        self.data = dataSet
        self.batch_size = batch_size
        self.shuff()

    def shuff(self):
        self.num_batches = int(len(self.data) // self.batch_size)
        if self.num_batches == 0:
            assert False, 'Not enough data, make batch_size small.'
        np.random.shuffle(self.data)

    def next_batch(self,k):
        x = []
        y = []
        for i in range(self.batch_size):
            tmp = list(self.data)[k*self.batch_size + i][:3]
            x.append(tmp)
            y_ = list(self.data)[k*self.batch_size + i][3]
            y.append(y_)
        x = np.array(x)
        # y = np.array(y).T
        return x,np.array(y)
        # return x, np.array(y).reshape([self.batch_size, 1]) 自己得代码









