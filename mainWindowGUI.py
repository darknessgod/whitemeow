from PyQt5 import QtCore, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
  
    closeEvent_ = QtCore.pyqtSignal()
    gridupdownEvent = QtCore.pyqtSignal(int)
    ctrlpressEvent= QtCore.pyqtSignal()
    ctrlreleaseEvent= QtCore.pyqtSignal()
  
    def closeEvent(self, event):
  
        QtCore.QCoreApplication.instance().quit
  
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



