from sqlite3 import Row
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPainter,QPixmap

from numpy import row_stack


class mineLabel (QtWidgets.QLabel):
    leftRelease = QtCore.pyqtSignal (int, int)  # 定义信号
    rightRelease = QtCore.pyqtSignal (int, int)
    leftPressed = QtCore.pyqtSignal (int, int)
    rightPressed = QtCore.pyqtSignal (int, int)
    leftAndRightPressed = QtCore.pyqtSignal (int, int)
    leftAndRightRelease = QtCore.pyqtSignal (int, int)
    mouseMove = QtCore.pyqtSignal (int, int)

    def __init__(self, row, column, pixsize, parent=None):
        super (mineLabel, self).__init__ (parent)
        self.leftAndRightClicked = False
        self.pixSize=pixsize
        self.pixmaps=[0]*15
        self.row=row
        self.column=column
        self.num = [[0 for j in range(self.column)] for i in range(self.row)]
        self.status = [[0 for j in range(self.column)] for i in range(self.row)]
        self.pressed = [[0 for j in range(self.column)] for i in range(self.row)]
        self.resizepixmaps(self.pixSize)

    '''def mousePressEvent(self, e):  ##重载一下鼠标点击事件
        if e.buttons () == QtCore.Qt.LeftButton | QtCore.Qt.RightButton:
            self.leftAndRightPressed.emit (self.i, self.j)
            self.leftAndRightClicked = True
        else:
            if e.buttons () == QtCore.Qt.LeftButton:
                self.leftPressed.emit (self.i, self.j)
            elif e.buttons () == QtCore.Qt.RightButton:
                self.rightPressed.emit (self.i, self.j)
                '''
    def resizepixmaps(self,num):
        targetsize=num
        for i in range(1,9):
            pngname="media/svg/cell"
            pngname+=str(i)
            pngname+=".svg"
            self.pixmaps[i]=QPixmap(pngname)
        self.pixmaps[0]=QPixmap("media/svg/celldown.svg")
        self.pixmaps[9]=QPixmap("media/svg/cellup.svg")
        self.pixmaps[10]=QPixmap("media/svg/cellflag.svg")
        self.pixmaps[11]=QPixmap("media/svg/cellmine.svg")
        self.pixmaps[12]=QPixmap("media/svg/falsemine.svg")
        self.pixmaps[13]=QPixmap("media/svg/blast.svg")
        self.pixmaps[14]=QPixmap("media/svg/cellunflagged.svg")
        for i in range(len(self.pixmaps)):
            size=self.pixmaps[i].size()
            self.pixmaps[i]=self.pixmaps[i].scaled(size/(160/targetsize))

    '''def resizepixmaps(self):
        for i in range(1,9):
            pngname="media/1"
            pngname+=str(i)
            pngname+=".png"
            self.pixmaps[i]=QPixmap(pngname)
        self.pixmaps[0]=QPixmap("media/10.png")
        self.pixmaps[9]=QPixmap("media/00.png")
        self.pixmaps[10]=QPixmap("media/03.png")
        self.pixmaps[11]=QPixmap("media/01.png")
        self.pixmaps[12]=QPixmap("media/04.png")
        self.pixmaps[13]=QPixmap("media/02.png")
        self.pixmaps[14]=QPixmap("media/05.png")
        for s in self.pixmaps:
            size=s.size()
            s=s.scaled(size) '''
    
    def mousePressEvent(self, e):  # 重载一下鼠标点击事件
        xx = e.localPos().x()
        yy = e.localPos().y()
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

    '''def mouseReleaseEvent(self, e):
        if self.leftAndRightClicked:
            self.leftAndRightRelease.emit (self.i, self.j)
            self.leftAndRightClicked=False
        else:
            if e.button () == QtCore.Qt.LeftButton:
                self.leftRelease.emit (self.i, self.j)
            elif e.button () == QtCore.Qt.RightButton:
                self.rightRelease.emit (self.i, self.j)'''
    
    def mouseReleaseEvent(self, e):
        #每个标签的鼠标事件发射给槽的都是自身的坐标
        #所以获取释放点相对本标签的偏移量，矫正发射的信号
        xx = e.localPos().x()
        yy = e.localPos().y()
        # print('抬起位置{}, {}'.format(xx, yy))
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

        xx = e.localPos().x()
        yy = e.localPos().y()
        #print('移动位置{}, {}'.format(xx, yy))
        self.mouseMove.emit (yy//self.pixSize, xx//self.pixSize)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        size=self.pixSize
        for i in range(self.row):
            for j in range(self.column):
                painter.drawPixmap(j*size,i*size,getPixmap(i,j))
        painter.end()
        
    def getPixmap(i, j):
        if self.pressed[i][j]>=2:
            return self.pixmaps[pressed+9]
        elif self.pressed[i][j]==1:
            return self.pixmaps[0]
        elif self.status[i][j]==2:
            return self.pixmaps[10]
        elif self.status[i][j]==0:
            return self.pixmaps[9]
        else:
            return self.pixmaps[self.num[i][j]]