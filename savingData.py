import numpy as np
import time
import serial

ser = serial.Serial('/dev/ttyACM0', 115200)
ser.write('All set')

data = np.linspace(0, 1, 201)   # create array with 201 elements from 0 to 1, equally spaced
np.savetxt('A_data.dat', data)  # save data to a file in a column form

x = np.linspace(0, 1, 201)
y = np.random.rand(201)
data = np.column_stack((x, y))  # stack the arrays in columns
np.savetxt('AA_data.dat', data)

data = np.loadtxt('AA_data.dat') # load data
x = data[:, 0]
y = data[:, 1]

# saving dat while acquiring them
header = "X-Column, Y-Column\n"
header += "This is a second line"

file = open('A_data.dat', 'wb')     # opening the file
np.savetxt(file, [], header=header)
for i in range(201):
    data = np.column_stack((x[i], y[i]))
    np.savetxt(file, data)
    file.flush()
    time.sleep(1)

file.close()
