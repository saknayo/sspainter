#!/usr/bin/env python

# embedding_in_qt4.py --- Simple Qt4 application embedding matplotlib canvases
#
# Copyright (C) 2005 Florent Rougon
#               2006 Darren Dale
#
# This file is an example program for matplotlib. It may be used and
# modified with no restriction; raw copies as well as modified versions
# may be distributed without limitation.

from __future__ import unicode_literals
import sys
import os
import random
from PyQt5 import QtGui,QtCore,QtWidgets
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from ext__button import ModCloseButton,RoundedPushButton, ModCrossButton, WindowLabel

def data_format(filepath):
    db=[]
    with open(filepath,'r')as f:
        for line in f:
            db.append( [float(x) for x in line.split()[1:]] )
    return db
    

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

        '''FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)'''

        FigureCanvas.updateGeometry(self)

        self.tootlbar=NavigationToolbar(self,parent)
        self.tootlbar.hide()
        
        

    def compute_initial_figure(self):
        pass

class FigurePlot(MyMplCanvas):
    def data_load(self,data):
        self.data=data
        self.index=arange(len(self.data))
    def bar_plot(self):
        self.axes.bar=(self.index,[x[1] for x in self.data])
        self.draw()
    def plot_plot(self):
        self.axes.plot([x[0] for x in self.data],[x[1] for x in self.data])
        self.draw()

class displayWindow(QtWidgets.QWidget):
    def __init__(self,parent):
        QtWidgets.QWidget.__init__(self,parent)
        
        self.layout=QtWidgets.QHBoxLayout()
        self.id=0
        self.parent=parent
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True) 
    def paintEvent (self, event):
        backgroundColor = QtGui.QPalette().light().color()
        backgroundColor.setRgb(255,255,255)
        backgroundColor.setAlpha(255)
        self.painter = QtGui.QPainter(self)
        self.painter.fillRect(event.rect(),backgroundColor)
        self.painter.end()
    def resizeEvent(self,ev):
        self.setGeometry(
            0.214*self.parent.width(),
            0.214*self.parent.height(),
            0.786*self.parent.width(),
            0.786*self.parent.height() )

class ApplicationWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.m_DragPosition=self.pos()
        self.avasize=QtWidgets.QDesktopWidget().availableGeometry()#screenGeometry()
        self.setGeometry(self.avasize)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint )
        self.setFocus()
        #self.setCentralWidget(self)
        self.cP=displayWindow(self)
        self.page=[self.cP]
        self.cL=WindowLabel(self,'')
        self.labelbox=[self.cL]
        self.cP.hide()
        self.cL.hide()

        mb=RoundedPushButton(self,100,40,'Zoom')
        print(mb.size())
        #mb.resize(100,40)
        mb.move(100,100)
        #mb.clicked.connect(sc.tootlbar.zoom)

        closeB=ModCloseButton(self,30,30)
        closeB.resize(closeB.size())
        closeB.move(self.width()-30,0)
        #print(cb.geometry())
        
        self.addB= ModCrossButton(self,100,100)
        self.addB.resize(100,100)
        self.addB.move(self.width()/2,self.height()/2)
        self.addB.clicked.connect(self.addNewFigure)
        #addB.clicked.connect(self.close)
        
    def addNewFigure(self):
        print('addB')
        filepath=QtWidgets.QFileDialog.getOpenFileName(self,"Data Load")[0]
        if not filepath.strip() :
            return
        # creat new display window
        self.cP.hide()
        self.page.append( displayWindow(self) )
        self.cP=self.page[-1]
        self.cP.id=len(self.page)-1
        self.cP.move( 0.214*self.width(),  0.214*self.height() )
        
        self.cP.hide()
        print('cp',self.cP.geometry())
        # fig plot
        databox=data_format(filepath)
        sc = FigurePlot(self.cP, width=5, height=4, dpi=100)
        sc.data_load(databox)#[[1,2],[2,3],[3,4]])
        sc.plot_plot()
        sc.resize(self.cP.width()/2,self.cP.height()/2)
        sc.move(self.cP.width()/2-sc.width()/2,self.cP.height()/2-sc.height()/2)
        print('sc',sc.geometry())
        #self.cP.layout.addWidget(sc)
        # fig label set 
        figl=WindowLabel(self, os.path.basename(filepath))
        figl.id=len(self.page)-1
        self.labelbox.append(figl)
        self.cL=self.labelbox[-1]
        if len(self.labelbox) == 1 :
            self.cL.move(0.214*self.width(), 0.214*self.height()-self.height()/60 )
        else :
            self.cL.move(0.214*self.width()+0.1*self.width()*len(self.labelbox), 0.214*self.height()-self.height()/60)
        self.cL.resize(100,30)
        print('windlabel',self.cL.geometry(),self.cL.linelabel.geometry(),self.cL.ltextlabel.geometry())
        # addBotton move
        self.addB.resize( self.cL.height(), self.cL.height() )
        self.addB.move( self.cL.x()+self.cL.width()+5, self.cL.y() )
        # left bar set
        
        
    def displayWindowShow(self,nid):
        self.cP.hide()
        self.cL.statsReset()
        self.cP=self.page[nid]
        self.cP.show()
        self.cL=self.labelbox[self.cP.id]

        # Just some button 
        '''
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plot)
 
        self.button1 = QtGui.QPushButton('Zoom')
        self.button1.clicked.connect(self.zoom)
         
        self.button2 = QtGui.QPushButton('Pan')
        self.button2.clicked.connect(self.pan)
         
        self.button3 = QtGui.QPushButton('Home')
        self.button3.clicked.connect(self.home)
        '''


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
#aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
