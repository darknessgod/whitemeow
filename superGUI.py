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

        
        self.initui(MainWindow)
        self.initmenu(MainWindow)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
       
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_("Meowsweeper Arbiter"))
        self.menu.setTitle(_("Game"))
        self.menu_P.setTitle(_("Options"))
        self.menu_H.setTitle(_("Help"))
        self.action_gridsize.setText(_("Current size:"))
        self.action_gridup.setText(_("Zoom in"))
        self.action_griddown.setText(_("Zoom out"))
        self.action.setText(_("New game"))
        self.action_re.setText(_("Restart game"))
        self.action_saveboard.setText(_("Save board"))
        self.action_savereplay.setText(_("Save replay"))
        self.action_loadreplay.setText(_("Load replay"))
        self.action_loadboard.setText(_("Load board"))
        self.action_record.setText(_("Best scores"))
        self.action_B.setText(_("Beginner"))
        self.action_I.setText(_("Intermediate"))
        self.action_E.setText(_("Expert"))
        self.action_C.setText(_("Custom"))
        self.action_X_2.setText(_("Exit"))
        self.action_counter.setText(_("Counter"))
        self.action_settings.setText(_("Settings"))

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
        self.frame1and2 = QtWidgets.QFrame(self.centralwidget)  
        self.frame1and2.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame1and2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame1and2.setLineWidth(5)
        self.frame1and2.setMidLineWidth(5)
        self.frame1and2.setContentsMargins(5,5,5,5)
        self.frame1and2.setStyleSheet("background-color:#C0C0C0;")
        self.halfverticalLayout=QtWidgets.QVBoxLayout(self.frame1and2)
        self.initialupperframe()#初始化顶端状态栏，即self.frame
        self.halfverticalLayout.addWidget(self.frame) 
        self.initialminearea()#初始化雷区，即self.frame_2
        self.halfverticalLayout.addWidget(self.frame_2)
        self.halfverticalLayout.setContentsMargins(5,5,5,5)
        self.verticalLayout.addWidget(self.frame1and2)
        self.verticalLayout.setSpacing(0)
        self.initialbottomframe()#初始化底端，即self.frame_3
        #self.scroll = QtWidgets.QScrollArea()
        #self.scroll.setWidget(self.frame_2)
        self.verticalLayout.addWidget(self.frame_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
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
        self.label_2.setFrameShadow(QtWidgets.QFrame.Raised)
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
        self.verticalLayout.setContentsMargins(0,0,0,0)

    def initialupperframe(self):
        self.frame = statusLabel.StatusFrame(self.frame1and2)#QFrame是是基本控件的基类
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.frame.setLineWidth(3)
        self.frame.setMidLineWidth(3)
        self.frame.setContentsMargins(3,3,3,3)
        self.frame.setFixedHeight(48)
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
        self.frame_2 = QtWidgets.QFrame(self.frame1and2)  
        self.frame_2.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_2.setLineWidth(3)
        self.frame_2.setMidLineWidth(3)
        self.frame_2.setContentsMargins(3,3,3,3)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
    def initialbottomframe(self):
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)  
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout3.setContentsMargins(5, 5, 5, 5)
        self.frame_3.setStyleSheet("background-color:#606060;")
        self.labeltag = QtWidgets.QLabel(self.frame_3)#
        self.labeltag.setObjectName("labeltag")
        self.resetplayertag()
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
        self.action_saveboard = QtWidgets.QAction(MainWindow)
        self.action_saveboard.setCheckable(False)
        self.action_saveboard.setObjectName("action_loadboard")
        self.action_saveboard.setShortcut(QtGui.QKeySequence("S"))
        self.action_saveboard.setEnabled(False)
        self.action_loadboard = QtWidgets.QAction(MainWindow)
        self.action_loadboard.setCheckable(False)
        self.action_loadboard.setObjectName("action_loadboard")
        self.action_loadboard.setShortcut(QtGui.QKeySequence("L"))
        self.action_loadboard.setEnabled(True)
        self.action_savereplay = QtWidgets.QAction(MainWindow)
        self.action_savereplay.setCheckable(False)
        self.action_savereplay.setObjectName("action_savereplay")
        self.action_savereplay.setShortcut(QtGui.QKeySequence("F11"))
        self.action_savereplay.setEnabled(False)
        self.action_loadreplay = QtWidgets.QAction(MainWindow)
        self.action_loadreplay.setCheckable(False)
        self.action_loadreplay.setObjectName("action_loadreplay")
        self.action_loadreplay.setShortcut(QtGui.QKeySequence("F4"))
        self.action_loadreplay.setEnabled(True)
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
        self.action_record = QtWidgets.QAction(MainWindow)
        self.action_record.setCheckable(False)
        self.action_record.setObjectName("action_C")
        self.action_record.setShortcut(QtGui.QKeySequence("B"))
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
        self.menu.addAction(self.action_saveboard)
        self.menu.addAction(self.action_loadboard)
        self.menu.addAction(self.action_savereplay)
        self.menu.addAction(self.action_loadreplay)
        self.menu.addSeparator()
        self.menu.addAction(self.action_B)
        self.menu.addAction(self.action_I)
        self.menu.addAction(self.action_E)
        self.menu.addAction(self.action_C)
        self.menu.addSeparator()
        self.menu.addAction(self.action_record)
        self.menu.addSeparator()
        self.menu.addAction(self.action_X_2)
        self.menu_P.addAction(self.action_settings)
        self.menu_P.addSeparator()
        self.menu_P.addAction(self.action_gridsize)
        self.menu_P.addAction(self.action_gridup)
        self.menu_P.addAction(self.action_griddown)
        self.menu_P.addSeparator()
        self.menu_P.addAction(self.action_counter)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_P.menuAction())
        self.menubar.addAction(self.menu_H.menuAction())

    def getdata(self):
        self.datas=readdata.readdata()
        self.datas.readstats()
        self.datas.getrecords()
        self.options=readdata.readsettings()
        self.options.readsettings()
        
    def resetplayertag(self):
        if self.options.settings['showplayertag']==True:
            self.labeltag.setText(self.options.settings['defaultplayertag'])
        else:
            self.labeltag.setText(' ')