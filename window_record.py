from PyQt5 import QtCore, QtGui, QtWidgets


class ui_recorddialog (object):
    def __init__(self,geo,record):
        self.record=[*record]
        self.geo=geo
        self.levelnum=3
        self.typenum=5
        self.Dialog = QtWidgets.QDialog ()
        self.setupui()
        self.allbutton.clicked.connect(self.showall)
        self.flbutton.clicked.connect(self.showfl)
        self.nfbutton.clicked.connect(self.shownf)

    def setupui(self):
        self.Dialog.setWindowTitle(_("Best scores"))
        self.Dialog.move(self.geo[0]+self.geo[2]//2-145,self.geo[1]+self.geo[3]//2-82)
        self.Dialog.setFixedSize(410,165)
        self.Dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.Dialog.setWindowIcon(QtGui.QIcon("media/mine.ico"))
        self.gridLayout = QtWidgets.QGridLayout(self.Dialog)
        self.allbutton = QtWidgets.QPushButton (self.Dialog)
        self.flbutton = QtWidgets.QPushButton (self.Dialog)
        self.nfbutton = QtWidgets.QPushButton (self.Dialog)
        buttons=[self.allbutton,self.flbutton,self.nfbutton]
        buttonstext=[_('Overall'),_('Flagging'),_('No-flagging')]
        for i in range(self.levelnum):
            buttons[i].setFixedSize(60,25)
            buttons[i].setText('%s'%(buttonstext[i]))
            buttons[i].setStyleSheet("font-size:14px;font-family:YF补 汉仪夏日体;")
            self.gridLayout.addWidget(buttons[i],0,i)
        recordtext=['Time','3bv/s','QG','RQP','IOE']
        for i in range(self.typenum):
            label =QtWidgets.QLabel (self.Dialog)
            label.setFixedSize(60,25)
            label.setText('%s'%(recordtext[i]))
            label.setAlignment (QtCore.Qt.AlignCenter)
            label.setStyleSheet("font-size:14px;font-family:YF补 汉仪夏日体;")
            self.gridLayout.addWidget(label,1,i+1)
        leveltext=[_('Beg'),_('Int'),_('Exp')]
        for j in range(self.levelnum):
            label =QtWidgets.QLabel (self.Dialog)
            label.setFixedSize(60,25)
            label.setText('%s'%(leveltext[j]))
            label.setAlignment (QtCore.Qt.AlignCenter)
            label.setStyleSheet("font-size:14px;font-family:YF补 汉仪夏日体;")
            self.gridLayout.addWidget(label,j+2,0)
        self.textlabels=[0]*(self.typenum*self.levelnum)
        for i in range(self.typenum):
            for j in range(self.levelnum):
                label =QtWidgets.QLabel (self.Dialog)
                label.setFixedSize(60,25)
                label.setAlignment (QtCore.Qt.AlignCenter)
                label.setStyleSheet("font-size:14px;font-family:YF补 汉仪夏日体;")
                self.gridLayout.addWidget(label,j+2,i+1)
                self.textlabels[i*self.levelnum+j]=label
        self.showall()

    def showall(self):
        self.showscore(0)

    def showfl(self):
        self.showscore(1)

    def shownf(self):
        self.showscore(2)

    def showscore(self,num):
        decimals=[2,3,3,3,3]
        for i in range(self.typenum):
            if i in [0,2,3]:
                direction=True
            else:
                direction=False
            for j in range(self.levelnum):
                if num==0:
                    if direction==True:
                        value=min(self.record[j][i],self.record[j+self.levelnum][i])
                    else:
                        value=max(self.record[j][i],self.record[j+self.levelnum][i])
                else:
                    value=self.record[j+(num-1)*self.levelnum][i]
                value=format(value,'.%df'%(decimals[i]))
                self.textlabels[i*self.levelnum+j].setText('%s'%(value))
                

