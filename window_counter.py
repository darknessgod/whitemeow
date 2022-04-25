from PyQt5 import QtCore, QtGui, QtWidgets
import time

class Counter(object):

    preview = QtCore.pyqtSignal()
    def __init__(self,counterWindow,game):
        self.game=game
        self.window=counterWindow
        self.window.setEnabled(True)
        self.window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.window.setWindowFlags(QtCore.Qt.Drawer)
        self.window.closeEvent2.connect(self.closecounter)
        self.window.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.window.customContextMenuRequested.connect(self.create_rightmenu) 
        self.window.setWindowTitle(_("Counter"))
        self.create_rightmenu()
        self.columnwidth=[90,90]
        self.lineheight=18
        self.rowsnames=['RTime','Est time','3BV','3BV/s','QG','RQP','Ops','Isls','LRD','Flags','Cl','Ce','Path','IOE','Corr','ThrP','Games','Ranks']
        sumheight=self.lineheight*len(self.rowsnames)
        self.window.setFixedSize(sum(self.columnwidth), sumheight+10)
        self.titlelabelarray=[0]*len(self.rowsnames)
        self.valuelabelarray=[0]*len(self.rowsnames)
        #gridlayout= QtWidgets.QGridLayout()
        #self.window.setLayout(gridlayout)
        for i in range(len(self.rowsnames)):
            self.titlelabelarray[i]=QtWidgets.QLabel(self.window)
            self.titlelabelarray[i].resize=(self.columnwidth[0],self.lineheight)
            self.titlelabelarray[i].setText(' %s'%(self.rowsnames[i]))
            self.titlelabelarray[i].setAlignment(QtCore.Qt.AlignLeft)
#            self.titlelabelarray[i].setStyleSheet("font-size:12px;font-family:YF补 汉仪夏日体;")
            #titlelabelarray[i].setFrameShadow(QtWidgets.QFrame.Raised)
            #titlelabelarray[i].setStyleSheet('border-width: 1px;border-color: rgb(255, 255, 255)')
            self.titlelabelarray[i].move(0,self.lineheight*i)
            self.valuelabelarray[i]=QtWidgets.QLabel(self.window)
            self.valuelabelarray[i].resize=(self.columnwidth[1],self.lineheight)
            self.valuelabelarray[i].setText('0')
            self.valuelabelarray[i].setAlignment(QtCore.Qt.AlignLeft)
            #self.valuelabelarray[i].setStyleSheet("font-size:12px;")
            #valuelabelarray[i].setFrameShadow(QtWidgets.QFrame.Raised)
            #valuelabelarray[i].setStyleSheet('border-width: 1px;border-color: rgb(255, 255, 255)')
            self.valuelabelarray[i].move(self.columnwidth[0],self.lineheight*i)

    def retranslate(self):
        self.window.setWindowTitle(_("Counter"))
        self.action_replay.setText(_('Preview replay'))
        self.action_sboard.setText(_('Save board'))
        self.action_sreplay.setText(_('Save replay'))

    def create_rightmenu(self):
        self.menu=QtWidgets.QMenu()
        self.action_replay=QtWidgets.QAction(self.window)
        self.menu.addAction(self.action_replay)
        self.action_sboard=QtWidgets.QAction(self.window)
        self.menu.addAction(self.action_sboard)
        self.action_sreplay=QtWidgets.QAction(self.window)
        self.menu.addAction(self.action_sreplay)     
        self.menu.popup(QtGui.QCursor.pos())
        self.action_sreplay.triggered.connect(self.game.savereplay)
        self.action_sboard.triggered.connect(self.game.saveboard)  
        self.action_replay.triggered.connect(self.window.getpreview)   
        self.retranslate()
        if self.game.finish:
            self.action_sboard.setEnabled(True)
            self.action_sreplay.setEnabled(True)
            self.action_replay.setEnabled(True)
        else:
            self.action_sboard.setEnabled(False)
            self.action_sreplay.setEnabled(False)
            self.action_replay.setEnabled(False)
    
    def refreshvalues(self,status):
        allclicks=sum(self.game.allclicks[0:3])
        eclicks=sum(self.game.eclicks)
        if status==2:
            if self.game.isreplaying():
                rt=max(0,min(self.game.replayboardinfo[5],round(self.game.intervaltime,2)))
            else:
                rt=self.game.intervaltime
            allbv=self.game.bbbv
            solvedbv=self.game.solvedelse+self.game.solvedops
            if eclicks==0:
                ioe,corr,thrp=0,0,0
            else:
                ioe,corr,thrp=solvedbv/allclicks,eclicks/allclicks,solvedbv/eclicks
            if solvedbv==0:
                est=999.99
            else:
                est=rt/(solvedbv+2*self.game.solvedops)*(allbv+2*self.game.ops)
            if rt==0:
                bvs,cls,ces=0,0,0
            else:
                bvs,cls,ces=solvedbv/rt,allclicks/rt,eclicks/rt
            values=['%.2f'%(rt),'%.2f'%(est),'%d/%d'%(solvedbv,allbv),'%.3f'%(bvs),'%.3f'%(pow(est,1.7)/allbv)]
            values+=['%.2f'%(est*(est+1)/allbv),'%d/%d'%(self.game.solvedops,self.game.ops),'%d/%d'%(self.game.solvedislands,self.game.islands)]
            values+=['%d/%d/%d'%(self.game.allclicks[0],self.game.allclicks[1],self.game.allclicks[2])]
            values+=['%d'%(self.game.allclicks[3])]
            values+=['%d@%.3f'%(allclicks,cls)]
            values+=['%d@%.3f'%(eclicks,ces)]
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

    def closecounter(self):
        pass





                    
                
                
        
       
    
        
        
            
