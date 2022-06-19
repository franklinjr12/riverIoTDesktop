import time
from matplotlib import style
from matplotlib import pyplot
import matplotlib.animation as animation
from matplotlib.figure import Figure
import matplotlib


matplotlib.rc("xtick", labelsize=4)
matplotlib.rc("ytick", labelsize=6)

f = Figure(figsize=(5, 5), dpi=100)
f.tight_layout()
f.subplots_adjust(wspace=0.8, hspace=1.5)

level = f.add_subplot(212)
level.set_title("River level")
level.set_xlabel("time")
level.set_ylabel("cm")

batteryGraph = f.add_subplot(231)
batteryGraph.set_title("Device battery")
batteryGraph.set_xlabel("time")
batteryGraph.set_ylabel("volts")

pressureGraph = f.add_subplot(232)
pressureGraph.set_title("Local pressure")
pressureGraph.set_xlabel("time")
pressureGraph.set_ylabel("hPa")

temperatureGraph = f.add_subplot(233)
temperatureGraph.set_title("Local temperature")
temperatureGraph.set_xlabel("time")
temperatureGraph.set_ylabel("ºC")


def animateGraph(graph):
    title = graph.get_title()
    pullData = None
    # if(title == "River level"):
    #     pullData = open("level.txt", "r").read()
    # elif(title == "Device Battery"):
    #     pullData = open("battery.txt", "r").read()
    # elif(title == "Local pressure"):
    #     pullData = open("pressure.txt", "r").read()
    # elif(title == "Local temperature"):
    #     pullData = open("temperature.txt", "r").read()
    # else:
    #     pullData = open("samples.txt", "r").read()
    pullData = open("samples.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append((x))
            yList.append((y))

    xlabel = graph.get_xlabel()
    ylabel = graph.get_ylabel()
    graph.clear()
    graph.plot(xList, yList)
    graph.set_title(title)
    graph.set_xlabel(xlabel)
    graph.set_ylabel(ylabel)


animateGraph(level)
animateGraph(batteryGraph)
animateGraph(pressureGraph)
animateGraph(temperatureGraph)

# f.draw(matplotlib.backend_bases)
f.canvas.draw()
# f.canvas.show()
# f.show()
