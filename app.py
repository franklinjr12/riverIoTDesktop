from tkinter import ttk
from tkinter import *
import tkinter as tk
from matplotlib import style
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
except ImportError:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg
import matplotlib
matplotlib.use("TkAgg")


LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

matplotlib.rc("xtick", labelsize=4)
matplotlib.rc("ytick", labelsize=6)

f = Figure(figsize=(5, 5), dpi=100)
f.tight_layout()
f.subplots_adjust(wspace=0.2, hspace=0.6)

level = f.add_subplot(212)
# level.set_ylim([0, 6])
level.set_title("River level")
level.set_xlabel("time")
level.set_ylabel("cm")

batteryGraph = f.add_subplot(231)
# batteryGraph.set_ylim([0, 4.5])
batteryGraph.set_title("Device battery")
batteryGraph.set_xlabel("time")
batteryGraph.set_ylabel("volts")

pressureGraph = f.add_subplot(232)
# pressureGraph.set_ylim([0, 1100])
pressureGraph.set_title("Local pressure")
pressureGraph.set_xlabel("time")
pressureGraph.set_ylabel("hPa")

temperatureGraph = f.add_subplot(233)
# temperatureGraph.set_ylim([0, 30])
temperatureGraph.set_title("Local temperature")
temperatureGraph.set_xlabel("time")
temperatureGraph.set_ylabel("ºC")


def animateGraph(graph):
    title = graph.get_title()
    pullData = None
    if(title == "River level"):
        pullData = open("level.txt", "r").read()
    elif(title == "Device battery"):
        pullData = open("battery.txt", "r").read()
    elif(title == "Local pressure"):
        pullData = open("pressure.txt", "r").read()
    elif(title == "Local temperature"):
        pullData = open("temperature.txt", "r").read()
    else:
        pullData = open("samples.txt", "r").read()
    # pullData = open("samples.txt", "r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(float(x))
            yList.append(float(y))
    graph.clear()
    graph.plot(xList, yList)
    xlabel = graph.get_xlabel()
    ylabel = graph.get_ylabel()
    graph.set_ylim([0, float(max(yList))*1.2])
    # graph.set_ylim([0, 10])
    graph.set_title(title)
    graph.set_xlabel(xlabel)
    graph.set_ylabel(ylabel)


def animate(i):
    animateGraph(level)
    animateGraph(batteryGraph)
    animateGraph(pressureGraph)
    animateGraph(temperatureGraph)
    # pass


class App(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        APP_TITLE = "River IoT Monitor"
        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, APP_TITLE)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageData):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        PAGE_TITLE = "Homepage"
        label = tk.Label(self, text=PAGE_TITLE, font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        PAGE_CONFIGURATION = "Device configuration"
        button = ttk.Button(self, text=PAGE_CONFIGURATION,
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="page 2",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        PAGE_VISUALIZATION = "Data view"
        button3 = ttk.Button(self, text=PAGE_VISUALIZATION,
                             command=lambda: controller.show_frame(PageThree))
        button3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        PAGE_TITLE = "Device configuration"
        label = tk.Label(self, text=PAGE_TITLE, font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        samplingText = Text(self, width=15, height=3)
        samplingText.insert("1.0", "Actual sample\nrate is\n 48 per day")
        samplingText["state"] = "normal"
        samplingText.pack()

        samplingText2 = Text(self, width=15, height=3)
        samplingText2.insert("1.0", "Choose sample\nrate")
        samplingText2["state"] = "normal"
        samplingText2.pack()

        samplingListOptions = ["1 per day", "2 per day", "4 per day",
                               "8 per day", "12 per day", "24 per day", "48 per day"]
        samplingListVar = StringVar(value=samplingListOptions)
        samplingList = Listbox(self, width=20, listvariable=samplingListVar)
        samplingList.pack(side=LEFT)

        button2 = ttk.Button(self, text="Update configuration",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack(side=RIGHT)

        # frame1 = ttk.Frame(self)
        # frame1.grid(row=0, column=0, rowspan=1, columnspan=1)
        # frame1.pack()

        # button2 = ttk.Button(self, text="Update configuration",
        #                      command=lambda: controller.show_frame(PageTwo))
        # button2.pack()

        # feet = StringVar()
        # feet_entry = ttk.Entry(self, width=20, textvariable=feet)
        # feet_entry.pack()
        # feet_entry.grid(column=2, row=1, sticky=(W, E))


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                             command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.grid(self, column=0, row=0, columnspan=4, rowspan=3)
        label = tk.Label(self, text="Device data", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to devices",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Configure",
                             command=lambda: controller.show_frame(StartPage))
        button2.pack()

        label2 = tk.Label(self, text="Choose start date or\ntype the day")
        label2.pack(pady=10, padx=10)

        samplingText2 = Text(self, width=15, height=1)
        samplingText2.insert("1.0", "dd/mm/aaaa")
        samplingText2["state"] = "normal"
        samplingText2.pack()

        samplingListOptions = ["first day",  "last week", "last month",
                               "last day"]
        samplingListVar = StringVar(value=samplingListOptions)
        samplingList = Listbox(self, width=20, height=4,
                               listvariable=samplingListVar)
        samplingList.pack()

        label2 = tk.Label(self, text="Choose end date or\ntype the day")
        label2.pack(pady=10, padx=10)

        samplingText = Text(self, width=15, height=1)
        samplingText.insert("1.0", "dd/mm/aaaa")
        samplingText["state"] = "normal"
        samplingText.pack()

        samplingListOptions = ["first day", "last week", "last month",
                               "last day"]
        samplingListVar = StringVar(value=samplingListOptions)
        samplingList = Listbox(self, width=20, height=4,
                               listvariable=samplingListVar)
        samplingList.pack()

        button3 = ttk.Button(self, text="Show data",
                             command=lambda: controller.show_frame(PageData))
        button3.pack()


class PageData(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Device data", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to options",
                             command=lambda: controller.show_frame(PageThree))
        button1.pack()

        button2 = ttk.Button(self, text="Export csv",
                             command=lambda: controller.show_frame(PageThree))
        button2.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = App()
animateGraph(level)
animateGraph(temperatureGraph)
animateGraph(pressureGraph)
animateGraph(batteryGraph)
# ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
