# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selfDefinedParameter.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog (object):
    def __init__(self, row, column, num):
        self.row = row
        self.column = column
        self.mineNum = num
        self.alter = False
        self.Dialog = QtWidgets.QDialog ()
        self.setupUi ()
        self.setParameter ()
        self.Dialog.setWindowIcon (QtGui.QIcon ("media/mine.ico"))
        self.pushButton.clicked.connect (self.processParameter)
        self.pushButton_2.clicked.connect (self.Dialog.close)

    def setupUi(self):
        self.Dialog.setObjectName ("Dialog")
        self.Dialog.setFixedSize (307, 108)
        self.horizontalLayout = QtWidgets.QHBoxLayout (self.Dialog)
        self.horizontalLayout.setObjectName ("horizontalLayout")
        self.widget = QtWidgets.QWidget (self.Dialog)
        self.widget.setObjectName ("widget")
        self.gridLayout = QtWidgets.QGridLayout (self.widget)
        self.gridLayout.setObjectName ("gridLayout")
        self.label = QtWidgets.QLabel (self.widget)
        self.label.setObjectName ("label")
        self.gridLayout.addWidget (self.label, 0, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox (self.widget)
        self.spinBox.setAlignment (QtCore.Qt.AlignCenter)
        self.spinBox.setMinimum (4)
        self.spinBox.setMaximum (80)
        self.spinBox.setProperty ("value", 8)
        self.spinBox.setObjectName ("spinBox")
        self.gridLayout.addWidget (self.spinBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel (self.widget)
        self.label_2.setObjectName ("label_2")
        self.gridLayout.addWidget (self.label_2, 1, 0, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox (self.widget)
        self.spinBox_2.setAlignment (QtCore.Qt.AlignCenter)
        self.spinBox_2.setMinimum (4)
        self.spinBox_2.setMaximum (80)
        self.spinBox_2.setObjectName ("spinBox_2")
        self.gridLayout.addWidget (self.spinBox_2, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel (self.widget)
        self.label_3.setObjectName ("label_3")
        self.gridLayout.addWidget (self.label_3, 2, 0, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox (self.widget)
        self.spinBox_3.setAlignment (QtCore.Qt.AlignCenter)
        self.spinBox_3.setMinimum (1)
        self.spinBox_3.setMaximum (999)
        self.spinBox_3.setObjectName ("spinBox_3")
        self.gridLayout.addWidget (self.spinBox_3, 2, 1, 1, 1)
        self.horizontalLayout.addWidget (self.widget)
        self.widget_2 = QtWidgets.QWidget (self.Dialog)
        self.widget_2.setObjectName ("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout (self.widget_2)
        self.verticalLayout.setObjectName ("verticalLayout")
        self.pushButton = QtWidgets.QPushButton (self.widget_2)
        self.pushButton.setObjectName ("pushButton")
        self.verticalLayout.addWidget (self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton (self.widget_2)
        self.pushButton_2.setObjectName ("pushButton_2")
        self.verticalLayout.addWidget (self.pushButton_2)
        self.horizontalLayout.addWidget (self.widget_2)

        self.retranslateUi ()
        QtCore.QMetaObject.connectSlotsByName (self.Dialog)
        self.setParameter ()

    def retranslateUi(self):
        self.Dialog.setWindowTitle (_("参数设置"))
        self.label.setText (_("行数"))
        self.label_2.setText (_("列数"))
        self.label_3.setText (_("雷数"))
        self.pushButton.setText (_("确定"))
        self.pushButton_2.setText (_("取消"))

    def setParameter(self):
        self.spinBox.setValue (self.row)
        self.spinBox_2.setValue (self.column)
        self.spinBox_3.setValue (self.mineNum)

    def processParameter(self):
        r = self.spinBox.value ()
        c = self.spinBox_2.value ()
        n = self.spinBox_3.value ()
        if r != self.row or c != self.column or n != self.mineNum:
            self.alter = True
            self.row = r
            self.column = c
            self.mineNum = min (max (n, 4), r*c//2)
        self.Dialog.close ()
