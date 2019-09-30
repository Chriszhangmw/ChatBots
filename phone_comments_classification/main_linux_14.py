
import os
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf
from project_model import Project_model
from processor import fffffuck
from text_loader import TextLoader
import numpy as np


#超参数
epochs = 20000
batch_size = 16
max_len = 64
lr = 5e-6  # 学习率
keep_prob = 0.8
bert_root = './bert_model_chinese'
bert_vocab_file = os.path.join(bert_root, 'vocab.txt')
model_save_path = './model/simi.model'

#获取数据
data_path = './dat'
train_input,eval_input,predict_input =fffffuck(data_path,bert_vocab_file,True,True,True,
                                               './temp',max_len,batch_size)
def train():
    model = Project_model(bert_root,data_path,'./temp',model_save_path,batch_size,max_len,lr,keep_prob)
    with tf.Session() as sess:
        with tf.device('/XLA_CPU:0'):
            writer = tf.summary.FileWriter('./tf_log/', sess.graph)
            # saver = tf.train.Saver()
            saver = tf.train.Saver()
            best_score = 0.0  # record the best score
            sess.run(tf.global_variables_initializer())
            data_loader = TextLoader(train_input,batch_size)
            for i in range(epochs):
                data_loader.shuff()
                for j in range(data_loader.num_batches):
                    x_train,y_train = data_loader.next_batch(j)
                    step, loss_ ,log= model.run_step(sess,x_train,y_train)
                    writer.add_summary(log, global_step=step)
                    print('the epoch number is : %d the index of batch is :%d, the loss value is :%f'%(i, j, loss_))
                    if ((i + 1)*data_loader.num_batches + j) % 10 == 0:
                        cur_score = model.evaluate(sess,eval_input)
                        print('****************the average validation dataset accurancy is *****************', cur_score)
                        if cur_score > best_score:
                            saver.save(sess,'./model14/simi.model',global_step=step,write_state=True)
                            best_score = cur_score

import matplotlib.pyplot as plt
import itertools

def plot_confusion_matrix(cm, classes, title='Confusion matrix'):
    plt.imshow(cm, interpolation='nearest', cmap=None)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=0)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

def plot_matrix(y_true, y_pred):
    from sklearn.metrics import confusion_matrix
    confusion_matrix = confusion_matrix(y_true, y_pred)
    class_names = ['positive', 'negative','middle']
    plot_confusion_matrix(confusion_matrix
                          , classes=class_names
                          , title='Confusion matrix')
def test():
    data_loader = TextLoader(predict_input,batch_size)
    saver = tf.train.import_meta_graph('./model/simi.model.meta')
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, tf.train.latest_checkpoint('./model/'))
        inputs_id = tf.get_default_graph().get_tensor_by_name('input_ids:0')
        inputs_pos = tf.get_default_graph().get_tensor_by_name('input_masks:0')
        inputs_type = tf.get_default_graph().get_tensor_by_name('segment_ids:0')
        y = tf.get_default_graph().get_tensor_by_name('y:0')
        true_label = []
        pre_label = []
        for i in range(data_loader.num_batches):
            x_test, label = data_loader.next_batch(i)
            x_input_ids = x_test[:, 0]
            x_input_mask = x_test[:, 1]
            x_segment_ids = x_test[:, 2]
            prediction = sess.run(y,feed_dict={inputs_id: x_input_ids, inputs_pos: x_input_mask,
                                                      inputs_type: x_segment_ids})
            prediction = np.argmax(prediction,1)
            for i in label:
                true_label.append(i)
            for j in prediction:
                pre_label.append(j)
    plot_matrix(true_label, pre_label)


if __name__ == '__main__':
    test()


