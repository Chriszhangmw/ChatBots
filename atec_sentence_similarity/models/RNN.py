#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import tensorflow as tf
tfconfig = tf.ConfigProto()
tfconfig.gpu_options.allow_growth = True
session = tf.Session(config=tfconfig)


import sys
import keras
from keras.models import *
from keras.layers import *
from keras.optimizers import *
from keras.preprocessing import sequence
from keras.regularizers import l2
from keras import backend as K
from keras.engine.topology import Layer
from keras.backend.tensorflow_backend import set_session
import time
from keras.activations import softmax
from tensorflow.contrib import learn
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np
from keras import backend as K
sys.path.append('utils/')
import config
from help import *
sys.path.append('models/layers/')

from MyPooling import MyMeanPool,MyMaxPool
from MyEmbeding import create_pretrained_embedding
from Cross import cross

def my_rnn():
    emb_layer = create_pretrained_embedding(
        config.word_embed_weight, mask_zero=False)
    lstm_layer = Bidirectional(CuDNNLSTM(250, recurrent_dropout=0.2))

    sequence_1_input = Input(shape=(config.word_maxlen,), dtype="int32")
    embedded_sequences_1 = emb_layer(sequence_1_input)
    x1 = lstm_layer(embedded_sequences_1)

    sequence_2_input = Input(shape=(config.word_maxlen,), dtype="int32")
    embedded_sequences_2 = emb_layer(sequence_2_input)
    y1 = lstm_layer(embedded_sequences_2)

    magic_input = Input(shape=(len(config.feats),), dtype="float32")
    features_dense = BatchNormalization()(magic_input)
    features_dense = Dense(2, activation="relu")(features_dense)
    features_dense = Dropout(0.2)(features_dense)


    

    addition = add([x1, y1])
    minus_y1 = Lambda(lambda x: -x)(y1)
    merged = add([x1, minus_y1])
    merged = multiply([merged, merged])
    merged = concatenate([merged, addition])
    merged = Dropout(0.4)(merged)

    merged = concatenate([merged, features_dense])
    merged = BatchNormalization()(merged)
    merged = GaussianNoise(0.1)(merged)

    merged = Dense(300, activation="relu")(merged)
    merged = Dropout(0.2)(merged)
    merged = BatchNormalization()(merged)

    out = Dense(2, activation="sigmoid")(merged)

    model = Model(inputs=[sequence_1_input, sequence_2_input, magic_input], outputs=out)
    model.compile(loss="binary_crossentropy",
                  optimizer=Adam(), metrics=['acc'])
    model.summary()
    return model





def rnn_v1(lstm_hidden=50):

    pass




def bma_gru():

    # The embedding layer containing the word vectors
    # Embedding
    emb_layer = create_pretrained_embedding(
        config.char_embed_weights, mask_zero=True)
    emb_layer_word = create_pretrained_embedding(
        config.word_embed_weights, mask_zero=True)
    # Model variables

    n_hidden = 128

    # Define the shared model
    x = Sequential()
    x.add(emb_layer)
    # # LSTM
    x.add(Bidirectional(LSTM(n_hidden,return_sequences=True)))
    x.add(Bidirectional(LSTM(n_hidden,return_sequences=True)))
    x.add(BatchNormalization())
    x.add(MyMaxPool(axis=1))
    shared_model = x



    x2 = Sequential()
    x2.add(emb_layer_word)
    # # LSTM
    x2.add(Bidirectional(LSTM(10,return_sequences=True)))
    #x2.add(Bidirectional(LSTM(n_hidden,return_sequences=True)))
    x2.add(BatchNormalization())
    x2.add(MyMaxPool(axis=1))
    shared_model2 = x2
    # The visible layer
  
    magic_input = Input(shape=(len(config.feats),))
    magic_dense = BatchNormalization()(magic_input)
    magic_dense = Dense(64, activation='relu')(magic_dense)


    left_input = Input(shape=(config.word_maxlen,), dtype='int32')
    right_input = Input(shape=(config.word_maxlen,), dtype='int32')
    w1 = Input(shape=(config.word_maxlen,), dtype='int32')
    w2 = Input(shape=(config.word_maxlen,), dtype='int32')

 

    left = shared_model(left_input)
    right = shared_model(right_input)
   
    left_w = shared_model2(w1)
    right_w = shared_model2(w2)

    # Pack it all up into a Manhattan Distance model
    malstm_distance = Lambda(lambda x: K.exp(-K.sum(K.abs(x[0] - x[1]), axis=1, keepdims=True)), output_shape=(
        1,))([left, right])

    malstm_distance2 = Lambda(lambda x: K.exp(-K.sum(K.abs(x[0] - x[1]), axis=1, keepdims=True)), output_shape=(
        1,))([left_w, right_w])
        
    cro = cross(left, right,n_hidden*2)
    cro2 = cross(left_w, right_w,n_hidden*2)
    
    #if config.nofeats:
    merge = concatenate([ left,right,cro,malstm_distance2,magic_dense])  # , magic_dense, malstm_distance])
    # else:   
    #     merge = concatenate([ cro,cro2])
    # # The MLP that determines the outcome
    x = Dropout(0.2)(merge)
    x = BatchNormalization()(x)
    x = Dense(300, activation='relu')(x)
    
    x = Dropout(0.2)(x)
    x = BatchNormalization()(x)
    pred = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=[left_input, right_input,w1,w2,magic_input], outputs=pred)
    model.compile(loss='binary_crossentropy',
                  optimizer="adam", metrics = [Precision,Recall,F1,])
    model.summary()
    shared_model.summary()
    return model



def unchanged_shape(input_shape):
    "Function for Lambda layer"
    return input_shape


def substract(input_1, input_2):
    "Substract element-wise"
    neg_input_2 = Lambda(lambda x: -x, output_shape=unchanged_shape)(input_2)
    out_ = Add()([input_1, neg_input_2])
    return out_


def submult(input_1, input_2):
    "Get multiplication and subtraction then concatenate results"
    mult = Multiply()([input_1, input_2])
    sub = substract(input_1, input_2)
    out_ = Concatenate()([sub, mult])
    return out_


def apply_multiple(input_, layers):
    "Apply layers to input then concatenate result"
    if not len(layers) > 1:
        raise ValueError('Layers list should contain more than 1 layer')
    else:
        agg_ = []
        for layer in layers:
            agg_.append(layer(input_))
        out_ = Concatenate()(agg_)
    return out_


def time_distributed(input_, layers):
    "Apply a list of layers in TimeDistributed mode"
    out_ = []
    node_ = input_
    for layer_ in layers:
        node_ = TimeDistributed(layer_)(node_)
    out_ = node_
    return out_


def soft_attention_alignment(input_1, input_2):
    "Align text representation with neural soft attention"
    attention = Dot(axes=-1)([input_1, input_2])
    w_att_1 = Lambda(lambda x: softmax(x, axis=1),
                     output_shape=unchanged_shape)(attention)
    w_att_2 = Permute((2, 1))(Lambda(lambda x: softmax(x, axis=2),
                                     output_shape=unchanged_shape)(attention))
    in1_aligned = Dot(axes=1)([w_att_1, input_1])
    in2_aligned = Dot(axes=1)([w_att_2, input_2])
    return in1_aligned, in2_aligned



# def Siamese_LSTM():

#     # The embedding layer containing the word vectors
#     # Embedding
#     emb_layer = create_pretrained_embedding(
#         config.char_embed_weights, mask_zero=True)
#     emb_layer_word = create_pretrained_embedding(
#         config.word_embed_weights, mask_zero=True)
#     # Model variables

#     n_hidden = 128

#     # Define the shared model
#     x = Sequential()
#     x.add(emb_layer)
#     # # LSTM
#     x.add(Bidirectional(LSTM(n_hidden,return_sequences=True)))
#     x.add(Bidirectional(LSTM(n_hidden,return_sequences=True)))
#     x.add(BatchNormalization())
#     x.add(MyMaxPool(axis=1))
#     shared_model = x



#     x2 = Sequential()
#     x2.add(emb_layer_word)
#     # # LSTM
#     x2.add(Bidirectional(LSTM(10,return_sequences=True)))
#     #x2.add(Bidirectional(LSTM(n_hidden,return_sequences=True)))
#     x2.add(BatchNormalization())
#     x2.add(MyMaxPool(axis=1))
#     shared_model2 = x2
#     # The visible layer
  
#     magic_input = Input(shape=(len(config.feats),))
#     magic_dense = BatchNormalization()(magic_input)
#     magic_dense = Dense(64, activation='relu')(magic_dense)


#     left_input = Input(shape=(config.word_maxlen,), dtype='int32')
#     right_input = Input(shape=(config.word_maxlen,), dtype='int32')
#     w1 = Input(shape=(config.word_maxlen,), dtype='int32')
#     w2 = Input(shape=(config.word_maxlen,), dtype='int32')

 

#     left = shared_model(left_input)
#     right = shared_model(right_input)
   
#     left_w = shared_model2(w1)
#     right_w = shared_model2(w2)

#     # Pack it all up into a Manhattan Distance model
#     malstm_distance = Lambda(lambda x: K.exp(-K.sum(K.abs(x[0] - x[1]), axis=1, keepdims=True)), output_shape=(
#         1,))([left, right])

#     malstm_distance2 = Lambda(lambda x: K.exp(-K.sum(K.abs(x[0] - x[1]), axis=1, keepdims=True)), output_shape=(
#         1,))([left_w, right_w])
        
#     cro = cross(left, right,n_hidden*2)
#     cro2 = cross(left_w, right_w,n_hidden*2)
    
#     #if config.nofeats:
#     merge = concatenate([ left,right,cro,malstm_distance2,magic_dense])  # , magic_dense, malstm_distance])
#     # else:   
#     #     merge = concatenate([ cro,cro2])
#     # # The MLP that determines the outcome
#     x = Dropout(0.2)(merge)
#     x = BatchNormalization()(x)
#     x = Dense(300, activation='relu')(x)
    
#     x = Dropout(0.2)(x)
#     x = BatchNormalization()(x)
#     pred = Dense(1, activation='sigmoid')(x)
#     model = Model(inputs=[left_input, right_input,w1,w2,magic_input], outputs=pred)
#     model.compile(loss='binary_crossentropy',
#                   optimizer="adam", metrics = [Precision,Recall,F1,])
#     model.summary()
#     shared_model.summary()
#     return model



def Siamese_LSTM():

    # The embedding layer containing the word vectors
    # Embedding
    emb_layer = create_pretrained_embedding(
        config.char_embed_weights, mask_zero=True)
    emb_layer_word = create_pretrained_embedding(
        config.word_embed_weights, mask_zero=True)
    # Model variables

    n_hidden = 128

    # Define the shared model
    x = Sequential()
    x.add(emb_layer)
    # # LSTM
    x.add(Bidirectional(LSTM(n_hidden,return_sequences=True)))
    x.add(Bidirectional(LSTM(n_hidden,return_sequences=True)))
    x.add(BatchNormalization())
    #x.add(MyMaxPool(axis=1))
    shared_model = x



    x2 = Sequential()
    x2.add(emb_layer_word)
    # # LSTM
    x2.add(Bidirectional(LSTM(10,return_sequences=True)))
    #x2.add(Bidirectional(LSTM(n_hidden,return_sequences=True)))
    x2.add(BatchNormalization())
    x2.add(MyMaxPool(axis=1))
    shared_model2 = x2
    # The visible layer
  
    magic_input = Input(shape=(len(config.feats),))
    magic_dense = BatchNormalization()(magic_input)
    magic_dense = Dense(64, activation='relu')(magic_dense)


    left_input = Input(shape=(config.word_maxlen,), dtype='int32')
    right_input = Input(shape=(config.word_maxlen,), dtype='int32')
    w1 = Input(shape=(config.word_maxlen,), dtype='int32')
    w2 = Input(shape=(config.word_maxlen,), dtype='int32')

 

    left = shared_model(left_input)
    right = shared_model(right_input)
   


     # Attention
    q1_aligned, q2_aligned = soft_attention_alignment(left, right)

    # Compose
    q1_combined =submult(left, q2_aligned)
    q2_combined = submult(right, q1_aligned)

    # compose = Bidirectional(LSTM(300, return_sequences=True))
    # q1_compare = compose(q1_combined)
    # q2_compare = compose(q2_combined)

    # Aggregate
    left = apply_multiple(q1_combined, [MyMeanPool(axis=1), MyMaxPool(axis=1)])
    right = apply_multiple(q2_combined, [MyMeanPool(axis=1), MyMaxPool(axis=1)])

    left_w = shared_model2(w1)
    right_w = shared_model2(w2)

    # Pack it all up into a Manhattan Distance model
    malstm_distance = Lambda(lambda x: K.exp(-K.sum(K.abs(x[0] - x[1]), axis=1, keepdims=True)), output_shape=(
        1,))([left, right])

    malstm_distance2 = Lambda(lambda x: K.exp(-K.sum(K.abs(x[0] - x[1]), axis=1, keepdims=True)), output_shape=(
        1,))([left_w, right_w])
        
    cro = cross(left, right,n_hidden*2)
    cro2 = cross(left_w, right_w,n_hidden*2)
    
    #if config.nofeats:
    merge = concatenate([ left,right,malstm_distance2,magic_dense])  # , magic_dense, malstm_distance])
    # else:   
    #     merge = concatenate([ cro,cro2])
    # # The MLP that determines the outcome
    x = Dropout(0.2)(merge)
    x = BatchNormalization()(x)
    x = Dense(300, activation='relu')(x)
    
    x = Dropout(0.2)(x)
    x = BatchNormalization()(x)
    pred = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=[left_input, right_input,w1,w2,magic_input], outputs=pred)
    model.compile(loss='binary_crossentropy',
                  optimizer="adam", metrics = [Precision,Recall,F1,])
    model.summary()
    shared_model.summary()
    return model

