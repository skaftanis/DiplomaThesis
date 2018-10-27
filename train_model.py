import numpy as np
from random import shuffle


from multinomal import model_fc_2


VERSION = 2
TRAINING_DATA_FILES = 8
WIDTH = 250
HEIGHT = 100
LR = 1e-3
EPOCHS = 30

MODEL_NAME = 'final_model_001-formula-1-car_v{}-{}-{}'.format(VERSION,LR,EPOCHS)

print("loading data...")

#CHANGE THIS IN EVERY PHASE
file_counter = 6300
model = model_fc_2(output=3)

for i in range(1,7):

    print(file_counter)

    print(str(i) + "/6")

    #load all data in RAM (~5GB)
    X = None
    Y = None
    X = np.load("X2_norm_final_data_{}.0.npy".format(i))
    Y = np.load("Y2_norm_final_data_{}.0.npy".format(i))

    #custom data shuffling
    combined = list(zip(X,Y))
    shuffle(combined)
    X[:], Y[:] = zip(*combined)

    #80% for train
    split_data_boundry = int(len(X) * 0.8)


    #LOAD previews trained model on the fly
    if i != 1:
        model.load("model_spirosnet-{}".format(file_counter))
        file_counter += 6300



    model.fit(X[:split_data_boundry],Y[:split_data_boundry], n_epoch=EPOCHS, validation_set=( X[split_data_boundry:], Y[split_data_boundry:]), 
	shuffle = False,snapshot_step=2500, show_metric=True, run_id=MODEL_NAME)

