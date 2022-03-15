from PyQt5 import QtCore, QtGui, QtWidgets
import sys
class Counter(object):
    def __init__(self,counterWindow):
        counterWindow.setWindowTitle("计数器") 
        counterWindow.setEnabled(True)
        counterWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        columnwidth=[90,90]
        self.lineheight=18
        self.rowsnames=['RTime','Est time','3BV','3BV/s','QG','RQP','Ops','Isls','LRD','Flags','Cl','Ce','IOE','Corr','ThrP']
        sumheight=self.lineheight*len(self.rowsnames)
        counterWindow.resize(sum(columnwidth), sumheight)
        self.titlelabelarray=[0]*len(self.rowsnames)
        self.valuelabelarray=[0]*len(self.rowsnames)
        #gridlayout= QtWidgets.QGridLayout()
        #counterWindow.setLayout(gridlayout)
        for i in range(len(self.rowsnames)):
            self.titlelabelarray[i]=QtWidgets.QLabel(counterWindow)
            self.titlelabelarray[i].resize=(columnwidth[0],self.lineheight)
            self.titlelabelarray[i].setText(' %s'%(self.rowsnames[i]))
            self.titlelabelarray[i].setAlignment(QtCore.Qt.AlignLeft)
            #titlelabelarray[i].setFrameShadow(QtWidgets.QFrame.Raised)
            #titlelabelarray[i].setStyleSheet('border-width: 1px;border-color: rgb(255, 255, 255)')
            self.titlelabelarray[i].move(0,self.lineheight*i)
            self.valuelabelarray[i]=QtWidgets.QLabel(counterWindow)
            self.valuelabelarray[i].resize=(columnwidth[1],self.lineheight)
            self.valuelabelarray[i].setText('0')
            self.valuelabelarray[i].setAlignment(QtCore.Qt.AlignLeft)
            #valuelabelarray[i].setFrameShadow(QtWidgets.QFrame.Raised)
            #valuelabelarray[i].setStyleSheet('border-width: 1px;border-color: rgb(255, 255, 255)')
            self.valuelabelarray[i].move(columnwidth[0],self.lineheight*i)


                    
                
                
        
       
    
        
        
            
