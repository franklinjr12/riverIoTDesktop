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
from azure_blob_downloader import *
import threading
import time
import serial
matplotlib.use("TkAgg")


LARGE_FONT = ("Verdana", 12)
style.use("ggplot")


f = Figure(figsize=(5, 5), dpi=100)
f.tight_layout()
f.subplots_adjust(wspace=0.2, hspace=0.3)

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

all_data = None

should_animate = False


def animateGraph(graph):
    if(all_data != None):
        title = graph.get_title()
        pullData = []
        if(title == "River level"):
            pullData = [float(data["deviceData"]["d"]) for data in all_data]
        elif(title == "Device battery"):
            for data in all_data:
                try:
                    pullData.append(float(data["deviceData"]["v"]))
                except:
                    pullData.append(float(0))
        elif(title == "Local pressure"):
            pullData = [float(data["deviceData"]["p"]) for data in all_data]
        elif(title == "Local temperature"):
            pullData = [float(data["deviceData"]["t"]) for data in all_data]
        else:
            return
        xList = [float(data["deviceData"]["time"]) for data in all_data]
        yList = pullData
        graph.clear()
        graph.plot(xList, yList)
        xlabel = graph.get_xlabel()
        ylabel = graph.get_ylabel()
        if(float(min(yList))*1.2 < 0):
            graph.set_ylim([float(min(yList))*1.2, float(max(yList))*1.2])
        else:
            graph.set_ylim([0, float(max(yList))*1.2])
        graph.set_title(title)
        graph.set_xlabel(xlabel)
        graph.set_ylabel(ylabel)


def animate(i):
    global should_animate
    if(should_animate == True):
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

        for F in (StartPage, PageOne, PageTwo, PageThree, PageData, PageRealTime):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        # self.show_frame(PageRealTime)

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

        button4 = ttk.Button(self, text="Real time",
                             command=lambda: controller.show_frame(PageRealTime))
        button4.pack()


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
        self.controller = controller
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
                             command=self.load_data)
        button3.pack()

    def load_data(self):
        global should_animate
        should_animate = True
        global all_data
        all_data = get_data_from_date("2022/06/19")
        animate(0)
        should_animate = False
        self.controller.show_frame(PageData)


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

        # animateGraph(level)
        # animateGraph(temperatureGraph)
        # animateGraph(pressureGraph)
        # animateGraph(batteryGraph)


class PageRealTime(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Real time", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.read_thread = None
        self.stop_thread = False
        self.controller = controller
        self.should_ping = False
        self.zero_offset = 0
        button1 = ttk.Button(self, text="Back to options",
                             command=self.back_home)
        button1.pack()
        # samplingText = Text(self, width=15, height=1)
        # samplingText.insert("1.0", "Type port like COM5")
        # samplingText["state"] = "normal"
        # samplingText.pack()
        self.comPort = StringVar()
        port = ttk.Entry(self, textvariable=self.comPort)
        port.pack()
        button2 = ttk.Button(self, text="Connect",
                             command=self.connect)
        button2.pack()
        button3 = ttk.Button(self, text="Download",
                             command=self.download)
        button3.pack()
        button4 = ttk.Button(self, text="Zero",
                             command=self.zero)
        button4.pack()
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def connect(self):
        if(self.comPort != None):
            try:
                print("connecting to port "+self.comPort.get())
                self.ser = serial.Serial(
                    port=self.comPort.get(), baudrate=115200)
                self.read_thread = threading.Thread(
                    target=self.read_data)
                self.read_thread.start()
            except Exception as ex:
                self.ser.close()
                print("couldnt open port "+self.comPort.get())
                print(ex)

    def read_data(self):
        global all_data
        global should_animate
        self.time = 1655673099
        self.last_level = 0
        if(all_data != None):
            all_data.clear()
        else:
            all_data = []
            # j = json.loads(
            #     "{\"deviceData\":{\"id\":\"riverdatalogger1\",\"d\":668.620667,\"v\":4.00,\"p\":916.94,\"t\":18.85,\"a\":861.45,\"time\":"+str(self.time)+"}}")
            # all_data.append(j)
        self.should_ping = True
        self.ping_thread = threading.Thread(target=self.ping_board)
        self.ping_thread.start()
        while(True):
            if(self.stop_thread == True):
                break
            # j = json.loads(
            #     "{\"deviceData\":{\"id\":\"riverdatalogger1\",\"d\":668.620667,\"v\":4.00,\"p\":916.94,\"t\":18.85,\"a\":861.45,\"time\":"+str(self.time)+"}}")
            # all_data.append(j)
            # self.time += 1
            try:
                line = self.ser.readline().decode("utf-8")
                print("income: "+line)
                while(line.startswith("{\"deviceData") == False):
                    line = self.ser.readline().decode("utf-8")
                    print("income: "+line)
                self.should_ping = False
                j = json.loads(line)
                self.last_level = float(j["deviceData"]["d"])
                j["deviceData"]["d"] = self.zero_offset - \
                    float(j["deviceData"]["d"])
                print(j["deviceData"]["d"])
                all_data.append(j)
                should_animate = True
            except Exception as ex:
                self.ser.flushInput()
                self.ser.flushOutput()
                print("exception on reading")
                print(ex)
            time.sleep(0.1)

    def ping_board(self):
        while(self.should_ping == True):
            try:
                self.ser.write(b"ping")
            except:
                pass
            time.sleep(0.1)

    def back_home(self):
        self.stop_thread = True
        self.controller.show_frame(PageOne)

    def download(self):
        pass

    def zero(self):
        self.zero_offset = self.last_level
        global level
        level.clear()
        pass


# all_data = get_data_from_date("2022/06/19")
app = App()
# animateGraph(level)
# animateGraph(temperatureGraph)
# animateGraph(pressureGraph)
# animateGraph(batteryGraph)
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
