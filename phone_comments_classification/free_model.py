


import tensorflow as tf
from tensorflow.python.framework.graph_util import convert_variables_to_constants



def freeze_graph():
    # model_path = model_path
    base_dir='./model/'
    tf.reset_default_graph()
    checkpoint_path = tf.train.latest_checkpoint(base_dir)
    saver = tf.train.import_meta_graph(checkpoint_path + '.meta', import_scope=None)
    output_node_names = 'y'
    with tf.Session() as sess:
        # Restore the variable values
        saver.restore(sess, checkpoint_path)
        # Get the graph def from our current graph
        graph_def = tf.get_default_graph().as_graph_def()
        # Turn all variables into constants
        frozen_graph_def = convert_variables_to_constants(sess, graph_def, output_node_names.split(','))
        # Save our new graph def
        with tf.gfile.GFile('./model/simi_frozen.pb', 'wb') as f:
            f.write(frozen_graph_def.SerializeToString())

if __name__ == '__main__':
    freeze_graph()