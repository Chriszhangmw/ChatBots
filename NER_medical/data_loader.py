import numpy as np
import os
from data_processor import get_data

class Data_loader(object):
    def __init__(self, dataSet, batch_size):
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


if __name__ == '__main__':
    bert_root = './bert_model_chinese'
    bert_vocab_file = os.path.join(bert_root, 'vocab.txt')
    train_input, eval_input, test_input = get_data('./data',bert_vocab_file,64)
    # print(len(train_input))
    # print(train_input[0][3])
    data = Data_loader(train_input,4)
    for i in range(1):
        x,y = data.next_batch(i)
        print(x[:,0])
        print(x[:,1])
        print(x[:,2])
        print('***'*8)
        print(y)
        # print(x.shape)
        # print(y.shape)



