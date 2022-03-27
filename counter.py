from PyQt5 import QtCore, QtGui, QtWidgets
import sys
class Counter(object):
    def __init__(self,counterWindow,game):
        self.game=game
        counterWindow.setWindowTitle("计数器") 
        counterWindow.setEnabled(True)
        counterWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        counterWindow.setWindowFlags(QtCore.Qt.Drawer)
        self.columnwidth=[90,90]
        self.lineheight=18
        self.rowsnames=['RTime','Est time','3BV','3BV/s','QG','RQP','Ops','Isls','LRD','Flags','Cl','Ce','Path','IOE','Corr','ThrP','Games','Ranks']
        sumheight=self.lineheight*len(self.rowsnames)
        counterWindow.setFixedSize(sum(self.columnwidth), sumheight)
        self.titlelabelarray=[0]*len(self.rowsnames)
        self.valuelabelarray=[0]*len(self.rowsnames)
        #gridlayout= QtWidgets.QGridLayout()
        #counterWindow.setLayout(gridlayout)
        for i in range(len(self.rowsnames)):
            self.titlelabelarray[i]=QtWidgets.QLabel(counterWindow)
            self.titlelabelarray[i].resize=(self.columnwidth[0],self.lineheight)
            self.titlelabelarray[i].setText(' %s'%(self.rowsnames[i]))
            self.titlelabelarray[i].setAlignment(QtCore.Qt.AlignLeft)
#            self.titlelabelarray[i].setStyleSheet("font-size:12px;font-family:YF补 汉仪夏日体;")
            #titlelabelarray[i].setFrameShadow(QtWidgets.QFrame.Raised)
            #titlelabelarray[i].setStyleSheet('border-width: 1px;border-color: rgb(255, 255, 255)')
            self.titlelabelarray[i].move(0,self.lineheight*i)
            self.valuelabelarray[i]=QtWidgets.QLabel(counterWindow)
            self.valuelabelarray[i].resize=(self.columnwidth[1],self.lineheight)
            self.valuelabelarray[i].setText('0')
            self.valuelabelarray[i].setAlignment(QtCore.Qt.AlignLeft)
            #self.valuelabelarray[i].setStyleSheet("font-size:12px;")
            #valuelabelarray[i].setFrameShadow(QtWidgets.QFrame.Raised)
            #valuelabelarray[i].setStyleSheet('border-width: 1px;border-color: rgb(255, 255, 255)')
            self.valuelabelarray[i].move(self.columnwidth[0],self.lineheight*i)

    def refreshvalues(self,status):
        allclicks=sum(self.game.allclicks[0:3])
        eclicks=sum(self.game.eclicks)
        if status==2:
            rt=self.game.intervaltime
            allbv=int(self.game.bbbv)
            solvedbv=int(self.game.solvedbbbv)
            if eclicks==0:
                ioe,corr,thrp=0,0,0
            else:
                ioe,corr,thrp=solvedbv/allclicks,eclicks/allclicks,solvedbv/eclicks
            if solvedbv==0:
                est=999.99
            else:
                est=rt/(solvedbv+2*self.game.solvedops)*(allbv+2*self.game.ops)
            values=['%.2f'%(rt),'%.2f'%(est),'%d/%d'%(solvedbv,allbv),'%.3f'%(solvedbv/rt),'%.3f'%(pow(est,1.7)/allbv)]
            values+=['%.2f'%(est*(est+1)/allbv),'%d/%d'%(self.game.solvedops,self.game.ops),'%d/%d'%(self.game.solvedislands,self.game.islands)]
            values+=['%d/%d/%d'%(self.game.allclicks[0],self.game.allclicks[1],self.game.allclicks[2])]
            values+=['%d'%(self.game.allclicks[3])]
            values+=['%d@%.3f'%(allclicks,allclicks/rt)]
            values+=['%d@%.3f'%(eclicks,eclicks/rt)]
            values+=['%.1f'%(self.game.path)]
            values+=['%.3f'%(ioe),'%.3f'%(corr),'%.3f'%(thrp)]
            values+=['%d'%(self.game.gamenum),'%d/%d/%d'%(self.game.ranks[0],self.game.ranks[1],self.game.ranks[2])]
            for i in range(len(self.valuelabelarray)):
                self.valuelabelarray[i].setText(values[i])
        elif status==1:
            rt=max(float('%.2f'%(self.game.intervaltime-0.005)),0.00)
            allbv='-'
            if eclicks==0:
                corr=0
            else:
                corr=eclicks/allclicks
            if rt==0:
                cls='-'
                ces='-'
            else:
                cls='%.3f'%(float(allclicks/rt))
                ces='%.3f'%(float(eclicks/rt))
            values=['%.2f'%(rt),'-','-','-','-','-','-','-']
            values+=['%d/%d/%d'%(self.game.allclicks[0],self.game.allclicks[1],self.game.allclicks[2])]
            values+=['%d'%(self.game.allclicks[3])]
            values+=['%d@%s'%(allclicks,cls)]
            values+=['%d@%s'%(eclicks,ces)]
            values+=['%.1f'%(self.game.path)]
            values+=['%s'%('-'),'%.3f'%(corr),'%s'%('-')]
            values+=['%d'%(self.game.gamenum),'-/-/-']
            for i in range(len(self.valuelabelarray)):
                self.valuelabelarray[i].setText(values[i])


                    
                
                
        
       
    
        
        
            
