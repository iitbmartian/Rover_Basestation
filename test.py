import matplotlib.pyplot as plt
import time
import random
import numpy as np

ysample = random.sample(xrange(0, 50), 50)

xdata = []
ydata = []

plt.show()

axes = plt.gca()
axes.set(xlabel='time', ylabel='RSSI', title='Prediction plot')

axes.set_xlim(0, 50)
x = np.arange(0,51,1)
axes.fill_between(x, 0, 10, facecolor='tan')
axes.set_ylim(0, +50)
line, = axes.plot(xdata, ydata, linewidth=2, color='g')
axes.hlines(y=10, xmin=0, xmax=50, linewidth=2, color='r')


for i in range(50):
	xdata.append(i)
	ydata.append(ysample[i])
	line.set_xdata(xdata)
	line.set_ydata(ydata)
	plt.draw()
	plt.pause(1e-4)
	time.sleep(0.1)

# add this if you don't want the window to disappear at the end 
plt.show()