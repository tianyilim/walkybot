import csv
import matplotlib.pyplot as plt
import numpy as np

# Get max/min values for data
ACCEL_MAX_X = 9.485
ACCEL_MIN_X = -10.097
ACCEL_MAX_Y = 9.561
ACCEL_MIN_Y = -9.791 
ACCEL_MAX_Z = 8.988

ACCEL_X_RANGE = ACCEL_MAX_X - ACCEL_MIN_X
ACCEL_Y_RANGE = ACCEL_MAX_Y - ACCEL_MIN_Y
# No min val for Z yet unfortunately

xdata = np.zeros(0) # initialize empty arrays for all 3 axes + time
ydata = np.zeros(0)
zdata = np.zeros(0)
xdata_filt = np.zeros(0)
ydata_filt = np.zeros(0)
zdata_filt = np.zeros(0)
t = np.zeros(0)

with open('accel_data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        t = np.append(t, float(row[0]))
        xdata = np.append(xdata, float(row[1]))
        ydata = np.append(ydata, float(row[2]))
        zdata = np.append(zdata, float(row[3]))
        xdata_filt = np.append(xdata_filt, float(row[4]))
        ydata_filt = np.append(ydata_filt, float(row[5]))
        zdata_filt = np.append(zdata_filt, float(row[6]))

time_ref = int(t[0])
t = (t-time_ref) # time since start

# Sample rate is around 270Hz (and might reduce with more devices on the i2c bus)\
# Device sample rate has been set to 200Hz.

# Moving average filter: Group N samples and take average so far.
x_avgs = np.zeros(0)
y_avgs = np.zeros(0)
z_avgs = np.zeros(0)
moving_avg = 20
for i in range(len(xdata) - moving_avg):
    x_avgs = np.append(x_avgs, np.average(xdata[i:i+moving_avg]))
    y_avgs = np.append(y_avgs, np.average(ydata[i:i+moving_avg]))
    z_avgs = np.append(z_avgs, np.average(zdata[i:i+moving_avg]))

print("x-axis - max: %0.8f, min: %0.8f, diff: %0.8f" %(np.max(xdata), np.min(xdata), np.max(xdata)-np.min(xdata)))
print("x-avg - max: %0.8f, min: %0.8f, diff: %0.8f" %(np.max(x_avgs), np.min(x_avgs), np.max(x_avgs)-np.min(x_avgs)))
print("y-axis - max: %0.8f, min: %0.8f, diff: %0.8f" %(np.max(ydata), np.min(ydata), np.max(ydata)-np.min(ydata)))
print("y-avg - max: %0.8f, min: %0.8f, diff: %0.8f" %(np.max(y_avgs), np.min(y_avgs), np.max(y_avgs)-np.min(y_avgs)))
print("z-axis - max: %0.8f, min: %0.8f, diff: %0.8f" %(np.max(zdata), np.min(zdata), np.max(zdata)-np.min(zdata)))
print("z-avg - max: %0.8f, min: %0.8f, diff: %0.8f" %(np.max(z_avgs), np.min(z_avgs), np.max(z_avgs)-np.min(z_avgs)))

print("")

x_diff = ( np.max(x_avgs)-np.min(x_avgs) ) / ( np.max(xdata)-np.min(xdata) ) *100
y_diff = ( np.max(y_avgs)-np.min(y_avgs) ) / ( np.max(ydata)-np.min(ydata) ) *100
z_diff = ( np.max(z_avgs)-np.min(z_avgs) ) / ( np.max(zdata)-np.min(zdata) ) *100
print("new absolute error as %% of original: x: %0.6f, y: %0.6f, z: %0.6f" %(x_diff, y_diff, z_diff) )

print("X ambient noise: %0.8f" %( (np.max(xdata)-np.min(xdata))/ACCEL_X_RANGE * 100 ) )
print("Y ambient noise: %0.8f" %( (np.max(ydata)-np.min(ydata))/ACCEL_Y_RANGE * 100 ) )
print("")

print("Post-filter X noise: %0.8f" %( (np.max(x_avgs)-np.min(x_avgs))/ACCEL_X_RANGE * 100 ))
print("Post-filter Y noise: %0.8f" %( (np.max(y_avgs)-np.min(y_avgs))/ACCEL_Y_RANGE * 100 ))

fig, axs = plt.subplots(1,3)
fig.suptitle("Data collected from accelerometer at rest")

axs[0].plot(t, xdata, '.-', label="raw")
axs[0].plot(t, xdata_filt, '.-', label="raw_avg")
axs[0].plot(t[:-moving_avg], x_avgs, '.-', label="moving_avg")
axs[0].set_xlabel("Time / S")
axs[0].set_ylabel("Accelerometer X axis")
axs[0].grid()

axs[1].plot(t, ydata, '.-', label="raw")
axs[1].plot(t, ydata_filt, '.-', label="raw_avg")
axs[1].plot(t[:-moving_avg], y_avgs, '.-', label="moving_avg")
axs[1].set_xlabel("Time / S")
axs[1].set_ylabel("Accelerometer Y axis")
axs[1].grid()

axs[2].plot(t, zdata, '.-', label="raw")
axs[2].plot(t, ydata_filt, '.-', label="raw_avg")
axs[2].plot(t[:-moving_avg], z_avgs, '.-', label="moving_avg")
axs[2].set_xlabel("Time / S")
axs[2].set_ylabel("Accelerometer Z axis")
axs[2].grid()

plt.legend()
plt.show()

# We conclude that a moving average filter of length 20 gives decent results, FWIW. Given a higher sampling rate, better things can be achieved.