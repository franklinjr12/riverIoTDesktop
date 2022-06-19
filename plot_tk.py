from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter.ttk import *

import matplotlib
matplotlib.use("TkAgg")


root = Tk()

figure = Figure(figsize=(5, 4), dpi=100)
plot = figure.add_subplot(1, 1, 1)

plot.plot(0.5, 0.3, color="#C41E3A", marker="o",
          linestyle="")  # Plotting points

x = [0.1, 0.2, 0.3]
y = [-0.1, -0.2, -0.3]
plot.plot(x, y, color="blue", marker="x", linestyle="")  # Plotting points

canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().grid(row=0, column=0)

root.mainloop()  # Running application
