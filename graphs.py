import matplotlib.pyplot as plot
import numpy as np

def bar_graph(x, y, x_label, y_label, title, filename):
    plot.bar(x, y, width=0.8)
    plot.legend()
    plot.title(title)
    plot.xlabel(x_label)
    plot.ylabel(y_label)
    plot.savefig("static/graphs/models/" + filename + ".png")
    plot.close()