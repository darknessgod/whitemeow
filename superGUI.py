# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'superGUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import statusLabel
import readdata

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        self.getdata()
        self.initui(MainWindow)
        self.initmenu(MainWindow)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
       

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Meowsweeper Arbiter"))
        self.menu.setTitle(_translate("MainWindow", "游戏"))
        self.menu_P.setTitle(_translate("MainWindow", "选项"))
        self.menu_H.setTitle(_translate("MainWindow", "这是啥"))
        self.action_gridsize.setText(_translate("MainWindow", "当前尺寸："))
        self.action_gridup.setText(_translate("MainWindow", "放大"))
        self.action_griddown.setText(_translate("MainWindow", "缩小"))
        self.action.setText(_translate("MainWindow", "新游戏"))
        self.action_re.setText(_translate("MainWindow", "重玩"))
        self.action_B.setText(_translate("MainWindow", "初级"))
        self.action_I.setText(_translate("MainWindow", "中级"))
        self.action_E.setText(_translate("MainWindow", "高级"))
        self.action_C.setText(_translate("MainWindow", "自定义"))
        self.action_X_2.setText(_translate("MainWindow", "退出"))
        self.action_counter.setText(_translate("MainWindow", "计数器"))
        self.action_settings.setText(_translate("MainWindow", "设置"))

    def showminenum(self,minenum):
        ledlist=['-','-','-']
        if minenum>=-99 and minenum<0:
            ledlist[0]='-'
            ledlist[1]=str((-minenum)//10)
            ledlist[2]=str((-minenum)%10)
        else:
            ledlist[0]=str(minenum//100)
            ledlist[1]=str((minenum%100)//10)
            ledlist[2]=str((minenum)%10)
        for i in range(len(ledlist)):
            filename='media/LED'
            filename+=ledlist[i]
            filename+='.png'
            pixmap = QtGui.QPixmap(filename)
            size=pixmap.size()
            scaled_pixmap=pixmap.scaled(size/13)
            self.labelmine[i].setPixmap(scaled_pixmap)
            
    def showtimenum(self,intervaltime):
        ledlist=['-','-','-']
        minenum=int(intervaltime+0.9999)
        ledlist[0]=str(minenum//100)
        ledlist[1]=str((minenum%100)//10)
        ledlist[2]=str((minenum)%10)
        for i in range(len(ledlist)):
            filename='media/LED'
            filename+=ledlist[i]
            filename+='.png'
            pixmap = QtGui.QPixmap(filename)
            size=pixmap.size()
            scaled_pixmap=pixmap.scaled(size/13)
            self.labeltime[i].setPixmap(scaled_pixmap)

    def initui(self,MainWindow):
        self.initmainwindow(MainWindow)
        #self.label.setFrameShape(QtWidgets.QFrame.WinPanel)
        #self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.initialupperframe()#初始化顶端状态栏，即self.frame
        self.verticalLayout.addWidget(self.frame) 
        self.initialminearea()#初始化雷区，即self.frame_2
        self.verticalLayout.addWidget(self.frame_2)
        self.verticalLayout.addStretch(1)
        self.initialbottomframe()#初始化底端，即self.frame_3
        #self.scroll = QtWidgets.QScrollArea()
        #self.scroll.setWidget(self.frame_2)
        self.verticalLayout.addWidget(self.frame_3)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        MainWindow.setCentralWidget(self.centralwidget)
        
        
    def initmenu(self,MainWindow):   
        self.createmenulabels(MainWindow) 
        MainWindow.setMenuBar(self.menubar)
        self.setmenuactions(MainWindow)
        self.addactionstomenu()

        #self.statusbar = QtWidgets.QStatusBar(MainWindow)
        #self.statusbar.setObjectName("statusbar")
        #MainWindow.setStatusBar(self.statusbar)

    def initialminenum(self):
        self.labelmine3 = QtWidgets.QLabel(self.frame)#
        self.labelmine3.setObjectName("label33")
        self.horizontalLayout.addWidget(self.labelmine3)
        self.labelmine2 = QtWidgets.QLabel(self.frame)#
        self.labelmine2.setObjectName("label32")
        self.horizontalLayout.addWidget(self.labelmine2)
        self.labelmine1 = QtWidgets.QLabel(self.frame)#
        self.labelmine1.setObjectName("label31")
        self.horizontalLayout.addWidget(self.labelmine1)
        self.labelmine=[self.labelmine3,self.labelmine2,self.labelmine1]

    def initialface(self):
        self.label_2 = statusLabel.StatusLabel(self.frame)#label2是脸
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)

    def initialtimer(self):
        self.labeltime3 = QtWidgets.QLabel(self.frame)#
        self.labeltime3.setObjectName("label33")
        self.horizontalLayout.addWidget(self.labeltime3)
        self.labeltime2 = QtWidgets.QLabel(self.frame)#
        self.labeltime2.setObjectName("label32")
        self.horizontalLayout.addWidget(self.labeltime2)
        self.labeltime1 = QtWidgets.QLabel(self.frame)#
        self.labeltime1.setObjectName("label31")
        self.horizontalLayout.addWidget(self.labeltime1)
        self.labeltime=[self.labeltime3,self.labeltime2,self.labeltime1]

    def initmainwindow(self,MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)  
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)#垂直布局
        self.verticalLayout.setObjectName("verticalLayout")

    def initialupperframe(self):
        self.frame = statusLabel.StatusFrame(self.centralwidget)#QFrame是是基本控件的基类
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)#水平布局
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(1, 5, 1, 5)
        self.horizontalLayout.setSpacing(0)
        self.initialminenum()
        spacerItem = QtWidgets.QSpacerItem(40,20,QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)#弹簧
        self.horizontalLayout.addItem(spacerItem)
        self.initialface()
        spacerItem1 = QtWidgets.QSpacerItem(40,20,QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.initialtimer()

    def initialminearea(self):
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)  #整个局面的框
        self.frame_2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

    def initialbottomframe(self):
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)  
        self.frame_3.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout3.setContentsMargins(0, 0, 0, 0)
        self.labeltag = QtWidgets.QLabel(self.frame_3)#
        self.labeltag.setObjectName("labeltag")
        self.labeltag.setText('fairy')
        self.labeltag.setAlignment(QtCore.Qt.AlignCenter)
        self.labeltag.setFixedHeight(22)
        self.labeltag.setStyleSheet("background-color:white;font-size:16px;font-family:YF补 汉仪夏日体;")
        self.horizontalLayout3.addWidget(self.labeltag)

    def createmenulabels(self,MainWindow):
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_P = QtWidgets.QMenu(self.menubar)
        self.menu_P.setObjectName("menu_P")
        self.menu_H = QtWidgets.QMenu(self.menubar)
        self.menu_H.setObjectName("menu_H")
        
    def setmenuactions(self,MainWindow):
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setCheckable(False)
        self.action.setChecked(False)
        self.action.setObjectName("action")
        self.action.setShortcut(QtGui.QKeySequence("Space"))
        self.action_re = QtWidgets.QAction(MainWindow)
        self.action_re.setCheckable(False)
        self.action_re.setChecked(False)
        self.action_re.setObjectName("action")
        self.action_re.setShortcut(QtGui.QKeySequence("R"))
        self.action_B = QtWidgets.QAction(MainWindow)
        self.action_B.setCheckable(True)
        self.action_B.setObjectName("action_B")
        self.action_B.setShortcut(QtGui.QKeySequence("1"))
        self.action_E = QtWidgets.QAction(MainWindow)
        self.action_E.setCheckable(True)
        self.action_E.setObjectName("action_E")
        self.action_E.setShortcut(QtGui.QKeySequence("3"))
        self.action_C = QtWidgets.QAction(MainWindow)
        self.action_C.setCheckable(True)
        self.action_C.setObjectName("action_C")
        self.action_C.setShortcut(QtGui.QKeySequence("4"))
        self.action_X_2 = QtWidgets.QAction(MainWindow)
        self.action_X_2.setObjectName("action_X_2")
        self.action_X_2.setShortcut(QtGui.QKeySequence("Escape"))
        self.action_I = QtWidgets.QAction(MainWindow)
        self.action_I.setCheckable(True)
        self.action_I.setObjectName("action_I")
        self.action_I.setShortcut(QtGui.QKeySequence("2"))
        self.action_settings = QtWidgets.QAction(MainWindow)
        self.action_settings.setCheckable(False)
        self.action_settings.setObjectName("action_settings")
        self.action_settings.setShortcut(QtGui.QKeySequence("F5"))
        self.action_gridup = QtWidgets.QAction(MainWindow)
        self.action_gridup.setCheckable(False)
        self.action_gridup.setObjectName("action_gridup")
        self.action_gridup.setShortcut(QtGui.QKeySequence("+"))
        self.action_griddown = QtWidgets.QAction(MainWindow)
        self.action_griddown.setCheckable(False)
        self.action_griddown.setObjectName("action_griddown")
        self.action_griddown.setShortcut(QtGui.QKeySequence("-"))
        self.action_gridsize = QtWidgets.QAction(MainWindow)
        self.action_gridsize.setEnabled(False)
        self.action_gridsize.setObjectName("action_gridsize")
        self.action_counter = QtWidgets.QAction(MainWindow)
        self.action_counter.setCheckable(False)
        self.action_counter.setObjectName("action_counter")
        self.action_counter.setShortcut(QtGui.QKeySequence("C"))

    def addactionstomenu(self):
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_re)
        self.menu.addSeparator()
        self.menu.addAction(self.action_B)
        self.menu.addAction(self.action_I)
        self.menu.addAction(self.action_E)
        self.menu.addAction(self.action_C)
        self.menu.addSeparator()
        self.menu.addAction(self.action_counter)
        self.menu.addSeparator()
        self.menu.addAction(self.action_X_2)
        self.menu_P.addAction(self.action_settings)
        self.menu_P.addSeparator()
        self.menu_P.addAction(self.action_gridsize)
        self.menu_P.addAction(self.action_gridup)
        self.menu_P.addAction(self.action_griddown)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_P.menuAction())
        self.menubar.addAction(self.menu_H.menuAction())

    def getdata(self):
        self.datas=readdata.readdata()
        self.datas.readstats()
        self.datas.getrecords()