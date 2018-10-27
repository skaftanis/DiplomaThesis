import numpy as np 
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif



TRAINING_DATA_FILES = 20



#load all data in RAM (~5GB)
data = np.load("data/telemetry_training_data-1.npy")


for i in range(2,TRAINING_DATA_FILES + 1 ):
    data = np.append(data,np.load('data/telemetry_training_data-{}.npy'.format(i)), axis=0 )


data_len = len(data)



#remove unnecessary features - preprocessing (34 features remaining)
for i in range(data_len):
    data[i][1].pop('throttle', None)
    data[i][1].pop('steer', None)
    data[i][1].pop('brake', None)
    #34^
    data[i][1].pop('svRL', None)
    data[i][1].pop('svRR', None)
    data[i][1].pop('svFL', None)
    data[i][1].pop('svFR', None)
    #30^
    data[i][1].pop('yaw', None)
    data[i][1].pop('pitch', None)
    data[i][1].pop('roll', None)
    #27^
    data[i][1].pop('xlv', None)
    data[i][1].pop('ylv', None)
    data[i][1].pop('zlv', None)
    data[i][1].pop('aax', None)
    data[i][1].pop('aay', None)
    data[i][1].pop('aaz', None)
    #21^
    data[i][1].pop('wsRL', None)
    data[i][1].pop('wsRR', None)
    data[i][1].pop('wsFL', None)
    data[i][1].pop('wsFR', None)
    #17^
    data[i][1].pop('xv', None)
    data[i][1].pop('yv', None)
    data[i][1].pop('zv', None)
    data[i][1].pop('xr', None)
    data[i][1].pop('yr', None)
    data[i][1].pop('zr', None)
    data[i][1].pop('xd', None)
    data[i][1].pop('yd', None)
    data[i][1].pop('zd', None)
    #8^
    

X = []


for i in range(data_len):
    current_X = []
    current_X = np.array(current_X)
    for key, value in sorted(data[i][1].items()):
        current_X = np.append(current_X, value)
    X.append(np.array(current_X))

X = np.array(X, dtype='float32')


Y = []

for i in range(data_len):
    curreny_Y = []
    curreny_Y = np.array(curreny_Y)
    for key,value in sorted(data[i][2].items()):
        curreny_Y = np.append(curreny_Y, value)
    Y.append(np.array(curreny_Y))

Y = np.array(Y, dtype='float32')

data = {}


sel = SelectKBest(f_classif, 5)
y= Y[:,1] #check for steeering
sel.fit(X,y)