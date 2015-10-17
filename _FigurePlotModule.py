#FigurePlotModule

from numpy import arange,  pi, cos, sin
from numpy.random import rand
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.setStyleSheet("{background-color:transparent;border:none;}")

        '''FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)'''

        FigureCanvas.updateGeometry(self)

        self.tootlbar=NavigationToolbar(self,parent)
        self.tootlbar.hide()

        self.fid=0
        self.data=[]
        self.index=[]
        
        

    def compute_initial_figure(self):
        pass

class FigurePlot(MyMplCanvas):
    def data_load(self,data):
        self.data=data
        self.index=arange(len(self.data))
    def bar_plot(self):
        #self.index=arange(len(self.data))
        #print(self.index,self.data)
        self.axes.bar(self.index,[x[1] for x in self.data])
        self.draw()
    def plot_plot(self):
        #print(self.data)
        self.axes.plot([x[0] for x in self.data],[x[1] for x in self.data])
        self.draw()

    def scartter_plot(self):
        rx, ry = 3., 1.
        area = rx * ry * pi
        theta = arange(0, 2*pi+0.01, 0.1)
        verts = list(zip(rx/area*cos(theta), ry/area*sin(theta)))

        x,y,s,c = rand(4, 30)
        #print(x,y,s,c)
        s*= 10**2.

        #fig, ax = plt.subplots()
        self.axes.scatter(x,y,s,c,marker=None,verts =verts)
        self.draw()

