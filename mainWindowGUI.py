from PyQt5 import QtCore, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
  
    closeEvent_ = QtCore.pyqtSignal()
    gridupdownEvent = QtCore.pyqtSignal(int)
    ctrlpressEvent= QtCore.pyqtSignal()
    ctrlreleaseEvent= QtCore.pyqtSignal()
    minbackEvent= QtCore.pyqtSignal()
  
    def closeEvent(self, event):
  
  
        self.closeEvent_.emit()

    def wheelEvent(self, event):

            angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
            angleY = -angle.y()
            self.gridupdownEvent.emit(angleY)

    def keyPressEvent(self, event):
        if(event.key() == QtCore.Qt.Key_Control):
            self.ctrlpressEvent.emit()

    def keyReleaseEvent(self, event):
        if(event.key() == QtCore.Qt.Key_Control):
            self.ctrlreleaseEvent.emit()

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                self.closeEvent_.emit()
            else:
                self.minbackEvent.emit()
    

class meowcounter(QtWidgets.QMainWindow):

    closeEvent2 = QtCore.pyqtSignal()

    def closeEvent(self, event):
        self.closeEvent2.emit()