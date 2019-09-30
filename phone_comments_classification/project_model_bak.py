
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


class Project_model():
    def __init__(self,bert_root,data_path,temp_path,model_save_path,batch_size,max_len,lr,keep_prob):
        self.bert_root = bert_root
        self.data_path = data_path
        self.temp_path = temp_path
        self.model_save_path = model_save_path
        self.batch_size = batch_size
        self.max_len = max_len
        self.lr = lr
        self.keep_prob = keep_prob

        self.bert_config()
        self.get_output()
        self.get_loss(True)
        self.get_accuracy()
        self.get_trainOp()


    def bert_config(self):
        bert_config_file = os.path.join(self.bert_root, 'bert_config.json')
        self.bert_config = modeling.BertConfig.from_json_file(bert_config_file)
        self.init_checkpoint = os.path.join(self.bert_root, 'bert_model.ckpt')
        self.bert_vocab_file = os.path.join(self.bert_root, 'vocab.txt')

        self.input_ids = tf.placeholder(tf.int32, shape=[None, None], name='input_ids')
        self.input_mask = tf.placeholder(tf.int32, shape=[None, None], name='input_masks')
        self.segment_ids = tf.placeholder(tf.int32, shape=[None, None], name='segment_ids')
        self.input_y = tf.placeholder(tf.float32, shape=[None, 1], name="input_y")

        self.global_step = tf.Variable(0, trainable=False)

        output_weights = tf.get_variable(
            "output_weights", [768, 1],
            initializer=tf.random_normal_initializer(stddev=0.1))
        output_bias = tf.get_variable(
            "output_bias", [1,], initializer=tf.random_normal_initializer(stddev=0.01))

        self.w_out = output_weights
        self.b_out = output_bias
        model = modeling.BertModel(
            config=self.bert_config,
            is_training=False,
            input_ids=self.input_ids,
            input_mask=self.input_mask,
            token_type_ids=self.segment_ids,
            use_one_hot_embeddings=False)
        tvars = tf.trainable_variables()
        (assignment, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars, self.init_checkpoint)
        tf.train.init_from_checkpoint(self.init_checkpoint, assignment)
        output_layer_pooled = model.get_pooled_output()  # 这个获取句子的output
        self.output_layer_pooled = tf.nn.dropout(output_layer_pooled, keep_prob=self.keep_prob)
        # return self.output_layer_pooled

    def get_output(self):
        self.pred = tf.add(tf.matmul(self.output_layer_pooled, self.w_out), self.b_out, name="pre1")
        self.probabilities = tf.nn.softmax(self.pred , axis=-1,name='probabilities')
        self.log_probs = tf.nn.log_softmax(self.pred , axis=-1,name='log_probs')
        self.pred  = tf.reshape(self.pred , shape=[-1, 1], name='pre')
        # return self.pred

    def get_loss(self,if_regularization):
        net_loss = tf.square(tf.reshape(self.pred, [-1]) - tf.reshape(self.input_y, [-1]))
        if if_regularization:
            tf.add_to_collection(tf.GraphKeys.WEIGHTS, self.w_out)
            tf.add_to_collection(tf.GraphKeys.WEIGHTS, self.b_out)
            regularizer = tf.contrib.layers.l1_regularizer(scale=5.0 / 50000)
            reg_loss = tf.contrib.layers.apply_regularization(regularizer)
            net_loss = net_loss + reg_loss
        self.loss = tf.reduce_mean(net_loss)
        return self.loss

    def get_loss(self,if_regularization):
        net_loss = tf.square(tf.reshape(self.pred, [-1]) - tf.reshape(self.input_y, [-1]))
        if if_regularization:
            tf.add_to_collection(tf.GraphKeys.WEIGHTS, self.w_out)
            tf.add_to_collection(tf.GraphKeys.WEIGHTS, self.b_out)
            regularizer = tf.contrib.layers.l1_regularizer(scale=5.0 / 50000)
            reg_loss = tf.contrib.layers.apply_regularization(regularizer)
            net_loss = net_loss + reg_loss
        self.loss = tf.reduce_mean(net_loss)
        return self.loss

    def get_accuracy(self):
        self.predicts = tf.argmax(self.pred, axis=-1)
        self.actuals = tf.argmax(self.input_y, axis=-1)
        self.accuracy = tf.reduce_mean(tf.cast(tf.equal(self.predicts, self.actuals), dtype=tf.float32))

    def get_trainOp(self):
        self.train_op = tf.train.AdamOptimizer(self.lr).minimize(self.loss)
        return self.train_op

    def evaluate(self,sess,devdata):
        data_loader = TextLoader(devdata, self.batch_size)
        accuracies = []
        for i in range(data_loader.num_batches):
            x_train, y_train = data_loader.next_batch(i)
            x_input_ids = x_train[:, 0]
            x_input_mask = x_train[:, 1]
            x_segment_ids = x_train[:, 2]
            feed_dict = {self.input_ids: x_input_ids, self.input_mask: x_input_mask,
                         self.segment_ids: x_segment_ids,
                         self.input_y: y_train}
            accuracy = sess.run(self.accuracy, feed_dict=feed_dict)
            accuracies.append(accuracy)
        acc = np.mean(accuracies) * 100
        return acc


    def run_step(self,sess,x_train,y_train):
        x_input_ids = x_train[:, 0]
        x_input_mask = x_train[:, 1]
        x_segment_ids = x_train[:, 2]
        step, loss_, _ = sess.run([self.global_step, self.loss, self.train_op],
                                           feed_dict={self.input_ids: x_input_ids, self.input_mask: x_input_mask,
                                                      self.segment_ids: x_segment_ids,
                                                      self.input_y: y_train})
        return step,loss_

