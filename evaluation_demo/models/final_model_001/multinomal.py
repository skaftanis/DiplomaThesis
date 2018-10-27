import tflearn
import tensorflow as tf

from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d



def model_fc_2(output=1):


    network = input_data(shape=[None, 100, 250, 6])

    part_one = network[...,:3]
    part_two = network[...,3:]

    network1 = conv_2d(part_one, 24, 5, strides=5, activation='elu')
    network2 = conv_2d(part_two, 24, 5, strides=5, activation='elu')

    network = tflearn.merge([network1, network2], 'concat')


    #from basic network
    #network = conv_2d(network, 24, 5, strides=5, activation='elu' )
    network = conv_2d(network, 36, 5, strides=5, activation='elu' )
    network = conv_2d(network, 48, 5, strides=5, activation='elu' )
    network = conv_2d(network, 64, 3, strides=3, activation='elu' )
    network = conv_2d(network, 64, 3, strides=3, activation='elu' )

    network = dropout(network, 0.5)

    network = fully_connected(network, 100, activation='elu')
    network = fully_connected(network, 50, activation='elu')
    network = fully_connected(network, 10, activation='elu')
    network = fully_connected(network, output, activation='linear')


    #momentum =  tflearn.Momentum(learning_rate=0.00001, lr_decay=0.96, decay_step=1500)
    #network = tflearn.regression(network, optimizer=momentum, loss='huber_loss', metric=None)

    network = tflearn.regression(network, optimizer='adam',
                         loss='huber_loss', metric=None, learning_rate = 0.0001)

    model = tflearn.DNN(network, checkpoint_path='model_spirosnet',
                        max_checkpoints=1, tensorboard_verbose=2, tensorboard_dir='log')



    return model


def model_lstm(output=1):


    network = input_data(shape=[None, 100, 250, 6])

    part_one = network[...,:3]
    part_two = network[...,3:]

    network1 = conv_2d(part_one, 24, 5, strides=5, activation='elu')
    network2 = conv_2d(part_two, 24, 5, strides=5, activation='elu')

    network = tflearn.merge([network1, network2], 'concat')


    #from basic network
    #network = conv_2d(network, 24, 5, strides=5, activation='elu' )
    network = conv_2d(network, 36, 5, strides=5, activation='elu' )
    network = conv_2d(network, 48, 5, strides=5, activation='elu' )
    network = conv_2d(network, 64, 3, strides=3, activation='elu' )
    network = conv_2d(network, 64, 3, strides=3, activation='elu' )

    network = dropout(network, 0.5)

    network = fully_connected(network, 100, activation='elu')
    network = fully_connected(network, 50, activation='elu')
    network = fully_connected(network, 10, activation='elu')

    network = dropout(network,0.5)
    network = tflearn.reshape(network, [-1, 1, 10])
    network = tflearn.lstm(network,128, return_seq=True)
    network = tflearn.lstm(network,128)


    network = fully_connected(network, output, activation='linear')


    #momentum =  tflearn.Momentum(learning_rate=0.00001, lr_decay=0.96, decay_step=1500)
    #network = tflearn.regression(network, optimizer=momentum, loss='huber_loss', metric=None)

    network = tflearn.regression(network, optimizer='adam',
                         loss='huber_loss', metric=None, learning_rate = 0.0001)

    model = tflearn.DNN(network, checkpoint_path='model_spirosnet',
                        max_checkpoints=1, tensorboard_verbose=2, tensorboard_dir='log')



    return model

