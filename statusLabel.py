from PyQt5 import QtWidgets, QtCore

class StatusLabel (QtWidgets.QLabel):
    leftRelease = QtCore.pyqtSignal ()  # 定义信号

    def __init__(self, parent=None):
        super (StatusLabel, self).__init__ (parent)
        self.setFrameShape (QtWidgets.QFrame.Panel)
        self.setFrameShadow (QtWidgets.QFrame.Raised)
        self.setLineWidth(1)
        self.setAlignment (QtCore.Qt.AlignCenter)

    def mousePressEvent(self, e):  ##重载一下鼠标点击事件
        if e.button () == QtCore.Qt.LeftButton:
            self.setFrameShadow (QtWidgets.QFrame.Sunken)

    def mouseReleaseEvent(self, e):
        if e.button () == QtCore.Qt.LeftButton:
            self.setFrameShadow (QtWidgets.QFrame.Raised)
            xx = int(e.localPos().x())
            yy = int(e.localPos().y())
            if xx<0 or xx>self.width() or yy<0 or yy>self.height():
                pass
            else:   
                self.leftRelease.emit ()

class menuLabel (QtWidgets.QLabel):
    leftRelease = QtCore.pyqtSignal (int)  # 定义信号

    def __init__(self, parent=None):
        super (menuLabel, self).__init__ (parent)
        self.setFrameShape (QtWidgets.QFrame.Panel)
        self.setFrameShadow (QtWidgets.QFrame.Raised)
        self.setLineWidth(1)
        self.setAlignment (QtCore.Qt.AlignCenter)
        self.menunum=0

    def mousePressEvent(self, e):  ##重载一下鼠标点击事件
        if e.button () == QtCore.Qt.LeftButton:
            self.setFrameShadow (QtWidgets.QFrame.Sunken)

    def mouseReleaseEvent(self, e):
        if e.button () == QtCore.Qt.LeftButton:
            self.setFrameShadow (QtWidgets.QFrame.Raised)
            xx = int(e.localPos().x())
            yy = int(e.localPos().y())
            if xx<0 or xx>self.width() or yy<0 or yy>self.height():
                pass
            else:   
                self.leftRelease.emit (self.menunum)


class StatusFrame (QtWidgets.QFrame):
    leftRelease = QtCore.pyqtSignal ()  # 定义信号

    def __init__(self, parent=None):
        super (StatusFrame, self).__init__ (parent)
        self.setFrameShape (QtWidgets.QFrame.Panel)
        self.setFrameShadow (QtWidgets.QFrame.Raised)
        self.setLineWidth(1)
        #self.setAlignment (QtCore.Qt.AlignCenter)

    def mousePressEvent(self, e):  ##重载一下鼠标点击事件
        if e.button () == QtCore.Qt.LeftButton:
            self.setFrameShadow (QtWidgets.QFrame.Sunken)

    def mouseReleaseEvent(self, e):
        if e.button () == QtCore.Qt.LeftButton:
            self.setFrameShadow (QtWidgets.QFrame.Raised)
            xx = int(e.localPos().x())
            yy = int(e.localPos().y())
            if xx<0 or xx>self.width() or yy<0 or yy>self.height():
                pass
            else:   
                self.leftRelease.emit ()
