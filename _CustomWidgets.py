#CustomWidgets
from PyQt5.QtWidgets import QPushButton,QLabel,QWidget,QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import Qt,QRect#,pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QPainterPath, QPalette,QBrush,QPen,QFont#,QPixmap,#QRegion,QPainterPath,QTransform , QColor,QImage





class ModCrossButton(QPushButton):
    def __init__(self,parent,path=None):
        QPushButton.__init__(self,parent)

        self.parent=parent


        #self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.backgroundColor = QPalette().light().color()
        self.backgroundColor.setRgb(157,157,157) #(220,203,231)
        #self.backgroundColor.setAlpha(100)
        self.brush=QBrush(Qt.SolidPattern)


    def paintEvent(self,event):
        self.wide=self.width()
        self.high=self.height()
        self.xdis=self.wide/7
        self.ydis=self.xdis

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

class ModCloseButton(QPushButton):
    def __init__(self,parent,wide,high,ppath=None):
        QPushButton.__init__(self,parent)

        self.parent=parent
        self.wide=wide
        self.high=high
        self.resize(self.wide,self.high)
        self.xdis=self.wide/10

        #self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.backgroundColor = QPalette().light().color()
        self.backgroundColor.setRgb(157,157,157) #(220,203,231)
        #self.backgroundColor.setAlpha(100)
        self.brush=QBrush(Qt.SolidPattern)

        if ppath :
            self.path=ppath
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


class WLLineLabel(QPushButton):
    def __init__(self,parent):
        super(WLLineLabel,self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint )
        self.linelength=1000
        self.lineheight=5
        self.resize(self.linelength, self.lineheight)
        self.move(100,100)
        self.stats=None
        #self.setStyleSheet("{background-color:transparent;border:none;color:transparent;}")

        self.backgroundColor = QPalette().light().color()
        self.backgroundColor.setRgb(157,157,157)#(220,203,231)
        #self.backgroundColor.setAlpha(255)
        self.brush=QBrush(Qt.SolidPattern)
    def paintEvent(self,event):
        self.brush.setColor(self.backgroundColor)
        self.painter=QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)

        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(self.brush)
        #print(self.geometry())
        self.painter.drawRect(0, 0, 1000, 5)
        self.painter.end()

    
    def statsReset(self):
        self.stats=None
        self.backgroundColor.setAlpha(255)
        self.redraw()
    def mousePressEvent(self,ev):
        if self.stats == 'selected' :
            self.stats = None
            self.backgroundColor.setAlpha(255)
        else:
            self.stats = 'selected'
            self.backgroundColor.setRgb(157,157,157)
        self.update()

    def enterEvent(self,ev):
        #print('enter')
        if self.stats != 'selected' :
            self.backgroundColor.setAlpha(0)
            self.update()
        
    def leaveEvent(self,ev):
        if self.stats != 'selected' :
            self.backgroundColor.setAlpha(255)
            self.update()
    
class FigLabelWidget(QWidget):
    def __init__(self,parent=None,text='FigLabelWidget'):
        super(FigLabelWidget,self).__init__(parent)
        self.parent=parent
        self.lx=5
        self.text=text
        self.fid=0
        self.stats=None

        self.linecolor=QPalette().light().color()
        self.linecolor.setRgb(157,157,157)
        self.backgroundColor = QPalette().light().color()
        self.backgroundColor.setRgb(187,187,187)
        self.brush=QBrush(Qt.SolidPattern)
        self.brush2=QBrush(Qt.SolidPattern)

        self.activeLabel()

    def paintEvent(self,ev):

        self.brush.setColor(self.linecolor)
        self.painter=QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(self.brush)
        self.painter.drawRect(0, 0, self.width(), self.lx)
        self.painter.end()

        #print(1)

        self.painter2=QPainter(self)
        self.painter2.setRenderHint(QPainter.Antialiasing)
        self.painter2.setPen(Qt.NoPen)
        self.painter2.setBrush(self.brush2)
        self.brush2.setColor(self.backgroundColor)
        self.painter2.drawRect(0,self.lx,self.width(),self.height()-self.lx)
        self.painter2.end()

        #print(2)

        self.painter3=QPainter(self)
        self.painter3.drawText(1,self.lx,self.width()-2,self.height()-self.lx,Qt.AlignCenter,self.text)
        self.painter3.end()

        #print(3)
    def activeLabel(self):
        self.stats = 'selected'
        self.linecolor.setRgb(242,146,52)
        self.update()

    def statsReset(self):
        self.stats=None
        self.linecolor.setRgb(157,157,157)
        #print('child reset',self.stats)
        self.update()
    def mousePressEvent(self,ev):
        if self.stats == 'selected' :
            pass
        else:
            self.activeLabel()
            self.parent.activeFig(self.fid)# ##### ##################################            connect to parent

    def enterEvent(self,ev):
        #print('enter')
        if self.stats != 'selected' :
            self.linecolor.setRgb(242,146,52)
            #self.backgroundColor.setRgb(227,227,227)
            self.update()
        
    def leaveEvent(self,ev):
        if self.stats != 'selected' :
            self.linecolor.setRgb(157,157,157)
            #self.backgroundColor.setRgb(187,187,187)
            self.update()


class RoundedPushButton1(QPushButton):
    def __init__(self,parent, default_wide, default_high,text=''):
        QPushButton.__init__(self, parent)
        #self.resize(100,80)
        self.default_high=default_high
        self.default_wide=default_wide
        self.xrd=self.default_wide/10
        #self.yrd=self.default_high/10
        self.yrd=self.xrd
        #self.resize(self.default_wide,self.default_high)

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

class RoundedPushButton(QPushButton):
    def __init__(self,parent, text=''):
        QPushButton.__init__(self, parent)
        self.text=text
        self.backgroundColor = QPalette().light().color()
        self.backgroundColor.setRgb(157,157,157) #(220,203,231)
        #self.backgroundColor.setAlpha(0)
        self.brush=QBrush(Qt.SolidPattern)

    def paintEvent(self,event):
        self.brush.setColor(self.backgroundColor)
        self.painter=QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        
        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(self.brush)
        self.painter.drawRoundedRect(QRect(0,0,self.width(),self.height()), self.width()/10, self.height()/10)
        self.painter.end()

        self.painter3=QPainter(self)
        self.painter3.drawText(1,0,self.width()-2,self.height(),Qt.AlignCenter,self.text)
        self.painter3.end()