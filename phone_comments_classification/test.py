import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
# number 1 to 10 data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)




batch_xs, batch_ys = mnist.train.next_batch(4)
print(batch_ys)




