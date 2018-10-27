from model_hybrid import model_fc_2
import numpy as np

model = model_fc_2(1)

X = np.load("X_norm_final_data_1.0.npy")
Y = np.load("Y_norm_final_data_1.0.npy")

#mean absolute error
sumA = 0
for i in range(len(X)):
    sumA +=  abs ( model.predict(X[i].reshape(1,100,250,6))[0][0] - Y[i][0] )

mean_absolute = sumA/len(X)

#mean squared error
sumB = 0 

for i in range(len(X)):
    sumB +=   ( model.predict(X[i].reshape(1,100,250,6))[0][0] - Y[i][0] )**2

mean_squared = sumB/len(X)

print(mean_absolute)
print(mean_squared)





