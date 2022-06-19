import numpy as np
import matplotlib
from matplotlib import pyplot

file = open("temperature.txt", "w")
# file = open("level.txt", "w")
# file = open("pressure.txt", "w")
# file = open("battery.txt", "w")


x = np.arange(0, 30, 1/12)
y_increment = np.arange(0, 6, 6/x.size)
y = []
for i in range(x.size):
    # temperature
    y.append(2.5*np.sin(2*np.pi*x[i])+17.5 +
             y_increment[i]+np.random.rand(1, 1)[0]*0.2)

    # level
    # y.append(1.5*np.sin(2*np.pi*x*2*[i])+3 +
    #          np.random.rand(1, 1)[0]*0.2)

    # pressure
    # y.append(1018 + y_increment[i] +
    #          np.random.rand(1, 1)[0]*0.01)

    # battery
    # y.append(4.2*(1-np.log(x[i]/1000+1)) +
    #          np.random.rand(1, 1)[0]*0.01)

    file.write("{:.2f},{:.2f}\n".format(x[i], y[i][0]))

fg, ax = pyplot.subplots()
ax.plot(x, y)
pyplot.show()

file.close()
