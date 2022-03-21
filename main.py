from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import mainWindowGUI 
import mineSweeperGUI


# import sweeper
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




#bug:初级时方块水平间距不是0(√)，点击时笑脸不会张嘴，切换模式时窗口关闭再开
    #计时精度不够(√),踩中的雷不能标成红雷(√)，布雷等算法有待优化(√)，第一下会点到雷(√)
