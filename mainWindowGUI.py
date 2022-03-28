from PyQt5 import QtCore, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    closeEvent_ = QtCore.pyqtSignal()

    def closeEvent(self, event):
        QtCore.QCoreApplication.instance().quit
        self.closeEvent_.emit()
