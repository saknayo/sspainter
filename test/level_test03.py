import sys
import random
from PyQt5 import QtGui,QtCore,QtWidgets

class textQLabel(QtWidgets.QLabel):
    def __init__(self,parent,text):
        super(textQLabel,self).__init__(parent)
        self.parent=parent
        self.text=text
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignCenter)
        font=QtGui.QFont()
        font.setPointSize(self.parent.height()/2)
        self.setFont(font)
    def resizeEvent(self,ev):
        self.resize(self.parent.size())


class RoundedPushButton(QtWidgets.QPushButton):
    def __init__(self,parent, default_wide, default_high,text=''):
        super(RoundedPushButton,self).__init__(parent)
        #self.resize(100,80)
        self.default_high=default_high
        self.default_wide=default_wide
        self.xrd=self.default_wide/10
        #self.yrd=self.default_high/10
        self.yrd=self.xrd
        #self.resize(self.default_wide,self.default_high)

        self.backgroundColor = QtGui.QPalette().light().color()
        self.backgroundColor.setRgb(157,157,157) #(220,203,231)
        #self.backgroundColor.setAlpha(0)
        self.brush=QtGui.QBrush(QtCore.Qt.SolidPattern)

        self.textlabel=textQLabel(self,text)

    def paintEvent(self,event):
        self.brush.setColor(self.backgroundColor)
        self.painter=QtGui.QPainter(self)
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        self.painter.setPen(QtCore.Qt.NoPen)
        self.painter.setBrush(self.brush)
        self.painter.drawRoundedRect(QtCore.QRect(0,0,self.default_wide,self.default_high), self.xrd, self.yrd)
        self.painter.end()
        print('paint',self.geometry())

class WL1(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(WL1, self).__init__(parent)
        #QtWidgets.QWidget.__init__(self,parent)
        self.move(0,0)
        print(1)
        self.resize(200,200)
        print(2)
        self.setStyleSheet("{background-color:(242,146,52);border:none;}")
        layout=QtWidgets.QVBoxLayout()

        self.rdpb=RoundedPushButton(self,100,30,'roundedpushbotton')
        #self.rdpb.resize(100,30)
        self.rdpb.move(100,50)
        
        self.pb=QtWidgets.QPushButton('childPB',self)
        self.ql=QtWidgets.QLabel(self)
        self.ql.setText('helo world')
        self.ql.setStyleSheet("{background-color:(242,146,52);border:none;}")

        self.tb=textQLabel(self,'textQLabel')

        self.move(40,0)
        
        #self.pb.move(0,50)
        print('child pb',self.pb.geometry())
        #self.ql.move(200,200)
        layout.addWidget(self.ql)
        #self.setLayout(layout)
        print(self.geometry(),self.ql.geometry())
    def mvev(self):
        #self.ql.resize(100,100)
        #self.ql.move(100,100)
        print(6)
        #self.resize(500,500)
        self.resize(random.randint(100,400),random.randint(100,400))
        print(7)
        print('after move:',self.geometry(),self.ql.geometry())
    def resizeEvent(self,ev):
        print('resize')
        self.move(random.randint(100,800),random.randint(100,800))
        self.resize(ev.size())
        print(ev,self.geometry())
class ApplicationWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.m_DragPosition=self.pos()
        self.avasize=QtWidgets.QDesktopWidget().availableGeometry()#screenGeometry()
        self.setGeometry(self.avasize)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint )
        self.setFocus()

        tw=WL1(self)
        self.tw=tw
        print(tw.geometry(),tw.ql.geometry(),tw.rdpb.geometry())
        print(3)
        tw.move(10,10)
        print(4)

        qw=QtWidgets.QWidget(self)

        pb=QtWidgets.QPushButton(self)
        pb.move(700,100)
        print('pb',pb.geometry())
        pb.setText('Push')
        pb.clicked.connect(tw.mvev)
        #pb.clicked.connect(self.pv)
        print(5)

    def pv(self):
        self.tw.move(200,200)
        print('pv',self.tw.geometry(),self.tw.ql.geometry())
qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
#aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
