import collections
import os
from bert import modeling
from bert import optimization
from bert import tokenization
import tensorflow as tf
from sklearn.metrics import f1_score,precision_score,recall_score
from tensorflow.python.ops import math_ops
# import tf_metrics
import pickle

class Ner_Model():
    def __init__(self,bert_root,data_path,model_save_path,batch_size,max_len,lr,keep_prob):
        self.bert_root = bert_root
        self.data_path = data_path
        self.model_save_path = model_save_path
        self.batch_size = batch_size
        self.max_len = max_len
        self.lr = lr
        self.keep_prob = keep_prob

        self.bert_config()
        # self.get_accuracy()
        self.get_trainOp()


    def bert_config(self):
        bert_config_file = os.path.join(self.bert_root, 'bert_config.json')
        self.bert_config = modeling.BertConfig.from_json_file(bert_config_file)
        self.init_checkpoint = os.path.join(self.bert_root, 'bert_model.ckpt')
        self.bert_vocab_file = os.path.join(self.bert_root, 'vocab.txt')

        self.input_ids = tf.placeholder(tf.int32, shape=[None, None], name='input_ids')
        self.input_mask = tf.placeholder(tf.int32, shape=[None, None], name='input_masks')
        self.segment_ids = tf.placeholder(tf.int32, shape=[None, None], name='segment_ids')
        self.input_y = tf.placeholder(tf.int32, shape=[None,None], name="input_y")

        self.global_step = tf.Variable(0, trainable=False)

        model = modeling.BertModel(
            config=self.bert_config,
            is_training=False,
            input_ids=self.input_ids,
            input_mask=self.input_mask,
            token_type_ids=self.segment_ids,
            use_one_hot_embeddings=False)
        tvars = tf.trainable_variables()
        (assignment, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars,
                                                                                               self.init_checkpoint)
        tf.train.init_from_checkpoint(self.init_checkpoint, assignment)
        sequence_output = model.get_sequence_output()
        hidden_size = sequence_output.shape[-1].value
        sequence_output = tf.nn.dropout(sequence_output, keep_prob=self.keep_prob)

        output_weights = tf.get_variable(
            "output_weights", [11, hidden_size],
            initializer=tf.random_normal_initializer(stddev=0.1))
        output_bias = tf.get_variable(
            "output_bias", [11], initializer=tf.random_normal_initializer(stddev=0.01))
        self.w_out = output_weights
        self.b_out = output_bias

        sequence_output = tf.reshape(sequence_output, [-1, hidden_size])
        logits = tf.matmul(sequence_output, self.w_out, transpose_b=True)
        self.logits = tf.nn.bias_add(logits, self.b_out)
        logits = tf.reshape(self.logits, [-1, self.max_len, 11])

        log_probs = tf.nn.log_softmax(logits, axis=-1)
        one_hot_labels = tf.one_hot(self.input_y, depth=11, dtype=tf.float32)
        per_example_loss = -tf.reduce_sum(one_hot_labels * log_probs, axis=-1)
        loss = tf.reduce_sum(per_example_loss)
        self.loss = tf.reduce_mean(loss)
        tf.summary.scalar('loss', self.loss)
        self.merged = tf.summary.merge_all()
        self.probabilities = tf.nn.softmax(logits, axis=-1,name='y')

    def get_trainOp(self):
        self.train_op = tf.train.AdamOptimizer(self.lr).minimize(self.loss)
        return self.train_op

    # def metric_fn(self, label_ids, probabilities):
    #     predictions = tf.argmax(probabilities, axis=-1, output_type=tf.int32)
    #     precision = tf_metrics.precision(label_ids, predictions, 11, [2, 3, 4, 5, 6, 7], average="macro")
    #     #tf_metrics API目前只支持二分类，所以这里第二个参数矩阵是将识别出来的命名体作为一个类，剩下的作为第二个类
    #     recall = tf_metrics.recall(label_ids, predictions, 11, [2, 3, 4, 5, 6, 7], average="macro")
    #     f = tf_metrics.f1(label_ids, predictions, 11, [2, 3, 4, 5, 6, 7], average="macro")
    #     return {
    #         "eval_precision": precision,
    #         "eval_recall": recall,
    #         "eval_f": f,
    #     }

    def run_step(self,sess,x_train,y_train):
        x_input_ids = x_train[:, 0]
        x_input_mask = x_train[:, 1]
        x_segment_ids = x_train[:, 2]
        step, loss_,_,log= sess.run([self.global_step, self.loss, self.train_op,self.merged],
                                           feed_dict={self.input_ids: x_input_ids, self.input_mask: x_input_mask,
                                                      self.segment_ids: x_segment_ids,
                                                      self.input_y: y_train})
        return step,loss_,log
