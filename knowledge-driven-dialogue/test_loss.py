#
# import keras
# import matplotlib as plt
# import keras
# from keras.datasets import mnist
# from keras.models import Sequential
# from keras.layers.core import Dense, Dropout, Activation
# from keras.optimizers import SGD, Adam, RMSprop
# from keras.utils import np_utils
# import matplotlib.pyplot as plt
# class LossHistory(keras.callbacks.Callback):
#     def on_train_begin(self, logs={}):
#         self.losses = {'batch': [], 'epoch': []}
#         self.accuracy = {'batch': [], 'epoch': []}
#         self.val_loss = {'batch': [], 'epoch': []}
#         self.val_acc = {'batch': [], 'epoch': []}
#
#     def on_batch_end(self, batch, logs={}):
#         self.losses['batch'].append(logs.get('loss'))
#         self.accuracy['batch'].append(logs.get('acc'))
#         self.val_loss['batch'].append(logs.get('val_loss'))
#         self.val_acc['batch'].append(logs.get('val_acc'))
#
#     def on_epoch_end(self, batch, logs={}):
#         self.losses['epoch'].append(logs.get('loss'))
#         self.accuracy['epoch'].append(logs.get('acc'))
#         self.val_loss['epoch'].append(logs.get('val_loss'))
#         self.val_acc['epoch'].append(logs.get('val_acc'))
#
#     def loss_plot(self, loss_type):
#         iters = range(len(self.losses[loss_type]))
#         #创建一个图
#         plt.figure()
#         # acc
#         plt.plot(iters, self.accuracy[loss_type], 'r', label='train acc')#plt.plot(x,y)，这个将数据画成曲线
#         # loss
#         plt.plot(iters, self.losses[loss_type], 'g', label='train loss')
#         if loss_type == 'epoch':
#             # val_acc
#             plt.plot(iters, self.val_acc[loss_type], 'b', label='val acc')
#             # val_loss
#             plt.plot(iters, self.val_loss[loss_type], 'k', label='val loss')
#         plt.grid(True)#设置网格形式
#         plt.xlabel(loss_type)
#         plt.ylabel('acc-loss')#给x，y轴加注释
#         plt.legend(loc="upper right")#设置图例显示位置
#         plt.show()
#
# #创建一个实例LossHistory
# history = LossHistory()
#
# batch_size = 128
# nb_classes = 10
# nb_epoch = 5
# (X_train, y_train), (X_test, y_test) = mnist.load_data()
# X_train = X_train.reshape(60000, 784)
# X_test = X_test.reshape(10000, 784)
# X_train = X_train.astype('float32')
# X_test = X_test.astype('float32')
# X_train /= 255
# X_test /= 255
# print(X_train.shape[0], 'train samples')
# print(X_test.shape[0], 'test samples')
# Y_train = np_utils.to_categorical(y_train, nb_classes)
# Y_test = np_utils.to_categorical(y_test, nb_classes)
#
# model = Sequential()
# model.add(Dense(512, input_shape=(784,)))
# model.add(Activation('relu'))
# model.add(Dropout(0.2))
# model.add(Dense(512))
# model.add(Activation('relu'))
# model.add(Dropout(0.2))
# model.add(Dense(10))
# model.add(Activation('softmax'))
#
# model.compile(loss='categorical_crossentropy',
#               optimizer=RMSprop(),
#               metrics=['accuracy'])
# #创建一个实例LossHistory
# history = LossHistory()
# model.fit(X_train, Y_train,
#             batch_size=batch_size, nb_epoch=nb_epoch,
#             verbose=1,
#             validation_data=(X_test, Y_test),
#             callbacks=[history])#callbacks回调，将数据传给history
# #模型评估
# score = model.evaluate(X_test, Y_test, verbose=0)
# print('Test score:', score[0])
# print('Test accuracy:', score[1])
# #绘制acc-loss曲线
# history.loss_plot('epoch')
#
#
#
#
#
#
#
#
#
#
#
# import numpy as np
#
# plot_x = np.linspace(-1, 6, 141)
# plot_y = (plot_x - 2.5) ** 2 - 1
#
#
#
#
#
#
#
#
#
#
#









import numpy as np
import pandas as pd   # pandas 是基于NumPy 的一种工具，该工具是为了解决数据分析任务而创建的
import matplotlib.pyplot as plt


# 计算代价函数
# X:输入变量 y：输出变量 theta：预测函数的两个系数值（h(x)=theta(1)+theta(2)*x）
def compute_cost(X,y,theta):
    m=len(X)
    inner=np.power(((X.dot(theta.T))-y),2)
    # inner1 = np.power(((X.dot(theta.T))-y),4)*10
    inner1 = abs((X.dot(theta.T))-y)

    lossa = sum(inner)/(2*m)
    lossb = sum(inner1)/(2*m)
    loss1 = lossa + lossb*10
    loss2 = lossa + lossb
    return loss1,lossa,lossb

# 梯度下降算法
# alpha：学习率 epoch：迭代次数
def gradientDescent(X, y, theta, alpha, epoch=1000):
    temp = np.array(np.zeros(theta.shape))
    parameters = int(theta.flatten().shape[0])  # 参数theta的数量
    cost = np.zeros(epoch)  # 初始化一个ndarray，包含每次迭代后的cost
    cost1 = np.zeros(epoch)
    m = X.shape[0]  # 样本数量

    # 利用向量化同步计算theta的值
    for i in range(epoch):
        temp = theta - (alpha / m) * (X.dot(theta.T) - y).T.dot(X)  # 得出一个theta行向量
        theta = temp
        loss1,lossa,lossb= compute_cost(X, y, theta)
        cost[i]  = loss1
        cost1[i] = lossa
    return theta, cost,cost1

if __name__=='__main__':
    path = './data.txt'
    # names添加列名，header用指定的行来作为标题，若原来无标题则设为none
    data = pd.read_csv(path, names=['Population', 'Profit'])

    # 在训练集中插入一列1，方便计算
    data.insert(0, 'Ones', 1)
    # 设置训练集X和目标变量y的值
    cols = data.shape[1]
    X = data.iloc[:, 0:cols - 1]  # 输入变量X为前cols-1列
    y = data.iloc[:, cols - 1:cols]  # 输出变量y为最后一列
    X = np.array(X.values)
    y = np.array(y.values)
    theta = np.array([0, 0]).reshape(1, 2)

    alpha = 0.01
    epoch = 5000

    final_theta, cost,cost1 = gradientDescent(X, y, theta, alpha, epoch)
    print('loss1 is final value is :',cost[-1],'the proportion begin/end:',cost[0]/cost[-1])
    print('loss2 is final value is :',cost1[-1],'the proportion begin/end:',cost1[0]/cost1[-1])

    population = np.linspace(data.Population.min(), data.Population.max(), 100)
    profit = final_theta[0, 0] + (final_theta[0, 1] * population)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(population, profit, 'r', label='Prediction')
    ax.scatter(data['Population'], data['Profit'], label='Training data')
    ax.legend(loc=4)
    ax.set_xlabel('Population')
    ax.set_ylabel('Profit')
    ax.set_title('Predicting Profit by Population Size')
    plt.show()

    fig, ax = plt.subplots(figsize=(8, 6))
    plt.ylim(0, 200.0)
    x = np.arange(epoch)
    y1 = cost
    y2 = cost1
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.xlabel("Number Epochs")
    plt.ylabel("Loss Function")
    plt.legend(['loss1','loss2'], loc='upper left')
    plt.show()




    # fig, ax = plt.subplots(figsize=(8, 6))
    #
    #
    # ax.plot(np.arange(epoch), cost, 'r')
    # ax.set_xlabel('Iteration')
    # ax.set_ylabel('Cost1')
    # ax.set_title('Error vs. Traning Epoch')
    # plt.show()
    #
    # fig, ax = plt.subplots(figsize=(8, 6))
    # ax.plot(np.arange(epoch), cost1, 'r')
    # ax.set_xlabel('Iteration')
    # ax.set_ylabel('Cost2')
    # ax.set_title('Error vs. Traning Epoch')
    # plt.show()







axes = plt.gca()
plt.gca().set_color_cycle(['red', 'green', 'blue', 'yellow'])
# plt.ylim(1.1, 1.3)
axes.set_ylim([1.1,1.3])
x = np.array([10,50,100,500,700,1000])
y1 = np.array([1.2189,1.15602,1.1454,1.1362,1.1356,1.1351])
y2 = np.array([1.27045,1.2042,1.19311,1.18353,1.18282,1.18229])
y3 = np.array([1.2882,1.223,1.212,1.2026,1.2019,1.2014])
y4 = np.array([1.291,1.2265,1.2156,1.2062,1.2055,1.205])
plt.plot(x, y1,marker='o', mec='r', mfc='w',label=u'epochs = 500')
plt.plot(x, y2,marker='*', mec='r', mfc='w',label=u'epochs = 1000')
plt.plot(x, y3,marker="v", mec='r', mfc='w',label=u'epochs = 2000')
plt.plot(x, y4,marker='h', mec='r', mfc='w',label=u'epochs = 5000')
plt.xlabel("K value")
plt.ylabel("Degree of Convergence ")
plt.legend([' epochs = 500', 'epochs = 1000', 'epochs = 2000', 'epochs = 5000'], loc='upper left')
plt.show()





