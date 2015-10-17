from PyQt5.QtWidgets import QPushButton,QLabel,QWidget,QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import Qt,QRect#,pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QPainterPath, QPalette,QBrush,QPen,QFont#,QPixmap,#QRegion,QPainterPath,QTransform , QColor,QImage
#from PIL import Image

class textQLabel(QLabel):
    def __init__(self,parent,text):
        QLabel.__init__(self,parent)
        self.parent=parent
        self.text=text
        self.setText(text)
        self.setAlignment(Qt.AlignCenter)
        font=QFont()
        font.setPointSize(self.parent.height()/2)
        self.setFont(font)
    def resizeEvent(self,ev):
        self.resize(self.parent.size())



class ModCloseButton(QPushButton):
    def __init__(self,parent,wide,high,path=None):
        QPushButton.__init__(self,parent)

        self.parent=parent
        self.wide=wide
        self.high=high
        self.xdis=self.wide/10

        #self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.backgroundColor = QPalette().light().color()
        self.backgroundColor.setRgb(157,157,157) #(220,203,231)
        #self.backgroundColor.setAlpha(100)
        self.brush=QBrush(Qt.SolidPattern)

        if path :
            self.path=path
        else :
            self.path=QPainterPath()

            self.path.moveTo(self.wide/2, self.high/2-self.xdis)
            self.path.arcTo(0,0, self.wide-2*self.xdis, self.high-2*self.xdis,45,90)
            self.path.closeSubpath()

            self.path.moveTo(self.wide/2-self.xdis, self.high/2)
            self.path.arcTo(0,0,self.wide-2*self.xdis,self.high-2*self.xdis,135,90)
            self.path.closeSubpath()

            self.path.moveTo(self.wide/2, self.high/2+self.xdis)
            self.path.arcTo(0,0,self.wide-2*self.xdis, self.high-2*self.xdis,225,90)
            self.path.closeSubpath()

            self.path.moveTo(self.wide/2+self.xdis, self.high/2)
            self.path.arcTo(0,0,self.wide-2*self.xdis, self.high-2*self.xdis,315,90)
            self.path.closeSubpath()

    def paintEvent(self,event):
        self.brush.setColor(self.backgroundColor)
        self.painter=QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)

        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(self.brush)
        self.painter.drawPath(self.path)
        self.painter.end()

    def mousePressEvent(self,ev):
        self.parent.close()

    def enterEvent(self,ev):
        self.backgroundColor.setRgb(234,39,13) 
        self.update()
        
    def leaveEvent(self,ev):
        self.backgroundColor.setRgb(157,157,157)
        self.update()

class ModCrossButton(QPushButton):
    def __init__(self,parent,wide,high,path=None):
        QPushButton.__init__(self,parent)

        self.parent=parent
        self.wide=wide
        self.high=high
        self.xdis=self.wide/7
        self.ydis=self.xdis

        #self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.backgroundColor = QPalette().light().color()
        self.backgroundColor.setRgb(157,157,157) #(220,203,231)
        #self.backgroundColor.setAlpha(100)
        self.brush=QBrush(Qt.SolidPattern)

        if path :
            self.path=path
        else :
            self.path=QPainterPath()
            self.path.setFillRule(Qt.OddEvenFill)

            self.path.moveTo(self.wide/2, self.high/2-self.xdis)
            self.path.arcTo(0,0, self.wide, self.high,0,360)
            #self.path.closeSubpath()

            self.path.moveTo(self.wide/2-self.xdis/2, self.ydis)
            self.path.lineTo(self.wide/2-self.xdis/2, self.high/2-self.xdis/2)
            self.path.lineTo(self.ydis, self.high/2-self.xdis/2)
            self.path.lineTo(self.ydis, self.high/2+self.xdis/2)
            self.path.lineTo(self.wide/2-self.xdis/2, self.high/2+self.xdis/2)
            self.path.lineTo(self.wide/2-self.xdis/2, self.high-self.ydis)
            self.path.lineTo(self.wide/2+self.xdis/2, self.high-self.ydis)
            self.path.lineTo(self.wide/2+self.xdis/2, self.high/2+self.xdis/2)
            self.path.lineTo(self.wide-self.ydis, self.high/2+self.xdis/2)
            self.path.lineTo(self.wide-self.ydis, self.high/2-self.xdis/2)
            self.path.lineTo(self.wide/2+self.xdis/2, self.high/2-self.xdis/2)
            self.path.lineTo(self.wide/2+self.xdis/2, self.ydis)
            self.path.closeSubpath()

    def paintEvent(self,event):
        self.brush.setColor(self.backgroundColor)
        self.painter=QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)

        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(self.brush)
        self.painter.drawPath(self.path)
        self.painter.end()

    #def mousePressEvent(self,ev):
    #    self.parent.close()

    def enterEvent(self,ev):
        self.backgroundColor.setRgb(242,146,52) 
        self.update()
        
    def leaveEvent(self,ev):
        self.backgroundColor.setRgb(157,157,157)
        self.update()

class RoundedPushButton(QPushButton):
    def __init__(self,parent, default_wide, default_high,text=''):
        QPushButton.__init__(self, parent)
        #self.resize(100,80)
        self.default_high=default_high
        self.default_wide=default_wide
        self.xrd=self.default_wide/10
        #self.yrd=self.default_high/10
        self.yrd=self.xrd
        self.resize(self.default_wide,self.default_high)

        self.backgroundColor = QPalette().light().color()
        self.backgroundColor.setRgb(157,157,157) #(220,203,231)
        #self.backgroundColor.setAlpha(0)
        self.brush=QBrush(Qt.SolidPattern)

        self.textlabel=textQLabel(self,text)

    def paintEvent(self,event):
        #brush.setStyle(Qt.Dense1Pattern)
        self.brush.setColor(self.backgroundColor)
        self.painter=QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        
        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(self.brush)
        self.painter.drawRoundedRect(QRect(0,0,self.default_wide,self.default_high), self.xrd, self.yrd)
        #self.painter.drawPixmap(self.imgx, self.imgy, self.piximg)
        self.painter.end()
class WLLineLabel(QLabel):
    def __init__(self,parent):
        QLabel.__init__(self,parent)
        self.linelength=parent.width()
        self.lineheight=parent.lineheight
        self.resize(self.linelength, self.lineheight)
        self.move(0,0)
        self.stats=None
        self.setStyleSheet("{background-color:transparent;border:none;}")
    def resizeEvent(self,event):
        self.resize(self.linelength, self.lineheight)
        print(self.geometry())
    def statsReset(self):
        self.stats=None
        self.setStyleSheet("{background-color:transparent;border:none;}")
    def _mousePressEvent(self):
        if self.stats == 'selected' :
            self.stats = None
            self.setStyleSheet("{background-color:transparent;border:none;}")
        else:
            self.stats = 'selected'
            self.setStyleSheet("{background-color:(242,146,52);border:none;}")
        #self.update()

    def _enterEvent(self):
        if self.stats != 'selected' :
            self.setStyleSheet("{background-color:(242,146,52);border:none;}")
            #self.update()
        
    def _leaveEvent(self):
        if self.stats != 'selected' :
            self.setStyleSheet("{background-color:transparent;border:none;}")
            #self.update()
class WLTextQLabel(textQLabel):
    def resizeEvent(self,ev):
        self.resize( self.parent.width(), self.parent.height()-self.parent.lineheight )
        self.move( 0,self.parent.lineheight )

    def _moveEvent(self,xd,yd):
        self.move(self.x()+xd, self.y()+yd)

class WindowLabel(QWidget):
    def __init__(self,parent,filename):
        QWidget.__init__(self,parent)
        self.parent=parent
        #self.layout=QVBoxLayout()
        self.setStyleSheet("{background-color:(242,146,52);border:none;}")
        self.id=0
        self.lineheight=3
        self.labeltext=filename
        self.linelabel=WLLineLabel(self)
        self.ltextlabel=WLTextQLabel(self,self.labeltext)
        #self.linelabel.hide()
        #self.ltextlabel.hide()
        print('linelabel',self.linelabel.geometry())
        print('ltextlabel',self.ltextlabel.geometry(),self.ltextlabel.text)
        #self.layout.addWidget(self.linelabel)
        #self.layout.addWidget(self.ltextlabel)
        #self.setLayout(self.layout)
    def statsReset(self):
        self.linelabel.statsReset()

    def resizeEvent(self,ev):
        print('resizeEvent')
        ttlenght=0.686*self.parent.width()
        ttpagenum=len(self.parent.page)
        width=min( ttlenght/ttpagenum, 0.1*self.parent.width() )
        height=self.parent.height()/60
        self.resize(width,height)
        print('WindowLabel',self.geometry())
        #self.resize(self.parent.width(),self.parent.height())
    def moveEvent(self,ev):
        print('move')
        self.move(ev)
        print(ev,type(ev))
        self.ltextlabel._moveEvent(1,1)

    def mousePressEvent(self,ev):
        self.parent.displayWindowShow(self.id)
        self.linelabel._mousePressEvent()

    def enterEvent(self,ev):
        self.linelabel._enterEvent()
        
    def leaveEvent(self,ev):
        self.linelabel._leaveEvent()