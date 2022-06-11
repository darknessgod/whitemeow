from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPainter,QPixmap
from constants import *
import time


class mineLabel (QtWidgets.QLabel):
    leftRelease = QtCore.pyqtSignal (int, int)  # 定义信号
    rightRelease = QtCore.pyqtSignal (int, int)
    leftPressed = QtCore.pyqtSignal (int, int)
    rightPressed = QtCore.pyqtSignal (int, int)
    leftAndRightPressed = QtCore.pyqtSignal (int, int)
    leftAndRightRelease = QtCore.pyqtSignal (int, int)
    mouseMove = QtCore.pyqtSignal (int, int)

    def __init__(self, game, pixsize, parent=None):
        super (mineLabel, self).__init__ (parent)
        self.game=game
        self.leftAndRightClicked = False
        self.pixSize=pixsize
        self.pixmaps=[0]*30
        self.setMouseTracking(True)
        self.resizepixmaps(self.pixSize)
        self.lastcell=None

    def resizepixmaps(self,num):
        targetsize=num
        for i in range(1,9):
            pngname=CELL_PATH+"cell"+str(i)+".svg"
            self.pixmaps[i]=QPixmap(pngname)
        self.pixmaps[0]=QPixmap(CELL_PATH+"celldown.svg")
        self.pixmaps[9]=QPixmap(CELL_PATH+"cellup.svg")
        self.pixmaps[10]=QPixmap(CELL_PATH+"cellflag.svg")
        self.pixmaps[11]=QPixmap(CELL_PATH+"cellmine.svg")
        self.pixmaps[12]=QPixmap(CELL_PATH+"falsemine.svg")
        self.pixmaps[13]=QPixmap(CELL_PATH+"blast.svg")
        self.pixmaps[14]=QPixmap("media/svg/cellunflagged.svg")
        self.pixmaps[15]=QPixmap(CELL_PATH+"greencross.svg")
        self.pixmaps[16]=QPixmap(ELEMENT_PATH+"arrowcursor.svg")
        self.pixmaps[17]=QPixmap("media/hint.png")
        for i in range(16):
            self.pixmaps[i]=self.pixmaps[i].scaled(targetsize,targetsize)
        self.pixmaps[16]=self.pixmaps[16].scaled(targetsize,targetsize,transformMode=QtCore.Qt.SmoothTransformation)


    def mousePressEvent(self, e):  # 重载一下鼠标点击事件
        if not self.game.isreplaying():
            xx = int(e.localPos().x())
            yy = int(e.localPos().y())
            # print('点下位置{}, {}'.format(xx, yy))
            if e.buttons () == QtCore.Qt.LeftButton | QtCore.Qt.RightButton:
                self.leftAndRightPressed.emit (yy//self.pixSize, xx//self.pixSize)
                self.leftAndRightClicked = True
            else:
                if e.buttons () == QtCore.Qt.LeftButton:
                    self.leftPressed.emit(yy//self.pixSize, xx//self.pixSize)
                elif e.buttons () == QtCore.Qt.RightButton:
                    self.rightPressed.emit(yy//self.pixSize, xx//self.pixSize)
            self.update()
    
    def mouseReleaseEvent(self, e):
        #每个标签的鼠标事件发射给槽的都是自身的坐标
        #所以获取释放点相对本标签的偏移量，矫正发射的信号
        # print('抬起位置{}, {}'.format(xx, yy))
        if not self.game.isreplaying() and not self.game.settings['instantclick']:
            xx = int(e.localPos().x())
            yy = int(e.localPos().y())
            if self.leftAndRightClicked:
                self.leftAndRightRelease.emit(yy//self.pixSize, xx//self.pixSize)
                self.leftAndRightClicked=False
            else:
                if e.button () == QtCore.Qt.LeftButton:
                    self.leftRelease.emit(yy//self.pixSize, xx//self.pixSize)
                elif e.button () == QtCore.Qt.RightButton:
                    self.rightRelease.emit(yy//self.pixSize, xx//self.pixSize)
            self.update()

    def mouseMoveEvent(self, e):
        #print('移动位置{}, {}'.format(xx, yy))
        if not self.game.isreplaying():
            xx = int(e.localPos().x())
            yy = int(e.localPos().y())
            if self.game.timeStart==True and self.game.finish==False:
                if self.lastcell!=None:
                    self.game.path+=(((yy-self.lastcell[1])**2+(xx-self.lastcell[0])**2)**0.5)/self.pixSize
                    self.game.addtrack(int(100*yy/self.pixSize),int(100*xx/self.pixSize))
                self.lastcell=(xx,yy)
            self.mouseMove.emit (yy//self.pixSize, xx//self.pixSize)
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        size=self.pixSize
        if self.game.isreplaying():
            mouse=(self.game.cursorplace[0]//100,self.game.cursorplace[1]//100)
        else:
            index=self.game.oldCell
            r=self.game.getrow(index)
            c=self.game.getcolumn(index)
            mouse=(r,c)
        for i in range(self.game.row):
            for j in range(self.game.column):
                index=self.game.pixmapindex[i*self.game.column+j]
                painter.drawPixmap(j*size,i*size,self.pixmaps[index])
        for i in self.game.rowRange(mouse[0] - 1, mouse[0]+ 2):
            for j in self.game.columnRange(mouse[1] - 1, mouse[1]+ 2):
                index=self.getPixmapIndex(i,j,mouse)
                if index!=None:
                    painter.drawPixmap(j*size,i*size,self.pixmaps[index])
        if self.game.isreplaying():
            painter.drawPixmap(self.game.cursorplace[1]*size//100,self.game.cursorplace[0]*size//100,self.pixmaps[16])
        elif self.game.isnggame() and not self.game.timeStart:
            if self.game.startcross!=None:
                painter.drawPixmap(self.game.startcross[0]*size,self.game.startcross[1]*size,self.pixmaps[15])
        safesquares=self.game.row*self.game.column-self.game.mineNum-self.game.status.count(1)
        if safesquares==1 and not self.game.isreplaying() and not self.game.finish:
            mb=None
            for square in range(self.game.row*self.game.column):
                if self.game.isCovered(square) and not self.game.isMine(square):
                    mb=square
                    break
            if mb!=None:
                #dis=((mouse[0]-self.game.getrow(mb)-0.5)**2+(mouse[1]-self.game.getcolumn(mb)-0.5)**2)**0.5
                #diag=(self.game.row**2+self.game.column**2)**0.5
                #if dis>0.25*diag:
                hints=self.game.adjacent1(mb)
                for grid in hints:
                    if self.game.isOpened(grid):
                        painter.drawPixmap(self.game.getcolumn(grid)*size,self.game.getrow(grid)*size,self.pixmaps[17])
        painter.end()
        
    def getPixmapIndex(self,i,j,mouse):
        index=self.game.getindex(i,j)
        if self.game.isCovered(index) and self.game.leftAndRightHeld and smallfuc.linyu(i,j,mouse[0],mouse[1]) and not self.game.mouseout:
            return 0
        elif self.game.isCovered(index) and self.game.leftHeld and i==mouse[0] and j==mouse[1] and not self.game.mouseout:
            return 0

    


                

