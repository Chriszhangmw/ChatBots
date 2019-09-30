
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import tensorflow as tf
import bert_code.modeling as modeling
import argparse
import bert_code.run_classifier as run_classifier
import bert_code.tokenization as tokenization
from processor import fffffuck
from text_loader import TextLoader
import numpy as np


#超参数
parser = argparse.ArgumentParser()
parser.add_argument("-e",'--EPOCHS',default=20,type=int,help="train epochs")
parser.add_argument("-b","--BATCH_SIZE",default=16,type=int,help="the batch size")
args = parser.parse_args()

epochs = 20000
batch_size = 4
max_sentence_length = 64


lr = 5e-6  # 学习率
# 配置文件
bert_root = './bert_model_chinese'
bert_config_file = os.path.join(bert_root, 'bert_config.json')
bert_config = modeling.BertConfig.from_json_file(bert_config_file)
init_checkpoint = os.path.join(bert_root, 'bert_model.ckpt')
bert_vocab_file = os.path.join(bert_root, 'vocab.txt')
# token = tokenization.CharTokenizer(vocab_file=bert_vocab_file)


#获取数据
data_path = './dat'
train_input,eval_input =fffffuck(data_path,bert_vocab_file,True,True,
                                               './temp',max_sentence_length,batch_size,batch_size)

# data_loader = TextLoader(train_input,batch_size)
# x_train,y_train = data_loader.next_batch(4)
# print(y_train)
# print(train_input)

input_ids = tf.placeholder(tf.int32, shape=[None, None], name='input_ids')
input_mask = tf.placeholder(tf.int32, shape=[None, None], name='input_masks')
segment_ids = tf.placeholder(tf.int32, shape=[None, None], name='segment_ids')
input_y = tf.placeholder(tf.float32, shape=[None,1], name="input_y")
weights = {
    'out': tf.Variable(tf.random_normal([768, 1]))
}
biases = {
    'out': tf.Variable(tf.constant(0.1, shape=[1, ]))
}
model = modeling.BertModel(
    config=bert_config,
    is_training=False,
    input_ids=input_ids,
    input_mask=input_mask,
    token_type_ids=segment_ids,
    use_one_hot_embeddings=False)
tvars = tf.trainable_variables()
(assignment, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars, init_checkpoint)
tf.train.init_from_checkpoint(init_checkpoint, assignment)
output_layer_pooled = model.get_pooled_output()  # 这个获取句子的output
output_layer_pooled = tf.nn.dropout(output_layer_pooled, keep_prob=0.8)
print('output_layer_pooled shape is ',output_layer_pooled.get_shape())

w_out = weights['out']
b_out = biases['out']
pred = tf.add(tf.matmul(output_layer_pooled, w_out), b_out, name="pre1")
probabilities = tf.nn.softmax(pred, axis=-1)
log_probs = tf.nn.log_softmax(pred, axis=-1)
# one_hot_labels = tf.one_hot(input_y, depth=3, dtype=tf.float32)


pred = tf.reshape(pred,shape=[-1,1],name= 'pre')
print(pred)
loss=tf.reduce_mean(tf.square(tf.reshape(pred, [-1]) - tf.reshape(input_y, [-1])))
# print('pred ************* shape:',pred.get_shape())
# loss = tf.nn.softmax_cross_entropy_with_logits_v2(logits=pred,labels=input_y)

train_op = tf.train.AdamOptimizer(lr).minimize(loss)
with tf.Session() as sess:
    # with tf.device('/gpu:0'):
    sess.run(tf.global_variables_initializer())
    data_loader = TextLoader(train_input,batch_size)
    for i in range(epochs):
        data_loader.shuff()
        for j in range(data_loader.num_batches):
            x_train,y_train = data_loader.next_batch(j)
            # print('x_train shape is :',x_train.shape)
            # print(x_train)

            x_input_ids = x_train[:,0]
            x_input_mask = x_train[:,1]
            x_segment_ids = x_train[:,2]

            loss_, _ = sess.run([loss, train_op],
                                feed_dict={input_ids: x_input_ids, input_mask: x_input_mask, segment_ids: x_segment_ids,
                                           input_y: y_train})
            print('the epoch number is : %d the index of batch is :%d, the loss value is :%f', i,j,loss_)

    # modelpp.save_model(sess, MODEL_PATH, overwrite=True)
























