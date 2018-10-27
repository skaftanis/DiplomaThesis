import time

import numpy as np
from sklearn.svm import SVR


# xbox = []
# wheel = []


# with open('wheel_data_points') as file:
# 	for i in range(41):
# 		cur_line = file.readline()
# 		ar = []
# 		ar.append(cur_line.split(" ")[0])
# 		ar = np.array(ar)
# 		xbox.append(ar)

# 		ar = []
# 		ar.append(cur_line.split(" ")[1].replace('\n',''))
# 		ar = np.array(ar)

# 		wheel.append(ar)


# for i in range(len(xbox)):
# 	xbox[i][0] = float(xbox[i][0])
# 	wheel[i][0] = float(wheel[i][0])

import numpy as np 
import numpy.polynomial.polynomial as poly
#from matplotlib import pyplot as plt


# xbox = np.array(xbox)
# wheel = np.array(wheel)

# X = wheel
# y = xbox

# svr_rbf = SVR(kernel='rbf', C=1e3, gamma=50)

# y_rbf = svr_rbf.fit(X, y).predict(X)


while True:

    steering = open("current_steering.txt")
    braking = open("current_brakes.txt")
    throttle = open("current_throttle.txt")
    # gearUP = open("current_gearUp.txt")
    # gearDown = open("current_gearDown.txt")

    #time.sleep(1)

    #print (steering.read())
    str_fl = steering.read()
    print(str_fl)

    #print(str( int(((str_fl+1)/2)*32767) ) )


    #print (steering.read() + " , " + throttle.read() + " , " + braking.read())
    # if str_fl != "":
    # 	print(str(str_fl) + " " + str(svr_rbf.predict(float(str_fl))))



