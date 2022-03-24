from PyQt5 import QtCore, QtGui, QtWidgets

class news_Dialog (object):
    def __init__(self,geo,breakrecord,style):
        self.breakrecord=[*breakrecord]
        self.geo=geo
        self.style=style
        self.Dialog = QtWidgets.QDialog ()
        self.setupui()
        self.okbutton.clicked.connect(self.Dialog.close)

    def setupui(self):
        self.Dialog.move(self.geo[0]+self.geo[2]//2-150,self.geo[1]+self.geo[3]//2-80)
        self.Dialog.setFixedSize(300,160)
        self.Dialog.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.label = QtWidgets.QLabel (self.Dialog)
        self.label.setObjectName ("label")
        self.label.setFixedSize(260,80)
        self.label.move(20,20)
        text='恭喜打破:\n%s '%(self.style)
        textlist=['Time,','3bv/s,','QG,','RQP,','IOE']
        for i in range(len(textlist)):
            if self.breakrecord[i]==1:
                text+=textlist[i]
        if text[-1]==',':
            text=list(text)
            text.pop()
            tmpstr=""
            text=tmpstr.join(text)
        text+='成绩！'
        self.label.setText(text)
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignTop)
        self.label.setStyleSheet("font-size:18px;font-family:YF补 汉仪夏日体;")
        self.okbutton = QtWidgets.QPushButton (self.Dialog)
        self.okbutton.setObjectName ("okbutton")
        self.okbutton.setFixedSize(130,30)
        self.okbutton.move(85,115)
        self.okbutton.setText('OK')




