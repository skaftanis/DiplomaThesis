import numpy as np
import math

for counter in range(10,70,10):

    counter = 76

    print(str(counter))
    print("loading data...")

    #load all data in RAM (~5GB)
    TRAINING_DATA_FILES = counter
    data = np.load("data/telemetry_training_data-{}.npy".format(counter-6))

    #data = np.load("normalized_data-1.npy")

    for i in range(counter-5,TRAINING_DATA_FILES + 1 ):
        data = np.append(data,np.load('data/telemetry_training_data-{}.npy'.format(i)), axis=0 )

    data_len = len(data)

    #keep only the interesting part (ROI)
    for i in range(data_len):
        data[i][0] = data[i][0][:100]

    #pre calculated means and stds for the whole dataset

    sum1 = 91461941044.18457 
    std_sum1 = 1875687355110.2168

    sum2 = 123215856697.59067
    std_sum2 = 113146464589.96437

    sum3 = 117359336885.57675
    std_sum3 = 128011048786.3762

    x_sum = 2030407.3156801462
    x_std_sum = 4384368263.496551

    speed_sum = 2087542.642747879
    speed_std_sum = 10022033.821311038

    y_sum = -586132.7977940273
    y_std_sum = 12510483.537866063

    dataset_data_len = 38000

    mean1 = sum1 / (dataset_data_len*100*250)
    std_1 = math.sqrt(std_sum1/(dataset_data_len*100*250))

    mean2 = sum2 / (dataset_data_len*100*250)
    std_2 = math.sqrt(std_sum2/(dataset_data_len*100*250))

    mean3 = sum3 / (dataset_data_len*100*250)
    std_3 = math.sqrt(std_sum3/(dataset_data_len*100*250))

    speed_mean = speed_sum / dataset_data_len
    speed_std = math.sqrt(speed_std_sum/dataset_data_len)

    x_mean = x_sum / dataset_data_len
    x_std = math.sqrt(x_std_sum/dataset_data_len)

    y_mean = y_sum / dataset_data_len
    y_std = math.sqrt(y_std_sum/dataset_data_len)

    #normalize images
    for i in range(data_len):
      data[i][0] = np.array(data[i][0], dtype='float32')

      data[i][0][...,0] = ( data[i][0][...,0] - mean1 ) / std_1
      data[i][0][...,1] = ( data[i][0][...,1] - mean2 ) / std_2
      data[i][0][...,2] = ( data[i][0][...,2] - mean3 ) / std_3

      data[i][1]['speed'] = ( data[i][1]['speed'] - speed_mean ) / speed_std
      data[i][1]['x'] = ( data[i][1]['x'] - x_mean ) / x_std
      data[i][1]['y'] = ( data[i][1]['y'] - y_mean ) / y_std


    HEIGHT = 100
    WIDTH = 250

    X = []

    for i in range(data_len):
        if (i%200 == 0):
            print(str(i) + " \ " + str(data_len))
        cur_x = data[i][1]['x']
        cur_y = data[i][1]['y']
        cur_speed = data[i][1]['speed']
        x_channel = np.zeros( (HEIGHT,WIDTH)  )
        y_channel = np.zeros( (HEIGHT,WIDTH)  )
        speed_channel = np.zeros( (HEIGHT,WIDTH)  )
        for h in range(HEIGHT):
            for w in range(WIDTH):
                x_channel[h][w] = cur_x
                y_channel[h][w] = cur_y
                speed_channel[h][w] = cur_speed
        temp = np.concatenate( (  data[i][0], np.expand_dims(x_channel,axis=2) ), axis=2 )
        temp = np.concatenate( (temp, np.expand_dims(y_channel,axis=2)), axis=2 )
        temp = np.concatenate( (temp, np.expand_dims(speed_channel,axis=2)), axis=2 )
        X.append(temp)




    print("converting X to numpy array")

    X = np.array(X)


    Y = []

    for i in range(data_len):
        curreny_Y = []
        curreny_Y = np.array(curreny_Y)
        for key,value in sorted(data[i][2].items()):
            curreny_Y = np.append(curreny_Y, value)
        Y.append(np.array(curreny_Y))

    Y = np.array(Y, dtype='float32')

    #keep only the sterring for this model (for now)

    #new_Y = []

    #for i in range(len(Y)):
    #    new_Y.append(Y[i][1])

    #new_Y = np.array(new_Y)

    #YY = []

    #for i in range(len(new_Y)):
    #    temp = []
    #    temp.a ppend(new_Y[i])
    #    temp = np.array(temp)
    #    YY.append(temp)

    #YY = np.array(YY)

    np.save("X2_norm_final_data_{}.npy".format(counter+4/10), X)
    np.save("Y2_norm_final_data_{}.npy".format(counter+4/10), Y)

    data = {}

    break
