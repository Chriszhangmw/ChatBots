

import  numpy as np
import os
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants



model_path = ''
tensorflow_model_dir = ''


class Model:
    def __init__(self,data):
        self.data = data

    def get_tensor_name(self,name):
        return name + ":0"

    def predict(self,one_data):
        '''
        使用模型
        :param data:模型的输入参数
        :return:
        '''
        with tf.Session() as session:
            tf.saved_model.loader.load(session,[tag_constants.SERVING],os.path.join(model_path,tensorflow_model_dir))
            input_ids = session.graph.get_tensor_by_name(self.get_tensor_name('input_ids'))
            input_mask = session.graph.get_tensor_by_name(self.get_tensor_name('input_masks'))
            segment_ids = session.graph.get_tensor_by_name(self.get_tensor_name('segment_ids'))
            pre_results = session.graph.get_tensor_by_name(self.get_tensor_name('pre'))
            x_input_ids, x_input_mask, x_segment_ids = self.one_single_data_process(one_data)
            predict = session.run(pre_results, feed_dict={input_ids: x_input_ids, input_mask: x_input_mask,
                                                  segment_ids: x_segment_ids})
            return self.resluts_to_categorys(predict)

    def resluts_to_categorys(self,result):
        if result > 0.5:
            return 1
        else:
            return 0

    def predict_all(self,datas):
        with tf.Session() as session:
            tf.saved_model.loader.load(session, [tag_constants.SERVING], os.path.join(model_path, tensorflow_model_dir))
            input_ids = session.graph.get_tensor_by_name(self.get_tensor_name('input_ids'))
            input_mask = session.graph.get_tensor_by_name(self.get_tensor_name('input_masks'))
            segment_ids = session.graph.get_tensor_by_name(self.get_tensor_name('segment_ids'))
            pre_results = session.graph.get_tensor_by_name(self.get_tensor_name('pre'))
            ratings = []
            for data in datas:
                x_input_ids, x_input_mask, x_segment_ids = self.one_single_data_process(self.data)
                predict = session.run(pre_results, feed_dict={input_ids: x_input_ids, input_mask: x_input_mask,
                                                      segment_ids: x_segment_ids})
                predict = self.resluts_to_categorys(predict)
                ratings.append(predict)
        return ratings

    def save_model(self,session,path,name=tensorflow_model_dir,overwrite = False):
        if overwrite:
            self.delete_file(path)

        builder = tf.saved_model.builder.SavedModelBuilder(os.path.join(path,name))
        builder.add_meta_graph_and_variables(session,[tf.saved_model.tag_constants.SERVING])
        builder.save()

    def delete_file(self,path):
        for root,dirs,files in os.walk(path,topdown=False):
            for name in files:
                os.remove(os.path.join(root,name))
            for name in dirs:
                os.rmdir(os.path.join(root,name))























