from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import mainWindowGUI 
import mineSweeperGUI

if __name__ == "__main__":
    app = QtWidgets.QApplication (sys.argv)
#    app.aboutToQuit.connect(app.deleteLater)
    MainWindow = mainWindowGUI.MainWindow ()
    ui = mineSweeperGUI.MineSweeperGUI (MainWindow)
    MainWindow.show()
    #ui.counterWindow.close()
    sys.exit(app.exec_())
    #app.exec_()
    #QtCore.QCoreApplication.instance().quit

