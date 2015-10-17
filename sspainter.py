##FileName:sspainter.py

from __future__ import unicode_literals
import sys
import os
import random
from PyQt5 import QtGui,QtCore,QtWidgets

from _CustomWidgets import ModCloseButton ,WLLineLabel,FigLabelWidget,ModCrossButton,RoundedPushButton
from _FigurePlotModule import FigurePlot

def data_format(filepath):
    db=[]
    with open(filepath,'r')as f:
        for line in f:
            db.append( [float(x) for x in line.split()[1:]] )
    return db


class FigMana(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(FigMana,self).__init__(parent)
        self.parent=parent
        self.setGeometry(
            0.214*self.parent.width(),
            0.214*self.parent.height(),
            0.786*self.parent.width(),
            0.786*self.parent.height() )
        self.figbox={}
        self.active_fig=FigurePlot(self)
        self.active_fig.hide()

    def addFig(self,fid,figdata):
        newfig=FigurePlot(self)
        newfig.fid=str(fid)
        newfig.data_load(figdata)
        newfig.bar_plot()
        newfig.setGeometry(130,100,450,250)
        self.figbox[newfig.fid]=newfig
        self.activeFig(newfig.fid)

    def activeFig(self,actid):
        try :
            self.active_fig.hide()
        except :
            pass
        #print('active',self.active_fig.data)
        self.active_fig=self.figbox[actid]
        self.active_fig.show()
    def plotBar(self):
        self.active_fig.bar_plot()
    def plotPlot(self):
        self.active_fig.plot_plot()
    def plotScar(self):
        self.active_fig.scartter_plot()

    '''def displayUpdate(self):
        for i in self.figbox :
            if i  == self.active_fig.fid :
                self.figbox[i].show()
            else :
                self.figbox[i].hide()
    def figRefresh(self,actfigid):
        self.active_fig=self.figbox[actfigid]
        self.displayUpdate()'''

class FigLabelMana(QtWidgets.QWidget):
    def __init__(self,parent=None,figmanager=None):
        super(FigLabelMana,self).__init__(parent)
        self.parent=parent
        self.figmanager=figmanager
        self.resize(0.686*self.parent.width(),0.08*self.parent.height())
        self.move(0.214*self.parent.width(), 0.214*self.parent.height()-self.height()-5)
        self.figlabelbox={}
        self.figidbox=[]
        self.endpoint=0

    def addFigLabel(self,figname,figid):
        newfiglab=FigLabelWidget(self,figname)
        newfiglab.fid=str(figid)
        newfiglab.show()
        self.figidbox.append(newfiglab.fid)
        self.figlabelbox[newfiglab.fid]=newfiglab

        self.activeFig(newfiglab.fid)

        #print(self.geometry(),self.active_figl.geometry())
        self.layoutUpdate()
        #self.statsReset(self.active_figl.fid)
        print('update',self.geometry(),self.active_figl.geometry())

    def activeFig(self,actid):
        try :
            self.active_figl.statsReset()
        except :
            pass
        #print('figlabel',actid,self.figlabelbox)
        self.active_figl=self.figlabelbox[actid]
        self.figmanager.activeFig(actid)

    def layoutUpdate(self):
        w=min(self.width()/len(self.figlabelbox) , 150)
        h=self.height()
        for i in range(len(self.figidbox)) :
            clw=self.figlabelbox[ self.figidbox[i] ]
            if i == 0 :
                x=i*w 
            else :
                x=self.figlabelbox[ self.figidbox[i-1] ].x()+w
            y=0
            self.figlabelbox[ self.figidbox[i] ].setGeometry(x,y,w,h)
        self.endpoint=self.figlabelbox[ self.figidbox[-1] ].x() + self.figlabelbox[ self.figidbox[-1] ].width()
        #self.update()

    '''def statsReset(self,actfigid=None):
        self.active_figl=self.figlabelbox[actfigid]
        for i in self.figlabelbox :
            if i  == self.active_figl.fid :
                print('ipass',i)
                pass
            else :
                print('ireset',i)
                self.figlabelbox[i].statsReset()
    def displayFigUpdate(self,actfigid):
        self.figmanager.figRefresh(actfigid)
        print('actfigid:',actfigid)'''


class FigTpeMana(QtWidgets.QWidget):
    def __init__(self,parent,figmana):
        super(FigTpeMana,self).__init__(parent)
        self.parent=parent
        self.fm=figmana
        self.setGeometry(
            0,
            0.314*self.parent.height(),
            0.214*self.parent.width(),
            0.686*self.parent.height() )
        #layout=QtWidgets.QVBoxLayout()
     
        self.barB=RoundedPushButton(self,'Bar Plot')
        #self.barB.resize(100,50)
        #self.barB.move(10,100)
        self.barB.setGeometry(50,50,100,50)
        self.barB.clicked.connect(self.fm.plotBar)
        #layout.addWidget(self.barB)

        self.plotB=RoundedPushButton(self,'Plot Plot')
        self.plotB.setGeometry(50,110,100,50)
        self.plotB.clicked.connect(self.fm.plotPlot)
        #layout.addWidget(self.plotB)

        self.scarB=RoundedPushButton(self,'Scartter Plot')
        self.scarB.setGeometry(50,170,100,50)
        self.scarB.clicked.connect(self.fm.plotScar)
        #layout.addWidget(self.scarB)

        #self.setLayout(layout)

class ApplicationWindow(QtWidgets.QWidget):
    def __init__(self):
        super(ApplicationWindow,self).__init__()

        self.m_DragPosition=self.pos()
        self.avasize=QtWidgets.QDesktopWidget().availableGeometry()#screenGeometry()
        self.setGeometry(self.avasize)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint )
        self.setFocus()
        #self.setCentralWidget(self)
        self.widgets_set()
        '''
        tb=QtWidgets.QPushButton('test',self)
        tb.resize(100,50)
        tb.move(0,400)
        tb.clicked.connect(self.test)'''
    def test(self):
        self.fm.addFigLabel('ajfeh',random.randint(1,100))
        #self.lb.resize(100,40)


    def widgets_set(self):
        # add close button
        self.closeB=ModCloseButton(self,40,40)
        self.closeB.move( self.width()-40, 0 )

        # label region
        self.fm=FigMana(self)
        self.flm=FigLabelMana(self,self.fm)
        '''
        self.lb=FigLabelWidget(self)
        self.lb.move(100,100)
        self.lb.resize(200,100)
        print(self.lb.geometry())'''

        self.addB=ModCrossButton(self)
        self.addB.setGeometry(self.width()/2,self.height()/2,100,100)
        self.addB.clicked.connect(self.addFigure)

        # figure type 
        self.ftm=FigTpeMana(self,self.fm)


    def addFigure(self):
        filepath=QtWidgets.QFileDialog.getOpenFileName(self,"Data Load")[0]
        if not filepath.strip() :
            return
        filename=os.path.basename(filepath)
        fid=random.randint(1,100)
        # fig add
        self.fm.addFig( fid, data_format(filepath) )
        # label add 
        self.flm.addFigLabel(filename,fid)
        # addbutton move resize
        self.addB.resize( self.flm.height(), self.flm.height() )
        self.addB.move( self.flm.x()+self.flm.endpoint+5 , self.flm.y() )




if __name__ == '__main__' :

    qApp = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.show()
    sys.exit(qApp.exec_())
