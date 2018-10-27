#this script calculates the means and the stds of the input features

import numpy as np
import cv2
import math

# def RGB2YUV( rgb ):

#     m = np.array([[ 0.29900, -0.16874,  0.50000],
#                  [0.58700, -0.33126, -0.41869],
#                  [ 0.11400, 0.50000, -0.08131]])

#     yuv = np.dot(rgb,m)
#     yuv[:,:,1:]+=128.0
#     return yuv

#find the mean of the dataset for every channel
print("loading files")
data = np.load("data/telemetry_training_data-61.npy")
TRAINING_DATA_FILES = 76

for i in range(62,TRAINING_DATA_FILES + 1 ):
    data = np.append(data,np.load('data/telemetry_training_data-{}.npy'.format(i)), axis=0 )

data_len = len(data)



for i in range(data_len):
    data[i][0] = data[i][0][:100]

print("YUV")
#convert images to YUV
m = np.array([[ 0.29900, -0.16874,  0.50000],
             [0.58700, -0.33126, -0.41869],
             [ 0.11400, 0.50000, -0.08131]])

for i in range(data_len):

    data[i][0] = np.dot(data[i][0],m)
    data[i][0][:,:,1:]+=128.0


#standarize images
# for i in range(data_len):
# 	data[i][0] = ( data[i][0] - np.min(data[i][0]) ) / (np.max(data[i][0]) - np.min(data[i][0]))


#100x250x3

print("channel 1...")

sum1 = 0 
for i in range(data_len):
	for h in range(100):
		for w in range(250):
			sum1 = sum1 + data[i][0][h][w][0] 
	
mean1 = sum1 / (data_len*100*250)

std_sum1 = 0 
for i in range(data_len):
	for h in range(100):
		for w in range(250):
			std_sum1 = std_sum1 + (data[i][0][h][w][0] - mean1)**2

std_1 = math.sqrt(std_sum1/(data_len*100*250))

#########
print("channel 2...")

sum2 = 0 
for i in range(data_len):
	for h in range(100):
		for w in range(250):
			sum2 = sum2 + data[i][0][h][w][1] 
	
mean2 = sum2 / (data_len*100*250)

std_sum2 = 0 
for i in range(data_len):
	for h in range(100):
		for w in range(250):
			std_sum2 = std_sum2 + (data[i][0][h][w][1] - mean2)**2

std_2 = math.sqrt(std_sum2/(data_len*100*250))

#########
print("channel 3...")


sum3 = 0 
for i in range(data_len):
	for h in range(100):
		for w in range(250):
			sum3 = sum3 + data[i][0][h][w][2] 
	
mean3 = sum3 / (data_len*100*250)


std_sum3 = 0 
for i in range(data_len):
	for h in range(100):
		for w in range(250):
			std_sum3 = std_sum3 + (data[i][0][h][w][2] - mean3)**2

std_3 = math.sqrt(std_sum3/(data_len*100*250))

#########

#normalize images
# for i in range(data_len):
# 	data[i][0][...,0] = ( data[i][0][...,0] - mean1 ) / std_1
# 	data[i][0][...,1] = ( data[i][0][...,1] - mean2 ) / std_2
# 	data[i][0][...,2] = ( data[i][0][...,2] - mean3 ) / std_3

print("features norm...")


speed_sum = 0
for i in range(data_len):
	speed_sum += data[i][1]['speed']

speed_mean = speed_sum / data_len


speed_std_sum = 0 
for i in range(data_len):
	speed_std_sum =  speed_std_sum + ( data[i][1]['speed'] - speed_mean)**2

speed_std = math.sqrt(speed_std_sum/data_len)

#########

x_sum = 0
for i in range(data_len):
	x_sum += data[i][1]['x']

x_mean = x_sum / data_len

x_std_sum = 0 
for i in range(data_len):
	x_std_sum =  x_std_sum + ( data[i][1]['x'] - x_mean)**2

x_std = math.sqrt(x_std_sum/data_len)

#########

y_sum = 0
for i in range(data_len):
	y_sum += data[i][1]['y']

y_mean = y_sum / data_len


y_std_sum = 0 
for i in range(data_len):
	y_std_sum =  y_std_sum + ( data[i][1]['y'] - y_mean)**2

y_std = math.sqrt(y_std_sum/data_len)
