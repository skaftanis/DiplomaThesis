import numpy as np
from random import randint


#TRAINING_DATA_FILES = 76

TRAINING_DATA_FILES = 38

#load all data in RAM (~5GB)
#data = np.load("data/telemetry_training_data-1.npy")
data = np.load("6990_data/6990_telemetry_training_data-1.npy")


for i in range(2,TRAINING_DATA_FILES + 1 ):
     data = np.append(data, np.load('6990_data/6990_telemetry_training_data-{}.npy'.format(i)), axis=0)
     #data = np.append(data,np.load('data/telemetry_training_data-{}.npy'.format(i)), axis=0 )


data_len = len(data)


class1 = 0
class2 = 0
class3 = 0
class4 = 0
class5 = 0


for i in range(data_len):
    if float(data[i][2]['steering']) >= -1 and float(data[i][2]['steering']) < -0.3:
        class1 = class1 + 1
    elif float(data[i][2]['steering']) >= -0.3 and float(data[i][2]['steering']) < -0.1:
        class2 = class2 + 1
    elif float(data[i][2]['steering']) >=-0.1 and float(data[i][2]['steering']) <0.1:
        class3 = class3 + 1
    elif float(data[i][2]['steering']) >= 0.1 and float(data[i][2]['steering']) <0.3:
        class4 = class4 + 1
    elif float(data[i][2]['steering']) >= 0.3 and float(data[i][2]['steering']) <=1:
        class5 = class5 + 1



#find random data from class1
found = 0
need = abs(4000 - class1)
while found < need:
    rand_num = randint(0,data_len-1)
    if float(data[rand_num][2]['steering']) >= -1 and float(data[rand_num][2]['steering']) < -0.3:
        found = found + 1
        data = np.vstack([data, data[rand_num]])



found = 0
need = abs(10000 - class2)
while found < need:
    rand_num = randint(0,len(data)-1)
    if float(data[rand_num][2]['steering']) >= -0.3 and float(data[rand_num][2]['steering']) < -0.1:
        found = found + 1
        data = np.vstack([data, data[rand_num]])


#here we delete
found = 0
need = abs(13000 - class3)
while found < need:
    rand_num = randint(0,len(data)-1)
    if float(data[rand_num][2]['steering']) >= -0.1  and float(data[rand_num][2]['steering']) < 0.1:
        found = found + 1
        data = np.delete(data, (rand_num), axis=0)


found = 0
need = abs(10000 - class4)
while found < need:
    rand_num = randint(0,len(data)-1)
    if float(data[rand_num][2]['steering']) >= 0.1 and float(data[rand_num][2]['steering']) < 0.3:
        found = found + 1
        data = np.vstack([data, data[rand_num]])

found = 0
need = 4000 - class5
while found < need:
    rand_num = randint(0, len(data) -1)
    if float(data[rand_num][2]['steering']) >= 0.3 and float(data[rand_num][2]['steering']) <= 1:
        found = found + 1
        data = np.vstack([data, data[rand_num]])



#np.save("balanced_data.npy", data)
#file saving on ipython3 in parts because of memory problems
