# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selfDefinedParameter.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import statusLabel
import copy


class Ui_SettingDialog (object):
    def __init__(self,window,options):
        self.Dialog = window
        self.options=options
        self.tmpsettings=copy.deepcopy(self.options.settings)
        self.setupUi ()
        self.Dialog.setWindowIcon (QtGui.QIcon ("media/mine.ico"))
        self.pushButton1.clicked.connect (self.Dialog.close)
        self.pushButton2.clicked.connect (self.Dialog.close)
        self.pushButton3.clicked.connect (self.Dialog.close)
        self.pushButton4.clicked.connect (self.savesettings)
        self.Dialog.closeEvent3.connect(self.closesettings)
        #self.pushButton.clicked.connect (self.processParameter)
        #self.pushButton_2.clicked.connect (self.Dialog.close)

    def setupUi(self):
        self.Dialog.setObjectName ("settings")
        self.Dialog.setFixedSize (600, 400)
        self.Dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.verticalLayout = QtWidgets.QVBoxLayout (self.Dialog)
        self.verticalLayout.setObjectName ("verticalLayout")
        self.widget = QtWidgets.QWidget (self.Dialog)
        self.widget.setObjectName ("widget")#主体部分，构成除去几个按钮以外的整个上半部分
        self.horizontalLayout2 = self.horizontalLayout = QtWidgets.QHBoxLayout (self.widget)
        self.horizontalLayout2.setObjectName ("horizontalLayout2")
        self.setmenuwidget = QtWidgets.QWidget (self.widget)
        self.setmenuwidget.setObjectName ("setmenuwidget")#主体部分，构成除去几个按钮以外的整个上半部分
        self.setmenuwidget.resize(135,500)
        menunames=['玩家设置','游戏设置','计数器设置']
        self.menulabels=[0]*len(menunames)
        self.verticalLayout2 = QtWidgets.QVBoxLayout (self.setmenuwidget)
        self.verticalLayout2.setObjectName ("verticalLayout2")
        iconlabel=QtWidgets.QLabel(self.setmenuwidget)
        pixmap=QtGui.QPixmap("media/arbiter.png")
        size=pixmap.size()
        scaled_pixmap=pixmap.scaled(size/1)
        iconlabel.setPixmap(scaled_pixmap)
        self.verticalLayout2.addWidget(iconlabel)
        self.verticalLayout2.setSpacing(2)
        for i in range(len(menunames)):
            self.menulabels[i]=statusLabel.StatusLabel(self.setmenuwidget)
            self.menulabels[i].resize=(100,25)
            self.menulabels[i].setText(' %s'%(menunames[i]))
            self.menulabels[i].setAlignment(QtCore.Qt.AlignLeft)
            self.menulabels[i].setStyleSheet("font-size:18px;")
            self.verticalLayout2.addWidget(self.menulabels[i])
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout2.addWidget (self.setmenuwidget)
        self.horizontalLayout2.addStretch(1)
        self.coreframe=QtWidgets.QFrame(self.widget)
        self.coreframe.setObjectName ("coreframe")
        self.coreframe.resize(445,500)
        self.coreframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.coreframe.setFrameShadow(QtWidgets.QFrame.Plain)
        self.verticalLayout3 = self.horizontalLayout = QtWidgets.QVBoxLayout (self.coreframe)
        self.verticalLayout3.setObjectName ("verticalLayout3")
        self.showsettings(0)
        self.verticalLayout3.setSpacing(3)
        self.horizontalLayout2.addWidget (self.coreframe)
        self.horizontalLayout2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.addWidget (self.widget)
        self.verticalLayout.addStretch(1)
        self.widget_2 = QtWidgets.QWidget (self.Dialog)
        self.widget_2.setObjectName ("widget_2")#按钮部分
        self.horizontalLayout = QtWidgets.QHBoxLayout (self.widget_2)
        self.pushButton1 = QtWidgets.QPushButton (self.widget_2)
        self.pushButton1.setObjectName ("pushButton1_resetall")
        self.horizontalLayout.addWidget (self.pushButton1)
        self.pushButton2 = QtWidgets.QPushButton (self.widget_2)
        self.pushButton2.setObjectName ("pushButton2_resetthis")
        self.horizontalLayout.addWidget (self.pushButton2)
        self.pushButton3 = QtWidgets.QPushButton (self.widget_2)
        self.pushButton3.setObjectName ("pushButton3_apply")
        self.horizontalLayout.addWidget (self.pushButton3)
        self.pushButton4 = QtWidgets.QPushButton (self.widget_2)
        self.pushButton4.setObjectName ("pushButton4_reset")
        self.horizontalLayout.addWidget (self.pushButton4)
        self.verticalLayout.addWidget (self.widget_2)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        
        
        self.retranslateUi ()
        #-QtCore.QMetaObject.connectSlotsByName (self.Dialog)
        #self.setParameter ()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle (_translate ("Dialog", "设置"))
        self.pushButton1.setText (_translate ("Dialog", "全部重置"))
        self.pushButton2.setText (_translate ("Dialog", "重置本页"))
        self.pushButton3.setText (_translate ("Dialog", "取消"))
        self.pushButton4.setText (_translate ("Dialog", "确定"))

    def showsettings(self,menunum):
        for i in range(self.verticalLayout3.count()): 
            self.verticalLayout3.itemAt(i).widget().deleteLater()
        self.menulabels[menunum].setStyleSheet("background-color:blue;color:white;font-size:18px;")
        self.titlelabel=QtWidgets.QLabel(self.coreframe)
        self.titlelabel.setFixedSize(400,35)
        self.titlelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titlelabel.setStyleSheet("font-size:22px;")
        self.titlelabel.setFrameShape(QtWidgets.QFrame.Panel)
        self.titlelabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout3.addWidget(self.titlelabel)
        if menunum==0:#0：玩家设置 1：游戏设置 2：计数器设置
            self.titlelabel.setText(' %s'%('玩家设置'))
            self.freshcheckBox=self.createcheckbox(self.coreframe,'显示玩家标识',self.tmpsettings['showplayertag'])
            self.verticalLayout3.addWidget(self.freshcheckBox)
            self.playertag = QtWidgets.QLineEdit(self.coreframe)
            self.playertag.setEnabled(self.freshcheckBox.isChecked())
            self.playertag.setText(self.tmpsettings['defaultplayertag'])
            self.playertag.setMaxLength(30)
            self.verticalLayout3.addWidget(self.playertag)
            self.playernametext = QtWidgets.QLabel(self.coreframe)
            self.playernametext.setText('录像玩家姓名')
            self.verticalLayout3.addWidget(self.playernametext)
            self.playername = QtWidgets.QLineEdit(self.coreframe)
            self.playername.setText(self.tmpsettings['playername'])
            self.verticalLayout3.addWidget(self.playername)
            self.modenametext = QtWidgets.QLabel(self.coreframe)
            self.modenametext.setText('模式名称')
            self.verticalLayout3.addWidget(self.modenametext)
            self.coreframe2=QtWidgets.QFrame(self.widget)
            self.coreframe2.setObjectName ("coreframe2")
            self.horizontalLayout3 = self.horizontalLayout = QtWidgets.QHBoxLayout (self.coreframe2)
            self.horizontalLayout3.setObjectName ("horizontalLayout3")
            self.modenamelabels=[0]*4
            levelnames=(self.tmpsettings['level1name'],self.tmpsettings['level2name'],self.tmpsettings['level3name'],self.tmpsettings['level4name'])
            for i in range(4):
                self.modenamelabels[i] = QtWidgets.QLineEdit(self.coreframe2)
                self.modenamelabels[i].setText(levelnames[i])
                self.horizontalLayout3.addWidget(self.modenamelabels[i])
            self.horizontalLayout3.setSpacing(1)
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout3.addWidget(self.coreframe2)
            self.reccheckBox = self.createcheckbox(self.coreframe,'启用递归双击和快速标雷(推荐)',self.tmpsettings['enablerec'])
            self.verticalLayout3.addWidget(self.reccheckBox)
            
    def createcheckbox(self,widget,text,defaultstate):
        checkbox=QtWidgets.QCheckBox(widget)
        checkbox.setText(text)
        checkbox.setCheckable(True)
        checkbox.setChecked(defaultstate)
        checkbox.stateChanged.connect(self.changesettings)
        return checkbox
        
    def changesettings(self):
        self.tmpsettings['showplayertag']=self.freshcheckBox.isChecked()
        self.playertag.setEnabled(self.freshcheckBox.isChecked())
        self.tmpsettings['enablerec']=self.reccheckBox.isChecked()

    def tmpsavesettings(self):
        self.tmpsettings['showplayertag']=self.freshcheckBox.isChecked()
        self.tmpsettings['enablerec']=self.reccheckBox.isChecked()
        self.tmpsettings['defaultplayertag']=self.playertag.text()
        self.tmpsettings['playername']=self.playername.text()
        self.tmpsettings['level1name']=(self.modenamelabels[0].text())
        self.tmpsettings['level2name']=(self.modenamelabels[1].text())
        self.tmpsettings['level3name']=(self.modenamelabels[2].text())
        self.tmpsettings['level4name']=(self.modenamelabels[3].text())

    def savesettings(self):

        self.tmpsavesettings()
        self.options.settings=copy.deepcopy(self.tmpsettings)
        self.options.writesettings()
        self.Dialog.close()

    def closesettings(self):
        pass



                
                

'''    def processParameter(self):
        r = self.spinBox.value ()
        c = self.spinBox_2.value ()
        n = self.spinBox_3.value ()
        if r != self.row or c != self.column or n != self.mineNum:
            self.alter = True
            self.row = r
            self.column = c
            self.mineNum = min (max (n, 4), r*c//2)
        self.Dialog.close ()'''

    
